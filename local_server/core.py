from contextlib import asynccontextmanager
import httpx
import numpy as np
import torch
import joblib
import pandas as pd
from io import StringIO
from fastapi import FastAPI, HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from database import DiabetesData, User
from schemas import UserCreate, DiabetesDataInput, Mail
from security import get_password_hash, verify_password
from model_utils import DiabetesBinaryNet
from config import settings
from security import get_password_hash, verify_password, create_access_token
from logging_config import get_logger
from mailing import send_email

logger = get_logger()
GLOBAL_SERVER_URL = settings.GLOBAL_SERVER_URL
API_KEY = settings.API_KEY

model = None
scaler = joblib.load(settings.SCALER_PATH)


# Convert lists back to PyTorch tensors
def convert_to_tensor(data):
    state_dict = {
        k: torch.tensor(v) if isinstance(v, (list, int, float)) else v 
        for k, v in data.items()
    }
    return state_dict

async def load_model():
    global model
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{GLOBAL_SERVER_URL}/model/global",
                headers={"X-API-Key": API_KEY}
            )
            model_data = response.json()
            
            
            state_dict = convert_to_tensor(model_data["weights"])

            model = DiabetesBinaryNet(len(model_data["features"]))
            model.load_state_dict(state_dict)
            logger.info("GLOBAL MODEL LOADED FROM SERVER")
            torch.save(model.state_dict(), settings.MODEL_PATH)
            
    except Exception as e:
        model = DiabetesBinaryNet(17)
        model.load_state_dict(torch.load(settings.MODEL_PATH, map_location=settings.DEVICE))
        logger.info("GLOBAL MODEL LOADED LOCALLY")
        
    model.eval()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await load_model()
    yield

async def register_user(user: UserCreate, db: Session):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    is_admin = db.query(User).count() == 0
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, role="ADMIN" if is_admin else "USER", full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def login_user(form_data, db: Session):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token, expire = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "exp" : int(expire), "role": user.role}

async def predict_diabetes(data: DiabetesDataInput, current_user: User, db: Session):
    global model
    features = np.array([[
        data.high_bp, data.high_chol, data.chol_check, data.bmi,
        data.smoker, data.stroke, data.heart_disease, data.phys_activity,
        data.fruits, data.veggies, data.hvy_alcohol, data.gen_hlth,
        data.ment_hlth, data.phys_hlth, data.diff_walk, data.sex, data.age
    ]])

    df = pd.DataFrame(features, columns=[
        "HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke",
        "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
        "HvyAlcoholConsump", "GenHlth", "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age"])
    
    features_scaled = scaler.transform(df)

    user_name = current_user.full_name if current_user.role == "USER" else data.full_name
    
    with torch.no_grad():
        output = model(torch.tensor(features_scaled, dtype=torch.float32))
        prediction = output.argmax(dim=1).item()
    
    db_data = DiabetesData(
        user_id=current_user.id,
        full_name=user_name,
        high_bp=data.high_bp,
        high_chol=data.high_chol,
        chol_check=data.chol_check,
        bmi=data.bmi,
        smoker=data.smoker,
        stroke=data.stroke,
        heart_disease=data.heart_disease,
        phys_activity=data.phys_activity,
        fruits=data.fruits,
        veggies=data.veggies,
        hvy_alcohol=data.hvy_alcohol,
        gen_hlth=data.gen_hlth,
        ment_hlth=data.ment_hlth,
        phys_hlth=data.phys_hlth,
        diff_walk=data.diff_walk,
        sex=data.sex,
        age=data.age,
        prediction=prediction
    )
    
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

async def get_prediction_history(current_user: User, db: Session):
    if current_user.role == "ADMIN":
        return db.query(DiabetesData).all()
    else:
        return db.query(DiabetesData).filter(DiabetesData.user_id == current_user.id).all()

async def train_local_model_with_csv(file: UploadFile, current_user: User, db: Session):
    global model

    if not file.filename.endswith(".csv"):
        logger.error("FILE MUST BE A CSV")
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))
        
        expected_features = [
        "HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke",
        "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
        "HvyAlcoholConsump", "GenHlth", "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age"]
        if not all(feature in df.columns for feature in expected_features):
            logger.error("CSV MUST CONTAIN ALL EXPECTED FEATURES")
            raise HTTPException(
                status_code=400,
                detail=f"CSV must contain the following features: {expected_features}"
            )
        
        features = df[expected_features]
        labels = df["prediction"].values if "prediction" in df.columns else None
        
        if labels is None:
            raise HTTPException(
                status_code=400,
                detail="CSV must contain a 'prediction' column for training"
            )
        
        logger.info("TRAINING LOCAL MODEL")
        features_scaled = scaler.transform(features)
        
        local_model = DiabetesBinaryNet(17)
        local_model.load_state_dict(model.state_dict())
        
        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(local_model.parameters(), lr=0.001)
        
        X = torch.tensor(features_scaled, dtype=torch.float32)
        y = torch.tensor(labels, dtype=torch.long)
        
        local_model.train()
        for epoch in range(5):
            print(f"Epoch {epoch}")
            optimizer.zero_grad()
            outputs = local_model(X)
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
        
        try:
            async with httpx.AsyncClient() as client:
                serialized_weights = {
                    key: value.cpu().tolist() 
                    for key, value in local_model.state_dict().items()
                }
                
                response = await client.post(
                    f"{GLOBAL_SERVER_URL}/model/update",
                    headers={"X-API-Key": API_KEY},
                    json=[{"weights": serialized_weights}],
                    timeout=30
                )

                if response.status_code == 200:
                    print("Global model updated")
                    torch.save(local_model.state_dict(), settings.MODEL_PATH)
                    response_data = response.json()
                    state_dict = convert_to_tensor(response_data["weights"])
                    model.load_state_dict(state_dict)
                    model.eval()
                    torch.save(model.state_dict(), settings.MODEL_PATH)
                    return {"message": "Local training completed and global model updated"}
        except httpx.HTTPStatusError as e:
            print(f"Failed to update global model: {e}")
            return {"message": "Local training completed, but global model update failed"}
        except httpx.RequestError as e:
            print(f"connection error: {e}")
            return {"message": "Local training completed, but global model update failed (failed to connect)"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")
    
async def  send_mail(mail:Mail, current_user: User, db: Session):
    user_full_name = current_user.full_name
    user_email = current_user.email
    subject = mail.subject
    message = mail.message
    # get the admin email 
    admin = db.query(User).filter(User.role == "ADMIN").first()
    admin_email = admin.email
    if send_email(message=message, sub=subject, sender_address=user_email, receiver_address=admin_email, receiver_full_name=admin.full_name, sender_full_name=user_full_name):
        return {"message": "Email sent successfully"}
    else:
        return HTTPException(status_code=500, detail="Failed to send email")
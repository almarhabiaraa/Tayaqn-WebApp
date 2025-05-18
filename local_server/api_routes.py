
from fastapi import APIRouter, Depends, UploadFile, File
from requests import Session
from typing import List

from database import  User
from schemas import  DiabetesDataInput, DiabetesDataOutput, Mail
from security import get_current_user,  get_db
from sqlalchemy.orm import Session
import schemas

from core import (
     predict_diabetes, get_prediction_history,
    train_local_model_with_csv, send_mail
)

router = APIRouter(prefix="/api", tags=["API"])

@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/predict", response_model=DiabetesDataOutput)
async def predict(
    data: DiabetesDataInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await predict_diabetes(data, current_user, db)

@router.get("/history", response_model=List[DiabetesDataOutput])
async def history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await get_prediction_history(current_user, db)

@router.post("/train")
async def train(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await train_local_model_with_csv(file, current_user, db)

@router.post("/contact")
async def contact(
    mail: Mail,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    return await send_mail(mail, current_user, db)
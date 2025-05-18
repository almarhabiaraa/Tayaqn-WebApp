from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum("ADMIN", "USER", name="user_roles"), default="USER")
    full_name = Column(String, nullable=True)

class DiabetesData(Base):
    __tablename__ = "diabetes_data"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    full_name = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    high_bp = Column(Integer)
    high_chol = Column(Integer)
    chol_check = Column(Integer)
    bmi = Column(Float)
    smoker = Column(Integer)
    stroke = Column(Integer)
    heart_disease = Column(Integer)
    phys_activity = Column(Integer)
    fruits = Column(Integer)
    veggies = Column(Integer)
    hvy_alcohol = Column(Integer)
    gen_hlth = Column(Integer)
    ment_hlth = Column(Integer)
    phys_hlth = Column(Integer)
    diff_walk = Column(Integer)
    sex = Column(Integer)
    age = Column(Integer)
    prediction = Column(Integer, nullable=True)

Base.metadata.create_all(bind=engine)

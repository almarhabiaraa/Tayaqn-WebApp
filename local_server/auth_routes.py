
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas import UserCreate, Token, User
from security import get_db
from core import (
    register_user, login_user)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return await register_user(user, db)

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return await login_user(form_data, db)

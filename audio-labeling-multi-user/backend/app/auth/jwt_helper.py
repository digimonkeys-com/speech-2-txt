from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

import os

from schemas import user_schemas, token_schemas
from db.database import get_db
from models.user_model import User
from auth.hash import Hash
from exceptions.exceptions import CredentialsException

from datetime import timedelta, datetime


router = APIRouter(tags=["Auth"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

auth_scheme = OAuth2PasswordBearer(tokenUrl='login')


def authenticate_user(
        email: str,
        password: str,
        db: Session = Depends(get_db)
):
    user = User.get_user_by_email(db, email).first()
    if not user:
        return False
    if not Hash.verify_password(password, user.password):
        return False
    return user


def create_token(data: dict, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
        token: str = Depends(auth_scheme),
        db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CredentialsException
        token_data = token_schemas.TokenData(email=email)
    except JWTError:
        raise CredentialsException
    user = User.get_user_by_email(db, email=token_data.email).first()
    if user is None:
        raise CredentialsException
    return user

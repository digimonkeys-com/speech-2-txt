from fastapi import APIRouter, Depends, status, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from datetime import timedelta
import os

from secrets import token_urlsafe

from schemas import token_schemas, user_schemas, info
from db.database import get_db
from auth.jwt_helper import authenticate_user, create_token, ACCESS_TOKEN_EXPIRE_MINUTES
from exceptions.exceptions import CredentialsException
from models.user_model import User, ResetPassword
from auth.sending_email import send_email_reset_password
from auth.hash import Hash
from routers.samples import create_recordings_for_user


router = APIRouter(prefix=f"{os.getenv('ROOT_PATH')}/v1", tags=["Auth"])


@router.post(
    '/login',
    response_model=token_schemas.Token
)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise CredentialsException
    access_token = create_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    create_recordings_for_user(db, user)
    return {"access_token": access_token, 'user_id': user.id}

@router.put(
    '/register',
    response_model=token_schemas.Token
)
async def register(
        email: str = Form(''),
        password: str = Form(''),
        name: str = Form(''),
        db: Session = Depends(get_db)
):

    passwd_hash = Hash.get_password_hash(password)

    user = User(email=email, password=passwd_hash, name=name)
    try:
        db.add(user)
        db.commit()
    except Exception as e:
        print(e)
        return {"access_token": "", 'user_id': -1}

    user = authenticate_user(email, password, db)
    if not user:
        raise CredentialsException
    access_token = create_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    create_recordings_for_user(db, user)
    return {"access_token": access_token, 'user_id': user.id}


@router.post(
    '/forgot-password',
    status_code=status.HTTP_200_OK,
    response_model=info.Info
)
async def forgot_password(
        request: user_schemas.ForgotPassword,
        db: Session = Depends(get_db),
):
    user = User.get_user_by_email(db, request.email).first()
    if not user:
        pass
    else:
        token_in_db = ResetPassword.get_unused_by_email(db, user.email).first()
        if token_in_db:
            reset_code = token_in_db.reset_code
        else:
            reset_code = token_urlsafe(16)
            code_in_db = ResetPassword(
                email=user.email,
                reset_code=reset_code
            )
            db.add(code_in_db)
            db.commit()
            db.refresh(code_in_db)
        await send_email_reset_password(email=[user.email], reset_code=reset_code)
    return {"info": "If we found an account associated with that email, we've sent a password reset message."}


@router.put(
    '/reset-password',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=info.Info

)
async def reset_password(
        request: user_schemas.ResetPassword,
        db: Session = Depends(get_db)
):
    reset_token = ResetPassword.get_unused_by_reset_code(db, request.reset_password_token).first()
    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reset password token has expired, please request a new one."
        )
    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Passwords do not match."
        )
    user = User.get_user_by_email(db, reset_token.email).first()
    if not user:
        pass
    else:
        user.password = Hash.get_password_hash(request.new_password)
        reset_token.status = True
        db.commit()
        db.refresh(user)
        db.refresh(reset_token)
    return {"info": "Password has been changed."}

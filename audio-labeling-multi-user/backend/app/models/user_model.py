import uuid

from fastapi import HTTPException, status

from datetime import datetime, timedelta

from sqlalchemy import Column, String, DateTime, Text, Boolean, Integer
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType

from db.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(EmailType, unique=True, nullable=False)
    password = Column(Text)
    name = Column(String(32), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    total_duration = Column(Integer)

    def __repr__(self):
        return f"<id: {self.id}, email: {self.email}>"

    @staticmethod
    def get_all_users(db):
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(db, user_id):
        try:
            uuid_user = uuid.UUID(user_id, version=4)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user id, try again."
            )
        if str(uuid_user) == user_id:
            return db.query(User).filter(User.user_id == user_id)

    @staticmethod
    def get_user_by_email(db, email):
        return db.query(User).filter(User.email == email)


class ResetPassword(Base):
    __tablename__ = "reset_password"
    reset_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128))
    reset_code = Column(String(128))
    status = Column(Boolean, default=False)
    expiry_time = Column(DateTime(timezone=True), default=datetime.utcnow()+timedelta(minutes=15))

    @staticmethod
    def get_unused_by_reset_code(db, reset_code):
        return db.query(ResetPassword)\
            .filter(ResetPassword.reset_code == reset_code)\
            .filter(ResetPassword.status == False)\
            .filter(ResetPassword.expiry_time > datetime.utcnow())

    @staticmethod
    def get_unused_by_email(db, email):
        return db.query(ResetPassword)\
            .filter(ResetPassword.email == email)\
            .filter(ResetPassword.status == False)\
            .filter(ResetPassword.expiry_time > datetime.utcnow())
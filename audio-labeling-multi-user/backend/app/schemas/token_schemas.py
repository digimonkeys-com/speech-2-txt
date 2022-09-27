from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    user_id: int


class TokenData(BaseModel):
    email: str | None = None

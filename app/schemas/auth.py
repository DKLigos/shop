from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    login: str
    password: str

class UserCreate(User):
    pass

class UserUpdate(User):
    pass

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
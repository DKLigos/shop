from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db_deps import get_db
from app.models import User
from app.schemas import UserCreate
from app.utils.hashing import Hash
from app.utils.jwttoken import create_access_token

from app.crud.crud_user import user as crud_user

router = APIRouter(tags=['Авторизация'])


@router.post('/register')
async def create_user(item: UserCreate, db: AsyncSession = Depends(get_db)):
    item.password = Hash.bcrypt(item.password)
    await crud_user.create(db, obj_in=dict(item))
    return {"res": "created"}



@router.post('/login')
async def login(item: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud_user.get(db, User.username == item.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неверный логин или пароль")

    if not Hash.verify(user.password, item.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неверный логин или пароль")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

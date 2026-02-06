from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
# from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt # pip install python-jose[cryptography]

from app.models.user import User
from app.schemas.user_schema import UserSignupRequest
from app.core.config import settings

import bcrypt


def hash_password(password: str) -> str:
    pw = password.encode('utf-8')
    salt = bcrypt.gensalt(12)
    hashed_bytes = bcrypt.hashpw(pw, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pw_bytes, hashed_bytes)

async def create_user(db: AsyncSession, user_data: UserSignupRequest) -> User:
    hashed_password = hash_password(user_data.password)
    
    new_user = User(
        email=user_data.email,
        password=hashed_password,
        full_name=user_data.full_name
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def login_user(db: AsyncSession, email: str, password: str) -> User:
    user = await get_user_by_email(db, email)
    
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINS)
    token_data = {"sub": str(user.email), "exp": datetime.now() + access_token_expires}
    access_token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    user.token = access_token
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
    
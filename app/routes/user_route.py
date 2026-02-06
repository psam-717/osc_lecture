from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.crud import user_crud
from app.schemas.user_schema import UserSignupRequest, UserResponse, UserLoginRequest

router = APIRouter(prefix="/users", tags=["users"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup_user(
    user_data: UserSignupRequest,
    db: AsyncSession = Depends(get_db)
):
    existing_user = await user_crud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = await user_crud.create_user(db, user_data)
    return new_user

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    login_user_data: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    existing_user = await user_crud.get_user_by_email(db, login_user_data.email)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account not registered"
        )
    logged_in_user = await user_crud.login_user(db, login_user_data.email, login_user_data.password)
    return logged_in_user
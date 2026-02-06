from pydantic import BaseModel, EmailStr, Field


class UserSignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str | None = Field(None, max_length=100)


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str | None

    model_config = {"from_attributes": True}


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str 

class UserLoginResponse(BaseModel):
    id: int
    email: str
    full_name: str | None
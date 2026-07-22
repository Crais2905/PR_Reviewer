from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPublic(UserBase):
    id: int
    is_active: bool

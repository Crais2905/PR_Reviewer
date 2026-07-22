from typing import Annotated

from fastapi import HTTPException, status, Depends, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from decouple import config

from app.auth.tokens import create_access_token, decode_token, create_refresh_token
from app.repositories.user import UserRepo, password_context
from app.schemas.user import UserCreate, UserLogin
from app.db.models import User

class UserService():
    def __init__(self, user_repository: UserRepo):
        self.user_repository = user_repository

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return password_context.verify(password, hashed_password)

    async def get_user(self, email: str, session: AsyncSession) -> User:
        return await self.user_repository.get_user_by_email(email, session)

    async def create_user(self, user_data: UserCreate, session: AsyncSession) -> User:
        existing_user = await self.user_repository.get_user_by_email(user_data.email, session)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email already exist"
            )

        result = await self.user_repository.write_to_db(user_data, session)
        return result

    async def check_user_cred(self, user_data: UserLogin, session: AsyncSession) -> User:
        user = await self.get_user(user_data.email, session)

        if (not user) or (not self.verify_password(user_data.password, user.hashed_password)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return user

    async def login_user(
            self,
            user_data: UserLogin,
            response: Response,
            access_token: Annotated[str | None, Cookie()],
            session: AsyncSession
    ) -> dict:
        if access_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are already logged in")

        user = await self.check_user_cred(user_data, session)
        access_token = await self.set_access_token(user, response)
        refresh_token = await self.set_refresh_token(user, response)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    @staticmethod
    async def logout_user(response: Response) -> dict:
        response.delete_cookie("access_token")
        return {"Log out": "successful"}

    async def refresh(
        self,
        response: Response,
        refresh_token: Annotated[str | None, Cookie()],
        session: AsyncSession
    ) -> dict:
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Can't get a refresh token")

        payload = decode_token(refresh_token)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await self.get_user(email, session)

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return await self.set_access_token(user, response)

    @staticmethod
    async def set_access_token(user: User, response: Response) -> dict:
        access_token = create_access_token({"sub": user.email})
        life_time = config("ACCESS_TOKEN_EXPIRE_MINUTES") * 60

        response.set_cookie("access_token", access_token, max_age=life_time)
        return {
            "access_token": access_token
        }

    @staticmethod
    async def set_refresh_token(user: User, response: Response) -> dict:
        refresh_token = create_refresh_token({"sub": user.email})
        life_time = config("ACCESS_TOKEN_EXPIRE_MINUTES") * 60

        response.set_cookie("refresh_token", refresh_token, max_age=life_time)
        return {
            "refresh_token": refresh_token
        }


def get_user_service(user_repo: UserRepo = Depends(UserRepo)) -> UserService:
    return UserService(user_repo)

from typing import Annotated

from fastapi import HTTPException, status, Depends, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.tokens import create_access_token
from app.repositories.user import UserRepo, password_context
from app.schemas.user import UserCreate, UserLogin


class UserService():
    def __init__(self, user_repository: UserRepo):
        self.user_repository = user_repository

    @staticmethod
    async def verify_password(password: str, hashed_password: str) -> bool:
        return password_context.verify(password, hashed_password)

    async def get_user(self, email: str, session: AsyncSession):
        return await self.user_repository.get_user_by_email(email, session)

    async def create_user(self, user_data: UserCreate, session: AsyncSession):
        existing_user = await self.user_repository.get_user_by_email(user_data.email, session)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email already exist"
            )

        result = await self.user_repository.write_to_db(user_data, session)
        return result

    async def login_user(
            self,
            user_data: UserLogin,
            response: Response,
            access_token: Annotated[str | None, Cookie()],
            session: AsyncSession
    ):
        print(access_token)
        if access_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are already logged in")

        user = await self.user_repository.get_user_by_email(user_data.email, session)

        if (not user) or (not self.verify_password(user_data.password, user.hashed_password)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token = create_access_token({"sub": user.email})
        response.set_cookie("access_token", access_token)

        return {
            "access_token": access_token
        }

    @staticmethod
    async def logout_user(response: Response):
        response.delete_cookie("access_token")
        return {"Log out": "successful"}


def get_user_service(user_repo: UserRepo = Depends(UserRepo)) -> UserService:
    return UserService(user_repo)
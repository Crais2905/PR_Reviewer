from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserRepo, password_context
from app.schemas.user import UserCreate


class UserService():
    def __init__(self, user_repository: UserRepo):
        self.user_repository = user_repository

    @staticmethod
    async def verify_password(password: str, hashed_password: str):
        return password_context.verify(password, hashed_password)

    async def get_user(self, email: str, session: AsyncSession):
        return await self.user_repository.get_user_by_email(email, session)

    async def create_user(self, user_data: UserCreate, session):
        existing_user = await self.user_repository.get_user_by_email(user_data.email, session)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email already exist"
            )

        result = await self.user_repository.write_to_db(user_data, session)
        return result


def get_user_service(user_repo: UserRepo = Depends(UserRepo)) -> UserService:
    return UserService(user_repo)
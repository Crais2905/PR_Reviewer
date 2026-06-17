from typing import Annotated

from fastapi import APIRouter, status, Depends, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.schemas.user import UserCreate, UserPublic, UserLogin
from app.db.session import get_session
from app.services.user import UserService, get_user_service


router = APIRouter()


@router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def register_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session)
):
    return await user_service.create_user(user_data, session)


@router.post("/login/", status_code=status.HTTP_200_OK)
async def login_user(
    user_data: UserLogin,
    response: Response,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session),
    access_token: Annotated[str | None, Cookie()] = None
):
    return await user_service.login_user(user_data, response, access_token, session)


@router.post("/logout/", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(
    response: Response,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.logout_user(response)


@router.get("/profile/", status_code=status.HTTP_200_OK, response_model=UserPublic)
async def profile_user(
    current_user: UserPublic = Depends(get_current_user)
):
    return current_user

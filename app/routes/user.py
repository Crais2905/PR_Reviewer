from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.schemas.user import UserCreate, UserPublic
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

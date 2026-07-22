from typing import List, Annotated

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.services.review import ReviewService, get_review_service
from app.schemas.review import ReviewCreate, ReviewPublic, ReviewFilterParams
from app.db.session import get_session
from app.db.models import User


router = APIRouter()


@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=ReviewPublic)
async def create_review(
    pr_data: ReviewCreate,
    review_service: ReviewService = Depends(get_review_service),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return await review_service.create_review(pr_data, current_user.id, session)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ReviewPublic])
async def get_reviews(
    filter_query: Annotated[ReviewFilterParams, Query()],
    review_service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await review_service.get_reviews(current_user.id, filter_query, session)


@router.get("/{review_id}", status_code=status.HTTP_200_OK, response_model=ReviewPublic)
async def get_review(
    review_id: int,
    review_service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await review_service.get_review(review_id, current_user.id, session)

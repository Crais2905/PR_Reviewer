from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.services.review import ReviewService, get_review_service
from app.schemas.review import ReviewCreate, ReviewPublic
from app.db.session import get_session


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReviewPublic)
async def create_review(
    review_data: ReviewCreate,
    review_service: ReviewService = Depends(get_review_service),
    session: AsyncSession = Depends(get_session)
):
    return await review_service.create_review(review_data, session)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ReviewPublic])
async def get_reviews(
    review_service: ReviewService = Depends(get_review_service),
    session: AsyncSession = Depends(get_session),
):
    return await review_service.get_reviews(session)


@router.get("/{review_id}", status_code=status.HTTP_200_OK, response_model=ReviewPublic)
async def get_review(
    review_id: int,
    review_service: ReviewService = Depends(get_review_service),
    session: AsyncSession = Depends(get_session)
):
    result = await review_service.get_review(review_id, session)
    print(result)
    return result

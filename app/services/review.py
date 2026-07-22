import asyncio
from typing import List, Sequence

from fastapi import HTTPException, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession


from app.repositories.review import ReviewRepo
from app.schemas.review import ReviewCreate, ReviewCreateDB, ReviewFilterParams
from app.db.models import Review
from app.back_tasks.review import create_review_task
from app.enums.review_status import ReviewStatus


class ReviewService:
    def __init__(self, review_repository: ReviewRepo):
        self.review_repository = review_repository

    async def create_review(self, review_data: ReviewCreate, user_id: int, session: AsyncSession) -> Review:
        new_review_data = ReviewCreateDB(**review_data.model_dump(), user_id=user_id)
        review = await self.review_repository.write_to_db(new_review_data, session)
        await self.review_repository.change_review_status(review, ReviewStatus.processing, session)

        create_review_task.delay(review.id)

        return review

    async def get_reviews(
            self, user_id: int,
            filter_query: ReviewFilterParams,
            session: AsyncSession
    ) -> Sequence[Review]:
        return await self.review_repository.get_user_reviews(user_id, filter_query, session)

    async def get_review(self, review_id: int, user_id: int, session: AsyncSession) -> Review:
        review = await self.review_repository.get_object_by_unic_field(review_id, Review.id, session)

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with id {review_id} not found"
            )

        if review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This review is forbidden for you. Please choose your review"
            )

        return review


def get_review_service(review_repo: ReviewRepo = Depends(ReviewRepo)) -> ReviewService:
    return ReviewService(review_repo)


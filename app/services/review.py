from fastapi import HTTPException, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession


from app.repositories.review import ReviewRepo
from app.schemas.review import ReviewCreate
from app.db.models import Review


class ReviewService():
    def __init__(self, review_repository: ReviewRepo):
        self.review_repository = review_repository

    async def create_review(self, review_data: ReviewCreate, session: AsyncSession):
        return await self.review_repository.write_to_db(review_data, session)

    async def get_reviews(self, session: AsyncSession):
        return await self.review_repository.get_objects(session)

    async def get_review(self, review_id: int,  session: AsyncSession):
        review = await self.review_repository.get_object_by_unic_field(review_id, Review.id, session)

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with id {review_id} not found"
            )

        return review


def get_review_service(review_repo: ReviewRepo = Depends(ReviewRepo)) -> ReviewService:
    return ReviewService(review_repo)


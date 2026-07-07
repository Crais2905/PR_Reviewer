import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncCelerySession
from app.repositories.review import ReviewRepo
from app.db.models import Review
from app.enums.review_status import ReviewStatus


class BGReviewService:
    def __init__(self, review_repository: ReviewRepo):
        self.review_repository = review_repository

    async def ai_analys(self, review: Review):
        await asyncio.sleep(20)

    async def review_process(self, review_id: int):
        async with AsyncCelerySession() as session:
            review = await self.review_repository.get_object_by_unic_field(
                review_id,
                Review.id,
                session
            )

            if review is None:
                return

            try:
                await self.ai_analys(review)
                await self.review_repository.change_review_status(
                    review,
                    ReviewStatus.completed,
                    session
                )
            except Exception as e:
                print(f"[ERROR]: {e}")

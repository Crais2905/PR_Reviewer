from app.db.session import AsyncCelerySession
from app.repositories.review import ReviewRepo
from app.db.models import Review
from app.enums.review_status import ReviewStatus
from app.ai.service import AIAnalysisService, ReviewResponse


class BGReviewService:
    def __init__(self, review_repository: ReviewRepo, ai_service: AIAnalysisService):
        self.review_repository = review_repository
        self.ai_service = ai_service

    async def ai_analys(self, review_diff: str) -> ReviewResponse:
        return await self.ai_service.get_review(review_diff)

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
                response = await self.ai_analys(review.diff)
                await self.review_repository.change_review_status(
                    review,
                    ReviewStatus.completed,
                    session
                )
                await self.review_repository.add_analys(review, response, session)

            except Exception as e:
                print(f"[ERROR]: {e}")
                await self.review_repository.change_review_status(
                    review,
                    ReviewStatus.failed,
                    session
                )

from app.db.session import AsyncCelerySession
from app.repositories.review import ReviewRepo
from app.db.models import Review
from app.enums.review_status import ReviewStatus
from app.ai.service import AIAnalysisService, ReviewResponse
from app.services.git_hub import GitParser
from app.repositories.problems import ProblemsRepo


class BGReviewService:
    def __init__(
            self,
            review_repository: ReviewRepo,
            problems_repository: ProblemsRepo,
            ai_service: AIAnalysisService,
            git_service: GitParser
    ):
        self.review_repository = review_repository
        self.problems_repository = problems_repository
        self.ai_service = ai_service
        self.git_parser = git_service

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
                pr_diff = await self.git_parser.get_pr_diff(review.pr_url)
                await self.review_repository.set_diff(review, pr_diff, session)

                response = await self.ai_analys(review.diff)

                await self.review_repository.change_review_status(
                    review,
                    ReviewStatus.completed,
                    session
                )

                await self.problems_repository.bulk_create_problems(response.finding_problems, review.id, session)
                await self.review_repository.add_analys(review, response, session)

            except Exception as e:
                print(f"[ERROR]: {e}")
                await self.review_repository.change_review_status(
                    review,
                    ReviewStatus.failed,
                    session
                )

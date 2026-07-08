from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas import ReviewResponse
from app.repositories.connector import Connector
from app.db.models import Review
from app.enums.review_status import ReviewStatus


class ReviewRepo(Connector):
    def __init__(self):
        super().__init__(Review)

    async def get_user_reviews(
            self,
            user_id: int,
            session: AsyncSession,
            offset: int = 0,
            limit: int = 10,
            filters: list | None = None,
    ):
        stmt = select(self.model).where(self.model.user_id == user_id)

        if filters:
            stmt = stmt.where(*filters)

        stmt = stmt.offset(offset).limit(limit)
        return await session.scalars(stmt)

    @staticmethod
    async def change_review_status(
            review: Review,
            new_status: ReviewStatus,
            session: AsyncSession
    ):
        review.status = new_status.value
        await session.commit()
        await session.refresh(review)

    @staticmethod
    async def add_analys(review: Review, ai_response: ReviewResponse, session: AsyncSession):
        data = ai_response.model_dump()
        print(data)
        review.summary = data["summary"]
        review.overall_comment = data["overall_comment"]
        review.risk = data["risk"].value

        await session.commit()
        await session.refresh(review)

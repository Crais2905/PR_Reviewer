from typing import List, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas import ReviewResponse
from app.repositories.connector import Connector
from app.db.models import Review
from app.enums.review_status import ReviewStatus
from app.schemas.review import ReviewFilterParams, ReviewPublic


class ReviewRepo(Connector):
    def __init__(self):
        super().__init__(Review)

    async def get_user_reviews(
            self,
            user_id: int,
            filters_query: ReviewFilterParams,
            session: AsyncSession,
    ) -> Sequence[Review]:
        stmt = (select(self.model).where(self.model.user_id == user_id))

        if filters_query.order_by_created_time:
            stmt = stmt.order_by(self.model.create_at.desc())

        stmt = stmt.offset(filters_query.offset).limit(filters_query.limit)
        result = await session.scalars(stmt)
        return result.all()

    @staticmethod
    async def change_review_status(
            review: Review,
            new_status: ReviewStatus,
            session: AsyncSession
    ) -> None:
        review.status = new_status.value
        await session.commit()
        await session.refresh(review)

    @staticmethod
    async def add_analys(review: Review, ai_response: ReviewResponse, session: AsyncSession) -> None:
        data = ai_response.model_dump()
        review.summary = data["summary"]
        review.overall_comment = data["overall_comment"]
        review.risk = data["risk"].value

        await session.commit()
        await session.refresh(review)

    @staticmethod
    async def set_diff(review: Review, diff: str, session: AsyncSession) -> None:
        review.diff = diff

        await session.commit()
        await session.refresh(review)

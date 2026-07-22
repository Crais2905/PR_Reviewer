from sqlalchemy import select
from sqlalchemy.orm import Session, noload

from app.db.models import Review
from app.enums.review_status import ReviewStatus


class BGReviewRepo:
    @staticmethod
    def get_review_by_id(review_id: int, session: Session) -> Review:
        stmt = (
            select(Review)
            .options(noload(Review.user))
            .where(Review.id == review_id)
        )
        return session.scalar(stmt)

    @staticmethod
    def change_review_status(review: Review, new_status: ReviewStatus,  session: Session) -> None:
        review.status = new_status.value
        session.commit()

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.review_status import ReviewStatus


class ReviewBase(BaseModel):
    title: str
    diff: str
    user_id: int
    status: ReviewStatus


class ReviewCreate(ReviewBase):
    model_config = ConfigDict(use_enum_values=True)


class ReviewPublic(ReviewBase):
    id: int

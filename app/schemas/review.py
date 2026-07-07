from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.review_status import ReviewStatus


class ReviewBase(BaseModel):
    title: str
    diff: str


class ReviewCreate(ReviewBase):
    model_config = ConfigDict(use_enum_values=True)


class ReviewCreateDB(ReviewCreate):
    user_id: int


class ReviewPublic(ReviewBase):
    id: int
    user_id: int
    status: ReviewStatus
    create_at: datetime


class TaskStatusPublic(BaseModel):
    task_id: str
    status: str
    result: ReviewPublic | None = None

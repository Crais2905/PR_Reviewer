from datetime import datetime
from typing import Optional

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
    summary: Optional[str] = None
    overall_comment: Optional[str] = None
    risk: Optional[str] = None
    create_at: datetime


class TaskStatusPublic(BaseModel):
    task_id: str
    status: str
    result: ReviewPublic | None = None

from datetime import datetime
from typing import Optional, List, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.enums.review_status import ReviewStatus
from app.ai.schemas import ProblemsResponse


class ReviewBase(BaseModel):
    title: str
    pr_url: str


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
    problems: List[ProblemsResponse]
    create_at: datetime


class ReviewFilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=20)
    offset: int = Field(0, ge=0)
    order_by_created_time: bool = True

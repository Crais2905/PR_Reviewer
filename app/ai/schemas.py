from enum import Enum
from pydantic import BaseModel, Field


class RiskLvl(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ReviewResponse(BaseModel):
    summary: str = Field(description="Short review of the diff")
    risk: RiskLvl = Field(description="Risk lvl of this changes")
    overall_comment: str = Field(description="An explanation of what was done well and what was done poorly")
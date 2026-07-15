from enum import Enum
from typing import List

from pydantic import BaseModel, Field, ConfigDict

from app.enums.category_problems import ProblemsCategory


class RiskLvl(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ProblemsResponse(BaseModel):
    category: ProblemsCategory = Field(description="Problem category")
    severity: RiskLvl = Field(description="Risk lvl of this problem")
    title: str = Field(description="Title which contain the key words of problem")
    description: str = Field(description="Short description of the problem")
    recommendation: str = Field(description="Recommendation how to improve code and solve the problem")

    model_config = ConfigDict(use_enum_values=True)


class ReviewResponse(BaseModel):
    summary: str = Field(description="Short review of the diff")
    risk: RiskLvl = Field(description="Risk lvl of this changes")
    overall_comment: str = Field(description="An explanation of what was done well and what was done poorly")
    finding_problems: List[ProblemsResponse] = Field("List with info about finding problems in diff")




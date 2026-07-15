from typing import List

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.connector import Connector
from app.db.models import ReviewProblems
from app.ai.schemas import ProblemsResponse

class ProblemsRepo(Connector):
    def __init__(self):
        super().__init__(ReviewProblems)

    async def bulk_create_problems(self, problems_response: List[ProblemsResponse], review_id: int, session: AsyncSession):
        for problem_data in problems_response:
            data = problem_data.model_dump()
            data["review_id"] = review_id

            stmt = insert(self.model).values(data).returning(self.model)
            await session.execute(stmt)
            await session.commit()


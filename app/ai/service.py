from fastapi import Depends

from app.ai.client import get_gemini_model, Client
from app.ai.schemas import ReviewResponse
from app.ai.prompts import AIPrompts


class AIAnalysisService:
    def __init__(self, client: Client):
        self.client: Client = client

    async def get_review(self, diff: str):
        prompt = AIPrompts.DIFF_REVIEW.render(diff=diff)

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': ReviewResponse
            }
        )

        return response.parsed

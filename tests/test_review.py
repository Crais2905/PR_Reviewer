from unittest.mock import patch
import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.ai.client import get_gemini_model
from app.enums.review_status import ReviewStatus
from app.repositories.problems import ProblemsRepo
from app.repositories.review import ReviewRepo
from app.services.bg_review import BGReviewService
from app.services.git_hub import GitParser
from app.ai.service import AIAnalysisService
from tests.conftest import FAKE_AI_RESPONSE
from tests.test_user import user_factory


@pytest_asyncio.fixture
async def review_factory(authorized_client: AsyncClient, user_factory):
    async def _create(title: str = "Test Review", pr_url: str = "Test Url"):
        with patch("app.back_tasks.review.create_review_task.delay"):
            response = await authorized_client.post(
                "/reviews/",
                json={
                    "title": title,
                    "pr_url": pr_url,
                },
            )
        assert response.status_code == 202
        return response.json()["id"]
    return _create




@pytest.mark.asyncio
async def test_create_review(authorized_client: AsyncClient):
    with patch("app.back_tasks.review.create_review_task.delay") as mock_delay:
        response = await authorized_client.post(
            "/reviews/",
            json={"title": "Test Review", "pr_url":  "Test Url"},
        )

    assert response.status_code == 202
    review_id = response.json()["id"]
    assert response.json()["status"] == "processing"
    assert response.json()["pr_url"] == "Test Url"
    mock_delay.assert_called_once_with(review_id)


@pytest.mark.asyncio
async def test_review_process_success(authorized_client: AsyncClient, review_factory, mock_external_apis):
    review_id = await review_factory()

    service = BGReviewService(
        review_repository=ReviewRepo(),
        problems_repository=ProblemsRepo(),
        ai_service=AIAnalysisService(client=get_gemini_model()),
        git_service=GitParser(),
    )
    await service.review_process(review_id)

    response = await authorized_client.get(
        f"/reviews/{review_id}"
    )
    assert response.status_code == 200
    resp_body = response.json()
    assert resp_body["status"] == ReviewStatus.completed.value
    assert resp_body["summary"] == "Overall looks fine, one minor issue found"

    problems = resp_body["problems"]
    assert len(problems) == len(FAKE_AI_RESPONSE.finding_problems)

@pytest.mark.asyncio
async def test_create_review_bad_input(authorized_client: AsyncClient, user_factory):
    """
    input json haven't diff field
    """
    response = await authorized_client.post(
        "/reviews/",
        json={
            "title": "Test Review",
            "user_id": 1,
            "status": "pending"
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_reviews(authorized_client: AsyncClient, review_factory):
    review_id = await review_factory()

    service = BGReviewService(
        review_repository=ReviewRepo(),
        problems_repository=ProblemsRepo(),
        ai_service=AIAnalysisService(client=get_gemini_model()),
        git_service=GitParser(),
    )
    await service.review_process(review_id)

    response = await authorized_client.get(
        "/reviews/"
    )
    assert response.status_code == 200
    assert response.json()[0]["pr_url"] == "Test Url"
    assert len(response.json()[0]["problems"]) == 1


@pytest.mark.asyncio
async def test_get_reviews_empty_list(authorized_client: AsyncClient, user_factory):
    response = await authorized_client.get(
        "/reviews/"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_review_bad_id(authorized_client: AsyncClient):
    response = await authorized_client.get(
        "/reviews/1"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_review(authorized_client: AsyncClient, review_factory):
    review_id = await review_factory()

    response = await authorized_client.get(
        f"/reviews/{review_id}"
    )
    assert response.status_code == 200
    assert response.json()["pr_url"] == "Test Url"




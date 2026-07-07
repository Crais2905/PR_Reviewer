import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient

from tests.test_user import user_factory


@pytest_asyncio.fixture
async def review_factory(authorized_client: AsyncClient, user_factory):
    async def _create(title: str = "Test Review", diff: str = "QWerty"):
        response = await authorized_client.post(
            "/reviews/",
            json={
                "title": title,
                "diff": diff,
            },
        )
        assert response.status_code == 202
        return response.json()["id"]
    return _create


@pytest.mark.asyncio
async def test_create_review(authorized_client: AsyncClient, user_factory):
    response = await authorized_client.post(
        "/reviews/",
        json={
            "title": "Test Review",
            "diff": "QWerty",
        },
    )

    assert response.status_code == 202
    assert response.json()["status"] == "processing"
    review_id = response.json()["id"]

    await asyncio.sleep(20)

    response = await authorized_client.get(f"/reviews/{review_id}")


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


@pytest.mark.asyncion
async def test_get_reviews(authorized_client: AsyncClient, review_factory):
    await review_factory()

    response = await authorized_client.get(
        "/reviews/"
    )
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Test Review"


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
    assert response.json()["title"] == "Test Review"


@pytest.mark.asyncio
async def test_get_review_bad_user(authorized_client: AsyncClient, review_factory, user_factory):
    review_id = await review_factory()



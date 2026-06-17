import pytest
import pytest_asyncio
from httpx import AsyncClient

from tests.test_user import user_factory


@pytest_asyncio.fixture
async def review_factory(client: AsyncClient, user_factory):
    async def _create(title: str = "Test Review", diff: str = "QWerty"):
        user_id = await user_factory(get_id=True)

        response = await client.post(
            "/reviews/",
            json={
                "title": title,
                "diff": diff,
                "user_id": user_id,
                "status": "pending"
            },
        )
        assert response.status_code == 201
        return response.json()["id"]
    return _create


@pytest.mark.asyncio
async def test_create_review(client: AsyncClient, user_factory):
    await user_factory()

    response = await client.post(
        "/reviews/",
        json={
            "title": "Test Review",
            "diff": "QWerty",
            "user_id": 1,
            "status": "pending"
        },
    )

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_review_bad_input(client: AsyncClient, user_factory):
    """
    input json haven't diff field
    """
    await user_factory()

    response = await client.post(
        "/reviews/",
        json={
            "title": "Test Review",
            "user_id": 1,
            "status": "pending"
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncion
async def test_get_reviews(client: AsyncClient, review_factory):
    await review_factory()

    response = await client.get(
        "/reviews/"
    )
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Test Review"


@pytest.mark.asyncio
async def test_get_reviews_empty_list(client: AsyncClient, user_factory):
    response = await client.get(
        "/reviews/"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_review_bad_id(client: AsyncClient, user_factory):
    response = await client.get(
        "/reviews/1"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_review(client: AsyncClient, review_factory):
    review_id = await review_factory()

    response = await client.get(
        f"/reviews/{review_id}"
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Review"


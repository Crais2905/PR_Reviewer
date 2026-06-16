import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture
async def user_factory(client: AsyncClient):
    async def _create(
            firstname: str = "Test",
            lastname: str = "User",
            email: str = "testuser@gmail.com",
            password: str = "testpassword",
            get_email: bool = False
    ):
        response = await client.post(
            "/auth/register/",
            json={
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "password": password,
            },
        )
        assert response.status_code == 201

        if get_email:
            response = await client.get("/auth/me/")
            return response.json()["email"]
        return
    return _create


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/auth/register/",
        json={
            "firstname": "Test",
            "lastname": "User",
            "email": "testuser@gmail.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, user_factory):
    await user_factory()

    response = await client.post(
        "/auth/login/",
        json={"email": "testuser@gmail.com", "password": "testpassword"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_auth_user(client: AsyncClient, user_factory):
    await user_factory()

    response = await client.post(
        "/auth/login/",
        json={"email": "testuser@gmail.com", "password": "testpassword"},
    )
    assert response.status_code == 200

    response = await client.post(
        "/auth/login/",
        json={"email": "testuser@gmail.com", "password": "testpassword"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_user_profile(authorized_client: AsyncClient):
    response = await authorized_client.get("/auth/profile/")

    assert response.status_code == 200
    assert response.json()["firstname"] == "First"
    assert response.json()["lastname"] == "Name"


@pytest.mark.asyncio
async def test_user_profile(client: AsyncClient):
    response = await client.get("/auth/profile/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_user_logout(authorized_client: AsyncClient):
    response = await authorized_client.post("/auth/logout/")
    assert response.status_code == 204

    response = await authorized_client.get("/auth/profile/")
    assert response.status_code == 401



from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from decouple import config

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.main import app
from app.db.models import Base, User
from app.db.session import get_session
from app.services.git_hub import GitParser
from app.ai.service import AIAnalysisService
from app.ai.schemas import ReviewResponse, ProblemsResponse
from app.celery_app import celery
import app.services.bg_review as bg_review_module


engine = create_async_engine(config("DATABASE_TEST_URL"), future=True)
test_celery_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


FAKE_DIFF = "diff --git a/main.py b/main.py\n@@ -1,3 +1,3 @@\n-old\n+new\n"

FAKE_AI_RESPONSE = ReviewResponse(
    summary="Overall looks fine, one minor issue found",
    risk="low",
    overall_comment="Overall looks fin",
    finding_problems=[
        ProblemsResponse(
            comment="Consider renaming variable for clarity",
            severity="low",
            category="bug_risk",
            title="Clarity",
            description="Consider renaming variable for clarity",
            recommendation="Recommendation"
        )
    ],
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    async def override_get_session():
        yield db_session
        await db_session.commit()

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Content-Type": "application/json"},
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def authorized_client(client: AsyncClient) -> AsyncClient:
    resp = await client.post(
        "/auth/register/",
        json={
            "firstname": "First",
            "lastname": "Name",
            "email": "test@gmail.com",
            "password": "testpassword",
        },
    )
    assert resp.status_code == 201, resp.text

    resp = await client.post(
        "/auth/login/",
        json={"email": "test@gmail.com", "password": "testpassword"},
    )
    assert resp.status_code == 200, resp.text

    client.headers.update({"Authorization": f"Bearer {resp.json()['access_token']}"})
    return client


@pytest.fixture(autouse=True, scope="session")
def celery_eager_mode():
    celery.conf.update(
        task_always_eager=True,
        task_eager_propagates=True,
    )


@pytest_asyncio.fixture(autouse=True)
def mock_external_apis():
    with patch.object(
        GitParser, "get_pr_diff", new=AsyncMock(return_value=FAKE_DIFF)
    ), patch.object(
        AIAnalysisService, "get_review", new=AsyncMock(return_value=FAKE_AI_RESPONSE)
    ):
        yield


@pytest_asyncio.fixture(autouse=True)
def patch_celery_session():
    with patch.object(bg_review_module, "AsyncCelerySession", test_celery_sessionmaker):
        yield

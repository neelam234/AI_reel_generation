import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from app.core.database import Base, engine, get_db
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import uuid
import asyncio

# Use an in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_project():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/projects/", json={"title": "Test Project"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Project"
    assert "id" in data
    assert data["status"] == "created"

@pytest.mark.asyncio
async def test_get_project_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(f"/api/projects/{uuid.uuid4()}")
    assert response.status_code == 404

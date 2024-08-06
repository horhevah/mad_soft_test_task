import asyncio
import os
from pathlib import Path
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from auth.models import User
from auth.users import current_active_user, fastapi_users
from database import get_async_session, Base
from main import app
from memes import services

# DATABASE
# DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL_TEST = f'sqlite+aiosqlite:///{BASE_DIR}/database_test.db'

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker_test = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
# metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker_test() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


user = User(
  email="user@example.com",
  hashed_password="aaa",
  is_active=True,
  is_verified=True,
  is_superuser=False,
)

app.dependency_overrides[current_active_user] = lambda: user


@pytest.fixture(autouse=True, scope='function')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
# @pytest.fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def minio_mock(monkeypatch):

    def mocked_minio(filename, file):
        pass
    # patch the module with the mocked function
    monkeypatch.setattr(services, "post_image_to_minio", mocked_minio)
    # first = 1
    # second = 2
    # actual_value = func2(first, second)
    # assert actual_value == first + second + mocked_value


@pytest.fixture
def send_post():
    memes_data = {
            'title': 'title',
            'category': 'category',
        }
    with open(os.path.join(BASE_DIR, 'tests', 'test_image.png'), 'rb') as f:
        response = client.post('/api/v1/memes', data=memes_data, files={"file": ("test_img.jpg", f, "image/png")})

    return response

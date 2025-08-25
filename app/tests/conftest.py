import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest_asyncio
from httpx import AsyncClient
from app.main import app
from app.database import async_session, get_db

@pytest_asyncio.fixture
async def async_client():
    async def override_get_db():
        async with async_session() as session:
            yield session

    # Override dependency
    app.dependency_overrides[get_db] = override_get_db

    try:
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
    finally:
        app.dependency_overrides.clear()

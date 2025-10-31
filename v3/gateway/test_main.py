import pytest
from main import app
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/manage/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


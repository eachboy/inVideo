import httpx
from app.main import app

transport = httpx.ASGITransport(app=app)


async def test_read_health():
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

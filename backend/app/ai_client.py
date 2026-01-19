import os
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

AI_SERVICE_URL = os.getenv(
    "AI_SERVICE_URL",
    "http://open-ai-service:8001"
)

TIMEOUT = 5.0

@retry(stop=stop_after_attempt(2), wait=wait_exponential(min=0.5, max=2))
async def generate_excuse(tone: str, days: int) -> str:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.post(
            f"{AI_SERVICE_URL}/generate",
            json={"tone": tone, "days": days}
        )

        if response.status_code != 200:
            raise RuntimeError("AI service error")

        return response.json()["excuse"]

import asyncio
import httpx
from locust import User, task, between

# macOS fix for event loop
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

class FastAPIHTTP2User(User):
    wait_time = between(1, 3)

    def on_start(self):
        # Force asyncio backend even for h2
        self.client = httpx.AsyncClient(
            base_url="https://127.0.0.1:8000",
            verify=False,
            http2=False,
            backend="asyncio"
        )

    @task
    async def list_authors(self):
        await self.client.get("/api/v1/authors/")

    def on_stop(self):
        asyncio.run(self.client.aclose())

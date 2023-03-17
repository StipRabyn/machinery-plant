from aioredis import from_url


class Database:
    def __init__(self, url):
        self.url = url

    async def __aenter__(self):
        self.db = from_url(url=self.url,
                           decode_responses=True)
        return self.db

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.db.close()
    

from aioredis import Redis


class Database:
    def __init__(self, url):
        self.url = url

    async def __aenter__(self):
        self.db = Redis(host=self.url,
                        decode_responses=True)
        return self.db

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.db.close()
    

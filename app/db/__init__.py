import asyncpg

from app.core.config import settings


class Database:
    def __init__(self):
        self.user = settings.POSTGRES_USER
        self.password = settings.POSTGRES_PASSWORD
        self.host = settings.POSTGRES_SERVER
        self.port = "5432"
        self.database = settings.POSTGRES_DB
        self._cursor = None
        self._connection_pool = None
        self.con = None

    async def connect(self):
        if not self._connection_pool:
            self._connection_pool = await asyncpg.create_pool(
                min_size=1,
                max_size=settings.POSTGRES_POOL_SIZE,
                command_timeout=settings.POSTGRES_POOL_TIMEOUT,
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )

    async def fetch_rows(self, query: str):
        if not self._connection_pool:
            await self.connect()
        else:
            self.con = await self._connection_pool.acquire()
            try:
                result = await self.con.fetch(query)
                return result
            except Exception as e:
                print(e)
            finally:
                await self._connection_pool.release(self.con)

    async def get_pool(self):
        if not self._connection_pool:
            await self.connect()
        return self._connection_pool

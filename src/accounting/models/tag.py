import asyncpg

from src import settings


class Tag:

    def __init__(self, id: int=None, name: str=None):
        self.id = id
        self.name = name

    async def save(self):
        con = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME
        )
        self.id = await con.fetchval(
            'insert into tags(name) values ($1) RETURNING id',
            self.name,
        )
        await con.close()

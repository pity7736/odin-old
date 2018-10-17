import asyncpg

from src import settings


class Category:

    def __init__(self, name: str, description: str):
        self.id = None
        self.name = name
        self.description = description

    async def save(self):
        con = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME
        )
        self.id = await con.fetchval(
            'insert into categories(name, description) values ($1, $2) RETURNING id', self.name, self.description
        )

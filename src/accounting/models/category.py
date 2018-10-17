import asyncpg

from src import settings


class Category:

    def __init__(self, name: str, description: str):
        self.id = None
        self.name = name
        self.description = description

    async def save(self):
        print('database', settings.DB_DATABASE)
        con = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_DATABASE
        )
        self.id = await con.fetchval('insert into categories(name, description) values ($1, $2) RETURNING id', self.name, self.description)

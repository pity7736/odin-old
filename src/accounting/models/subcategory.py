import asyncpg

from src import settings
from src.accounting.models import Category


class SubCategory:

    def __init__(self, id: int=None, name: str=None, category: Category=None, category_id: int=None):
        self.id = id
        self.name = name
        self.category = category
        self.category_id = category_id

    async def save(self):
        con = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME
        )
        self.id = await con.fetchval(
            'insert into subcategories(name, category_id) values ($1, $2) RETURNING id',
            self.name,
            self.category_id or getattr(self.category, 'id', None)
        )

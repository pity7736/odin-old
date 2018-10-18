import datetime

import asyncpg

from src import settings
from src.accounting.models import Category


class Movement:

    def __init__(self, id=None, type=None, date=None, value=None, note=None, category=None, category_id=None):
        self.id = id
        self.type = type
        self.date = date
        self.value = value
        self.note = note
        self._category = category
        self.category_id = category_id

    async def save(self):
        if isinstance(self.date, str):
            self.date = datetime.date.fromisoformat(self.date)

        con = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME
        )

        self.id = await con.fetchval(
            'insert into movements(type, date, value, note, category_id) values ($1, $2, $3, $4, $5) RETURNING id',
            self.type,
            self.date,
            self.value,
            self.note,
            getattr(self._category, 'id', self.category_id)
        )

    async def get_category(self):
        if self._category:
            return self._category

        self._category = await Category.get(self.category_id)
        return self._category

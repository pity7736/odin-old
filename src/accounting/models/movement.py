from enum import Enum

from src.accounting.models import Category
from src.db.fields import Field, ForeignKeyField, DateField
from src.db.models import Model


class MovementTypeEnum(Enum):
    EXPENSE = 'expense'
    INCOME = 'income'


class Movement(Model):
    __table_name__ = 'movements'
    id = Field(name='id')
    type = Field(name='type')
    date = DateField(name='date')
    value = Field(name='value')
    note = Field(name='note')
    category = ForeignKeyField(name='category', to=Category)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tags = []

    @classmethod
    async def all_expenses(cls):
        return await cls.filter('expense')

    @classmethod
    async def filter(cls, type=None):
        con = await cls._get_connection()
        expenses = await con.fetch('select * from movements where type = $1', type)
        await con.close()
        result = []
        for expense in expenses:
            result.append(cls(
                id=expense['id'],
                type=expense['type'],
                date=expense['date'],
                value=expense['value'],
                note=expense['note'],
                category_id=expense['category_id']
            ))
        return result

    async def get_category(self):
        if self.category:
            return self.category

        self.category = await Category.get(id=self.category_id)
        return self.category

    async def add_tags(self, *tags):
        con = await self._get_connection()
        values = [(tag.id, self.id) for tag in tags]
        await con.copy_records_to_table(
            'movements_tags',
            records=values,
            columns=('tag_id', 'movement_id')
        )
        self._tags.extend(tags)

    @property
    def tags(self):
        return self._tags

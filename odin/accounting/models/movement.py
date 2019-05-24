from enum import Enum

from gideon.fields import CharField, IntegerField, DateField, ForeignKeyField
from gideon.models import Model

from odin.accounting.models import Category


class MovementTypeEnum(Enum):
    EXPENSE = 'expense'
    INCOME = 'income'


class Movement(Model):
    __table_name__ = 'movements'
    _type = CharField(name='type')
    _date = DateField(name='date')
    _value = IntegerField(name='value')
    _note = CharField(name='note')
    _category = ForeignKeyField(name='category', to=Category)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tags = []

    @classmethod
    async def all_expenses(cls):
        return await cls.filter(type='expense')

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

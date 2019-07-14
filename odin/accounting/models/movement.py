from enum import Enum
from typing import List

from gideon.fields import CharField, IntegerField, DateField, ForeignKeyField
from gideon.models import Model

from .category import Category
from .event import Event
from .tag import Tag
from .wallet import Wallet


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
    _wallet = ForeignKeyField(name='wallet', to=Wallet)
    _event = ForeignKeyField(name='event', to=Event)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tags: List[Tag] = []

    @classmethod
    async def all_expenses(cls) -> List['Movement']:
        return await cls.filter(type='expense')

    async def get_category_(self) -> Category:
        if self.category:
            return self.category

        self.category = await Category.get(id=self.category_id)
        return self.category

    async def get_wallet_(self) -> Wallet:
        if self.wallet:
            return self.wallet

        self.wallet = await Wallet.get(id=self.wallet_id)
        return self.wallet

    async def get_event_(self) -> Event:
        if self.event:
            return self.event

        self.event = await Event.get(id=self.event_id)
        return self.event

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
    def tags(self) -> List[Tag]:
        return self._tags

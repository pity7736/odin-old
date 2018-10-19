import datetime

from pytest import mark

from src.db.fields import Field
from src.db.models import Model


class ChildModel(Model):
    __table_name__ = 'test_model'
    id = Field(name='id')
    name = Field(name='name')
    date = Field(name='date')
    note = Field(name='note')


@mark.asyncio
async def test_save_with_attribute_as_params(create_db, db_transaction, connection):
    instance = ChildModel(
        name='test model',
        date=datetime.date.today(),
        note='test note of model'
    )
    await instance.save()

    record = await connection.fetchrow(
        'select * from test_model where id = $1',
        instance.id
    )

    assert instance.id == record['id']
    assert instance.name == record['name']
    assert instance.note == record['note']
    assert instance.date == record['date']

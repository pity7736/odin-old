import datetime

from pytest import mark, raises

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


@mark.asyncio
async def test_filter_by_name(create_db, db_transaction):
    child_data = (
        ('name 1', datetime.date.today(), 'note 1'),
        ('name 2', datetime.date.today(), 'note 2'),
        ('name 3', datetime.date.today(), 'note 3'),
        ('name 4', datetime.date.today(), 'note 4'),
    )
    for data in child_data:
        child = ChildModel(name=data[0], date=data[1], note=data[2])
        await child.save()

    records = await ChildModel.filter(name='name 1')
    record = records[0]

    assert len(records) == 1
    assert record.name == 'name 1'
    assert record.date == datetime.date.today()
    assert record.note == 'note 1'


@mark.asyncio
async def test_filter_by_name_and_note(create_db, db_transaction):
    child_data = (
        ('name 1', datetime.date.today(), 'note 1'),
        ('name 2', datetime.date.today(), 'note 2'),
        ('name 3', datetime.date.today(), 'note 3'),
        ('name 4', datetime.date.today(), 'note 4'),
    )
    for data in child_data:
        child = ChildModel(name=data[0], date=data[1], note=data[2])
        await child.save()

    records = await ChildModel.filter(name='name 1', note='note 1')
    record = records[0]

    assert len(records) == 1
    assert record.name == 'name 1'
    assert record.date == datetime.date.today()
    assert record.note == 'note 1'


@mark.asyncio
async def test_filter_by_date_instance_returning_many(create_db, db_transaction):
    child_data = (
        ('name 1', datetime.date.today(), 'note 1'),
        ('name 2', datetime.date.today(), 'note 2'),
        ('name 3', datetime.date.today(), 'note 3'),
        ('name 4', datetime.date.today(), 'note 4'),
    )
    for data in child_data:
        child = ChildModel(name=data[0], date=data[1], note=data[2])
        await child.save()

    records = await ChildModel.filter(date=datetime.date.today())

    assert len(records) == 4


@mark.asyncio
async def test_filter_without_arguments():
    with raises(AssertionError):
        await ChildModel.filter()

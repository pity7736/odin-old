import datetime

import asyncpg
from asyncpg import NotNullViolationError
from pytest import mark, raises

from src import settings
from src.accounting.models import Movement
from tests.factories import TagFactory


@mark.asyncio
async def test_save_with_category_instance(create_db, db_transaction, category):
    movement = Movement(type='expense', date=datetime.date.today(), value=10000, category=category)
    await movement.save()

    con = await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME
    )
    record = await con.fetchrow(
        'select * from movements where id = $1',
        movement.id
    )
    await con.close()

    assert movement.id == record['id']
    assert movement.type == record['type']
    assert movement.date == datetime.date.today()
    assert movement.value == record['value']
    assert movement.category_id == record['category_id']


@mark.asyncio
async def test_save_with_category_id(create_db, db_transaction, category):
    movement = Movement(type='expense', date=datetime.date.today(), value=10000, category_id=category.id)
    await movement.save()
    con = await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME
    )
    record = await con.fetchrow(
        'select * from movements where id = $1',
        movement.id
    )
    await con.close()

    assert movement.id == record['id']
    assert movement.type == record['type']
    assert movement.date == datetime.date.today()
    assert movement.value == record['value']
    assert movement.category_id == record['category_id']


@mark.asyncio
async def test_save_without_category(create_db):
    movement = Movement(type='expense', date=datetime.date.today(), value=10000)
    with raises(NotNullViolationError):
        await movement.save()


@mark.asyncio
async def test_save_with_isoformat_date(create_db, db_transaction, category):
    movement = Movement(type='expense', date='2018-10-18', value=10000, category=category)
    await movement.save()

    assert isinstance(movement.date, datetime.date)
    assert str(movement.date) == '2018-10-18'


@mark.asyncio
async def test_save_with_not_isoformat_date(create_db, db_transaction, category):
    movement = Movement(type='expense', date='18-10-2018', value=10000, category=category)
    with raises(ValueError):
        await movement.save()


@mark.asyncio
async def test_add_one_tag_to_movement(create_db, db_transaction, movement):
    tag = TagFactory()
    await tag.save()
    await movement.add_tags(tag)

    con = await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME
    )
    record = await con.fetchrow(
        'select * from movements_tags where movement_id = $1 and tag_id = $2',
        movement.id,
        tag.id
    )
    await con.close()

    assert movement.tags[0] == tag
    assert record


@mark.asyncio
async def test_add_two_tags_to_movement(create_db, db_transaction, movement):
    tags = TagFactory.create_batch(2)
    for t in tags:
        await t.save()

    await movement.add_tags(*tags)

    con = await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME
    )
    records = await con.fetch(
        'select * from movements_tags where movement_id = $1',
        movement.id
    )
    await con.close()

    assert len(records) == 2


@mark.asyncio
async def test_get_category_with_movement_category_instance(create_db, db_transaction, category):
    movement = Movement(type='expense', date='18-10-2018', value=10000, category=category)
    mov_category = await movement.get_category()

    assert mov_category == category


@mark.asyncio
async def test_get_category_with_movement_category_id(create_db, db_transaction, category):
    movement = Movement(type='expense', date='18-10-2018', value=10000, category_id=category.id)
    mov_category = await movement.get_category()

    assert mov_category != category
    assert mov_category.id == category.id

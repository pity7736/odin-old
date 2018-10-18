import datetime

from asyncpg import NotNullViolationError
from pytest import mark, raises

from src.accounting.models import Movement


@mark.asyncio
async def test_save_with_category_instance(create_db, db_transaction, category):
    movement = Movement(type='expense', date=datetime.date.today(), value=10000, category=category)

    assert movement.id is None
    await movement.save()
    mov_category = await movement.get_category()

    assert movement.id is not None
    assert mov_category == category


@mark.asyncio
async def test_save_with_category_id(create_db, db_transaction, category):
    movement = Movement(type='expense', date=datetime.date.today(), value=10000, category_id=category.id)
    await movement.save()
    mov_category = await movement.get_category()

    assert mov_category.id == category.id


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

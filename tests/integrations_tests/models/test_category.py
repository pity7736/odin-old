from asyncpg import NotNullViolationError
from pytest import mark, raises

from src.accounting.models import Category


@mark.asyncio
async def test_save_returning_id(create_db, event_loop):
    category = Category(name='test name', description='test description')
    assert category.id is None
    await category.save()
    assert category.id is not None


@mark.asyncio
async def test_save_without_description(create_db, event_loop):
    category = Category(name='test', description='')
    with raises(NotNullViolationError):
        await category.save()

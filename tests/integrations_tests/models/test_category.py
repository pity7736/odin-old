from asyncpg import NotNullViolationError
from pytest import mark, raises

from src.accounting.models import Category
from tests.factories import CategoryFactory


@mark.asyncio
async def test_save_returning_id(create_db, db_transaction):
    category = CategoryFactory(name='test name', description='test description')
    assert category.id is None
    await category.save()
    assert category.id is not None


@mark.asyncio
async def test_save_without_description():
    category = Category(name='test')
    with raises(NotNullViolationError):
        await category.save()


@mark.asyncio
async def test_filter_by_name_without_categories(create_db, db_transaction):
    categories = await Category.filter(name='test name')
    assert categories == []


@mark.asyncio
async def test_filter_by_id(create_db, db_transaction):
    fixture = CategoryFactory(name='qwerty')
    await fixture.save()
    categories = await Category.filter(id=fixture.id)
    category = categories[0]

    assert category.id == fixture.id
    assert category.name == 'qwerty'


@mark.asyncio
async def test_filter_by_description(create_db, db_transaction):
    fixture = CategoryFactory()
    await fixture.save()

    categories = await Category.filter(description='test description')
    category = categories[0]

    assert category.id == fixture.id
    assert category.description == 'test description'


@mark.asyncio
async def test_filter_without_params(create_db, db_transaction):
    fixture = CategoryFactory()
    await fixture.save()

    with raises(AssertionError):
        await Category.filter()

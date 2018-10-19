import asyncpg
from asyncpg import NotNullViolationError
from pytest import mark, raises

from src import settings
from src.accounting.models import Category
from tests.factories import CategoryFactory


@mark.asyncio
async def test_save(create_db, db_transaction):
    category = CategoryFactory(id=None, name='test name', description='test description')
    await category.save()
    con = await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME
    )
    record = await con.fetchrow(
        'select * from categories where id = $1',
        category.id
    )
    await con.close()

    assert category.id == record['id']
    assert category.name == record['name']
    assert category.description == record['description']


@mark.asyncio
async def test_save_without_description():
    category = Category(name='test')
    with raises(NotNullViolationError):
        await category.save()


@mark.asyncio
async def test_filter_by_name_with_not_existing_categories(create_db, db_transaction):
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

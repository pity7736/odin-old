from asyncpg import NotNullViolationError
from pytest import mark, raises

from src.accounting.models import Category
from tests.factories import CategoryFactory


@mark.asyncio
async def test_save(create_db, db_transaction, connection):
    category = CategoryFactory(id=None, name='test name', description='test description')
    await category.save()
    record = await connection.fetchrow(
        'select * from categories where id = $1',
        category.id
    )

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


@mark.asyncio
async def test_get_by_id(create_db, db_transaction, category):
    record = await Category.get(id=category.id)

    assert record != category
    assert record.id == category.id
    assert record.name == category.name
    assert record.description == category.description


@mark.asyncio
async def test_get_by_name(create_db, db_transaction, category):
    record = await Category.get(name=category.name)

    assert record != category
    assert record.id == category.id
    assert record.name == category.name
    assert record.description == category.description


@mark.asyncio
async def test_get_by_id_and_name(create_db, db_transaction, category):
    record = await Category.get(id=category.id, name=category.name)

    assert record != category
    assert record.id == category.id
    assert record.name == category.name
    assert record.description == category.description
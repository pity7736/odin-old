from asyncpg import NotNullViolationError
from pytest import mark, raises

from src.accounting.models import SubCategory
from tests.factories import CategoryFactory


@mark.asyncio
async def test_save_with_category_instance(create_db, db_transaction):
    category = CategoryFactory()
    await category.save()

    subcategory = SubCategory(name='test sub', category=category)
    assert subcategory.id is None
    await subcategory.save()
    assert subcategory.id is not None


@mark.asyncio
async def test_save_with_category_id(create_db, db_transaction):
    category = CategoryFactory()
    await category.save()

    subcategory = SubCategory(name='test sub', category_id=category.id)
    assert subcategory.id is None
    await subcategory.save()
    assert subcategory.id is not None


@mark.asyncio
async def test_save_without_category(create_db):
    subcategory = SubCategory(name='test sub')
    with raises(NotNullViolationError):
        await subcategory.save()

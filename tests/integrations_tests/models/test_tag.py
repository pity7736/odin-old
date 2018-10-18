from pytest import mark

from src.accounting.models import Tag


@mark.asyncio
async def test_save(create_db, db_transaction):
    tag = Tag(name='test tag')
    assert tag.id is None
    await tag.save()
    assert tag.id is not None


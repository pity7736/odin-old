import asyncpg
from pytest import mark

from src import settings
from src.accounting.models import Tag


@mark.asyncio
async def test_save(create_db, db_transaction):
    tag = Tag(name='test tag')
    await tag.save()
    con = await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME
    )
    record = await con.fetchrow(
        'select * from tags where id = $1',
        tag.id
    )
    await con.close()

    assert tag.id == record['id']
    assert tag.name == record['name']

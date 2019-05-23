from pytest import mark

from odin.accounting.models import Tag


@mark.asyncio
async def test_save(create_db, db_transaction, connection):
    tag = Tag(name='test tag')
    await tag.save()
    record = await connection.fetchrow(
        'select * from tags where id = $1',
        tag.id
    )

    assert tag.id == record['id']
    assert tag.name == record['name']

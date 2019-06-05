import subprocess

import asyncpg
from pytest import fixture

from odin import settings
from tests.factories import CategoryFactory, MovementFactory, WalletFactory


@fixture(scope='session')
def create_db():
    print('creating database...')
    sql_file = f'{settings.ROOT_DIR}/create_db.sql'
    subprocess.call(['psql', '-U', settings.DB_USER, '-h', settings.DB_HOST, '-f', sql_file])


@fixture
async def connection():
    con = await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME
    )
    yield con
    await con.close()


@fixture
async def db_transaction(connection):
    # TODO: refactor this for a better solution
    yield
    await connection.execute('TRUNCATE categories, movements_tags, tags, movements;')
    await connection.close()


@fixture
async def category():
    cat = CategoryFactory()
    await cat.save()
    return cat


@fixture
async def wallet():
    w = WalletFactory()
    await w.save()
    return w


@fixture
async def movement(category, wallet):
    mov = MovementFactory(category=category, wallet=wallet)
    await mov.save()
    return mov

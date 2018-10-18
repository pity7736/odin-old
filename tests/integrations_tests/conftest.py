import subprocess

import asyncpg
from pytest import fixture

from src import settings


@fixture(scope='session')
def create_db():
    print('creating database...')
    sql_file = f'{settings.ROOT_DIR}/create_db.sql'
    subprocess.call(['psql', '-U', settings.DB_USER, '-h', settings.DB_HOST, '-f', sql_file])


@fixture()
async def db_transaction():
    # TODO: refactor this for a better solution
    yield
    connection = await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME
    )
    await connection.execute('TRUNCATE categories, subcategories;')

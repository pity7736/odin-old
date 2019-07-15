from multiprocessing import Process
import subprocess

import asyncpg
import boto3
import uvicorn
from pytest import fixture

from odin import settings, app
from odin.settings import DYNAMODB_USER_CREDENTIALS_TABLE, DYNAMODB_HOST, DYNAMODB_TOKEN_TABLE
from tests.factories import CategoryFactory, MovementFactory, WalletFactory, EventFactory


@fixture(scope='session')
def create_db():
    print('creating database...')
    sql_file = f'{settings.ROOT_DIR}/create_db.sql'
    subprocess.call(['psql', '-U', settings.DB_USER, '-h', settings.DB_HOST, '-f', sql_file])


@fixture(scope='session')
def server():
    process = Process(
        target=uvicorn.run,
        daemon=False,
        name='test_server',
        kwargs={
            'app': app,
            'host': '0.0.0.0',
            'port': 8889,
        },
    )
    process.start()
    print(f'running test server...')
    yield
    print('stopping test server...')
    process.kill()


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
    await connection.execute('TRUNCATE categories, movements_tags, tags, movements, wallets, events, users;')
    await connection.close()
    dynamodb = boto3.resource('dynamodb', endpoint_url=DYNAMODB_HOST)
    table = dynamodb.Table(DYNAMODB_USER_CREDENTIALS_TABLE)
    items = table.scan()['Items']
    for item in items:
        table.delete_item(Key={'email': item['email']})

    table = dynamodb.Table(DYNAMODB_TOKEN_TABLE)
    items = table.scan()['Items']
    for item in items:
        table.delete_item(Key={'value': item['value']})


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
async def event():
    e = EventFactory()
    await e.save()
    return e


@fixture
async def movement(category, wallet):
    mov = MovementFactory.build(category=category, wallet=wallet)
    print('mov', mov)
    await mov.save()
    print('mov', mov)
    return mov

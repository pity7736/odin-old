import asyncio

from graphene.test import Client
from graphql.execution.executors.asyncio import AsyncioExecutor
from pytest import fixture
import uvloop

from odin.api import schema
from tests.factories import UserFactory


@fixture(scope='session')
def event_loop():
    print('creating loop')
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    print('closing loop')
    loop.close()


@fixture
def graph_client(event_loop):
    return Client(schema=schema, executor=AsyncioExecutor(loop=event_loop))


@fixture
def valid_password():
    return 'Th1s is a valid Pa$sword'


@fixture
def graphql_context():
    class Request:
        user = UserFactory.build()

    return {
        'request': Request()
    }

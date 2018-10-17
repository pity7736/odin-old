import asyncio

import uvloop
from pytest import fixture


@fixture
def event_loop():
    print('creating loop')
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    print('closing loop')
    loop.close()

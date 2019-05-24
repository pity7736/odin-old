from graphql.execution.executors.asyncio import AsyncioExecutor
from sanic import Sanic
from sanic.response import json
from sanic_graphql import GraphQLView

from .schema import schema


app = Sanic()


@app.listener('before_server_start')
def init_graphql(app, loop):
    app.add_route(
        GraphQLView.as_view(
            schema=schema,
            executor=AsyncioExecutor(loop=loop),
            graphiql=True
        ),
        '/api/'
    )


@app.route('/')
async def root(request):
    return json({'hello': 'world'})

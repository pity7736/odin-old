from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from starlette.responses import UJSONResponse

from .schema import schema


app = Starlette(debug=True)
app.add_route('/api/', GraphQLApp(schema=schema, executor_class=AsyncioExecutor))


@app.route('/')
async def root(request):
    return UJSONResponse({'hello': 'world!'})

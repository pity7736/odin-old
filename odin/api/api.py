from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import UJSONResponse

from odin.auth.backend import OdinAuthBackend
from .schema import schema


def on_error(conn, exec):
    return UJSONResponse({'authentication error': str(exec)})


app = Starlette(debug=True)
app.add_middleware(AuthenticationMiddleware, backend=OdinAuthBackend(), on_error=on_error)
app.add_route('/api/', GraphQLApp(schema=schema, executor_class=AsyncioExecutor))


@app.route('/')
async def root(request):
    return UJSONResponse({'hello': 'world!'})

from graphql import graphql
from graphql.execution.executors.asyncio import AsyncioExecutor
from pytest import mark
import requests

from odin.api import schema
from tests.factories import UserFactory


@mark.asyncio
async def test_success(create_db, db_transaction, valid_password, server):
    user = UserFactory.build()
    await user.set_password(valid_password)
    await user.save()
    mutation = f'''
        mutation {{
            login(email: "{user._email}", password: "{valid_password}") {{
                token
                message
            }}
        }}
    '''
    result = await graphql(schema, mutation, executor=AsyncioExecutor(), return_promise=True)
    query = '''
        query {
          categories {
            name
            description
          }
        }
    '''
    response = requests.post(
        'http://localhost:8889/api/',
        json={'query': query},
        headers={
            'Authorization': f'Token {result.data["login"]["token"]}',
            'Content-type': 'application/json'
        }
    )
    assert response.json() == {
        "data": {
            "categories": []
        },
        "errors": None
    }


@mark.asyncio
async def test_invalid_token(create_db, db_transaction, valid_password, server):
    user = UserFactory.build()
    await user.set_password(valid_password)
    await user.save()
    query = '''
        query {
          categories {
            name
            description
          }
        }
    '''
    response = requests.post(
        'http://localhost:8889/api/',
        json={'query': query},
        headers={
            'Authorization': f'Token anytoken',
            'Content-type': 'application/json'
        }
    )
    assert response.json() == {'authentication error': 'invalid token!'}

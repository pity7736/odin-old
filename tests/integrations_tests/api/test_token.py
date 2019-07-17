import datetime

from freezegun import freeze_time
from graphql import graphql
from graphql.execution.executors.asyncio import AsyncioExecutor
from pytest import mark
import requests

from odin.api import schema
from odin.settings import TOKEN_EXPIRATION_MINUTES_DELTA
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
async def test_non_exists_token(create_db, db_transaction, valid_password, server):
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
    assert response.json() == {'authentication error': 'invalid token'}


@freeze_time(str(datetime.datetime.now() - datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES_DELTA)))
@mark.asyncio
async def test_expired_token(create_db, db_transaction, valid_password, server):
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
    print(response.content)
    assert response.json() == {'authentication error': 'token expired'}


@freeze_time(str(datetime.datetime.now() - datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES_DELTA - 1)))
@mark.asyncio
async def test_valid_token(create_db, db_transaction, valid_password, server):
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

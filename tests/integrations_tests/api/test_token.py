import datetime

import ujson

from odin.auth.models import Token
from odin.settings import TOKEN_EXPIRATION_MINUTES_DELTA
from odin.utils.crypto import AES256, get_random_string


def token_fixture(user, loop, minutes_expired=0):
    aes = AES256()
    data = ujson.dumps({
        'user_id': user.id,
        'created_at': (datetime.datetime.now() - datetime.timedelta(minutes=minutes_expired)).isoformat(),
        'data': get_random_string()
    })
    token = Token(
        value=aes.encrypt(data=data),
        iv=aes.iv,
        key=aes.key
    )
    loop.run_until_complete(token.save())
    return token.value


def test_success(create_db, db_transaction, user_fixture, test_client_fixture, event_loop):
    token = token_fixture(user=user_fixture, loop=event_loop)
    query = '''
        query {
          categories {
            name
            description
          }
        }
    '''
    response = test_client_fixture.post(
        'http://localhost:8889/api/',
        json={'query': query},
        headers={
            'Authorization': f'Bearer {token}',
            'Content-type': 'application/json'
        }
    )
    assert response.json() == {
        "data": {
            "categories": []
        },
        "errors": None
    }


def test_non_exists_token(create_db, db_transaction, test_client_fixture):
    query = '''
        query {
          categories {
            name
            description
          }
        }
    '''
    response = test_client_fixture.post(
        'http://localhost:8889/api/',
        json={'query': query},
        headers={
            'Authorization': f'Bearer anytoken',
            'Content-type': 'application/json'
        }
    )
    assert response.json() == {'authentication error': 'invalid token'}


def test_expired_token(create_db, db_transaction, user_fixture, test_client_fixture, event_loop):
    token = token_fixture(user=user_fixture, loop=event_loop, minutes_expired=TOKEN_EXPIRATION_MINUTES_DELTA)
    query = '''
        query {
          categories {
            name
            description
          }
        }
    '''
    response = test_client_fixture.post(
        'http://localhost:8889/api/',
        json={'query': query},
        headers={
            'Authorization': f'Bearer {token}',
            'Content-type': 'application/json'
        }
    )
    assert response.json() == {'authentication error': 'token expired'}


def test_valid_token(create_db, db_transaction, user_fixture, event_loop, test_client_fixture):
    token = token_fixture(user=user_fixture, loop=event_loop, minutes_expired=TOKEN_EXPIRATION_MINUTES_DELTA - 1)
    query = '''
        query {
          categories {
            name
            description
          }
        }
    '''
    response = test_client_fixture.post(
        'http://localhost:8889/api/',
        json={'query': query},
        headers={
            'Authorization': f'Bearer {token}',
            'Content-type': 'application/json'
        }
    )
    assert response.json() == {
        "data": {
            "categories": []
        },
        "errors": None
    }


def test_bearer_token(create_db, db_transaction, user_fixture, event_loop, test_client_fixture):
    token = token_fixture(user=user_fixture, loop=event_loop)
    query = '''
        query {
          categories {
            name
            description
          }
        }
    '''
    response = test_client_fixture.post(
        'http://localhost:8889/api/',
        json={'query': query},
        headers={
            'Authorization': f'Token {token}',
            'Content-type': 'application/json'
        }
    )
    assert response.json() == {'authentication error': 'invalid token'}


def test_wrong_format_token(create_db, db_transaction, user_fixture, event_loop, test_client_fixture):
    token = token_fixture(user=user_fixture, loop=event_loop)
    query = '''
        query {
          categories {
            name
            description
          }
        }
    '''
    response = test_client_fixture.post(
        'http://localhost:8889/api/',
        json={'query': query},
        headers={
            'Authorization': f'Bearer token {token}',
            'Content-type': 'application/json'
        }
    )
    assert response.json() == {'authentication error': 'invalid token'}

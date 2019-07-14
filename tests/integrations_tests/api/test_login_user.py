from graphql import graphql
from graphql.execution.executors.asyncio import AsyncioExecutor
from pytest import mark

from odin.api import schema
from tests.factories import UserFactory


@mark.asyncio
async def test_success_login_user(create_db, db_transaction, valid_password):
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

    assert result.data['login']['token']
    assert result.data['login']['message'] == 'login successfully'
    assert result.errors is None


@mark.asyncio
async def test_fail_login_user(create_db, db_transaction, valid_password):
    user = UserFactory.build()
    await user.set_password(valid_password)
    await user.save()
    mutation = f'''
        mutation {{
            login(email: "{user._email}", password: "wrong password") {{
                token
                message
            }}
        }}
    '''
    result = await graphql(schema, mutation, executor=AsyncioExecutor(), return_promise=True)

    assert result.data['login']['token'] is None
    assert result.data['login']['message'] == 'email or password are wrong'


@mark.asyncio
async def test_login_non_existent_user(create_db, db_transaction, valid_password):
    email = 'pity7736@gmail.com'
    mutation = f'''
        mutation {{
            login(email: "{email}", password: "wrong password") {{
                token
                message
            }}
        }}
    '''
    result = await graphql(schema, mutation, executor=AsyncioExecutor(), return_promise=True)

    assert result.data['login']['token'] is None
    assert result.data['login']['message'] == f'Does not exists an user with email: {email}'

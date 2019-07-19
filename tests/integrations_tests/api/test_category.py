from graphql import graphql
from graphql.execution.executors.asyncio import AsyncioExecutor
from pytest import mark

from odin.api import schema
from tests.factories import CategoryFactory


def test_query_existing_category(create_db, db_transaction, category, graph_client, graphql_context_fixture):
    query = f'''
        query {{
            category(id: {category.id}) {{
                name
                description
            }}
        }}
    '''
    result = graph_client.execute(query, context=graphql_context_fixture)

    assert result == {
        'data': {
            'category': {
                'name': 'test name',
                'description': 'test description'
            }
        }
    }


def test_query_non_existent_category(create_db, graph_client, graphql_context_fixture):
    query = '''
        query {
            category(id: 1) {
                name
                id
                description
            }
        }
    '''
    result = graph_client.execute(query, context=graphql_context_fixture)

    assert result == {
        'data': {
            'category': None
        }
    }


def test_category_mutation(create_db, db_transaction, graph_client, graphql_context_fixture):
    mutation = '''
        mutation {
            createCategory(name: "test category mutation", description: "test description") {
                category {
                    name
                    description
                }
            }
        }
    '''
    result = graph_client.execute(mutation, context=graphql_context_fixture)

    assert result == {
        'data': {
            'createCategory': {
                'category': {
                    'name': 'test category mutation',
                    'description': 'test description'
                }
            }
        }
    }


@mark.asyncio
async def test_query_all_categories(create_db, db_transaction, graphql_context_fixture):
    categories = CategoryFactory.create_batch(5)
    for i, category in enumerate(categories):
        category.name = f'name {i}'
        await category.save()

    query = '''
        query {
            categories {
                name
            }
        }
    '''

    result = await graphql(schema, query, executor=AsyncioExecutor(), return_promise=True,
                           context=graphql_context_fixture)
    assert result.data == {
        'categories': [
            {
                'name': 'name 0'
            },
            {
                'name': 'name 1'
            },
            {
                'name': 'name 2'
            },
            {
                'name': 'name 3'
            },
            {
                'name': 'name 4'
            }
        ]
    }

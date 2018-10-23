
def test_query_existing_category(create_db, db_transaction, category, graph_client):
    query = f'''
        query {{
            category(id: {category.id}) {{
                name
                description
            }}
        }}
    '''
    result = graph_client.execute(query)

    assert result == {
        'data': {
            'category': {
                'name': 'test name',
                'description': 'test description'
            }
        }
    }


def test_query_non_existent_category(create_db, graph_client):
    query = '''
        query {
            category(id: 1) {
                name
                id
                description
            }
        }
    '''
    result = graph_client.execute(query)

    assert result == {
        'data': {
            'category': None
        }
    }


def test_category_mutation(create_db, db_transaction, graph_client):
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
    result = graph_client.execute(mutation)

    assert result == {
        'data': {
            'createCategory':{
                'category': {
                    'name': 'test category mutation',
                    'description': 'test description'
                }
            }
        }
    }

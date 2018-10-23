import datetime


def test_query_movement(create_db, db_transaction, movement, graph_client):
    query = f'''
        query {{
            movement(id: {movement.id}) {{
                id
                type
                date
                value
                note
            }}
        }}
    '''
    result = graph_client.execute(query)

    assert result == {
        'data': {
            'movement': {
                'id': 1,
                'type': 'EXPENSE',
                'date': datetime.date.today().isoformat(),
                'value': 10000,
                'note': 'note'
            }
        }
    }


def test_query_non_existent_movement(create_db, graph_client):
    query = '''
        query {
            movement(id: 1) {
                id
                type
                date
                value
                note
            }
        }
    '''
    result = graph_client.execute(query)

    assert result == {
        'data': {
            'movement': None
        }
    }


def test_query_movement_with_category(create_db, db_transaction, movement, graph_client):
    query = f'''
        query {{
            movement(id: {movement.id}) {{
                type
                date
                value
                note
                category {{
                    name
                    description
                }}
            }}
        }}
    '''
    result = graph_client.execute(query)

    assert result == {
        'data': {
            'movement': {
                'type': 'EXPENSE',
                'date': datetime.date.today().isoformat(),
                'value': 10000,
                'note': 'note',
                'category': {
                    'name': 'test name',
                    'description': 'test description'
                }
            }
        }
    }


def test_movement_mutation(create_db, db_transaction, graph_client, category):
    mutation = f'''
        mutation {{
            createMovement(data: {{
                    type: EXPENSE,
                    date: "{datetime.date.today()}",
                    value: 20000,
                    note: "test",
                    categoryId: {category.id}
                }}) {{
                movement {{
                    type
                    date
                    value
                    note
                    category {{
                        id
                        name
                        description
                    }}
                }}
            }}
        }}
    '''
    result = graph_client.execute(mutation)

    assert result == {
        'data': {
            'createMovement': {
                'movement': {
                    'type': 'EXPENSE',
                    'date': str(datetime.date.today()),
                    'value': 20000,
                    'note': 'test',
                    'category': {
                        'id': category.id,
                        'name': category.name,
                        'description': category.description
                    }
                }
            }
        }
    }

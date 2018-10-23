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
                id
                type
                date
                value
                note
                category {{
                    name
                    id
                    description
                }}
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
                'note': 'note',
                'category': {
                    'name': 'test name',
                    'id': 1,
                    'description': 'test description'
                }
            }
        }
    }

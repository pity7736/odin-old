
def test_query_event(event, graph_client, graphql_context_fixture):
    query = f'''
        query {{
            event(id: {event.id}) {{
                id
                name
                initDate
                endDate
            }}
        }}
    '''
    result = graph_client.execute(query, context=graphql_context_fixture)

    assert result == {
        'data': {
            'event': {
                'id': event.id,
                'name': event.name,
                'initDate': event.init_date.isoformat(),
                'endDate': event.end_date.isoformat()
            }
        }
    }

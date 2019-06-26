from pytest import mark

from odin.utils.crypto import pbkdf2


vectors = (
    (
        {
            'password': b'hello world',
            'salt': b'test',
            'hash_name': 'sha512',
            'iterations': 100_000
        },
        '57d2fb14237c675235478a98ca7608fc44115d89102a316e2281f6e13b9644f8'
        'eca7a74dc6fc7b00c718d1061dc067cfe8c107e16ed4adf26f38f615ae7c2ad5'
    ),
    (
        {
            'password': b'hello world',
            'salt': b'test',
        },
        '88ad75039d9e564e62af3c7757a7356f7c1d6e43f51c6a618de1c50e05a9294b'
        '4823720e5bbf41b5f20b2ebeb45413d67556a4b7e601efc48a472c5cb482c25f'
    ),
    (
        {
            'password': 'hello world',
            'salt': 'test',
        },
        '88ad75039d9e564e62af3c7757a7356f7c1d6e43f51c6a618de1c50e05a9294b'
        '4823720e5bbf41b5f20b2ebeb45413d67556a4b7e601efc48a472c5cb482c25f'
    ),
    (
        {
            'password': b'hello world',
            'salt': b'test',
            'hash_name': 'sha1',
            'iterations': 1000
        },
        'e0f225d3d4d3a04a82cfc39cebf2a3237781d844290ae178f76f4829208e101e'
        '2c4b52103aacf040e3cac482aa43848424a956846cd5312c1645e25c452dcaf9'
    )
)


@mark.parametrize('params, expected_result', vectors)
def test_hash(params, expected_result):
    result = pbkdf2(**params)
    assert result.hex() == expected_result

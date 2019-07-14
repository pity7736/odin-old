from odin.auth.utils import make_password


def test_make_password(valid_password):
    password, salt = make_password(raw_password=valid_password, salt='test')
    assert password == 'sha512$200000$lYIU8uVSWAyTnJjbA8K6pUEHuyD/rtTqrC2gF' \
                       '8b7eo6knLa209aZn0JhTOxLxTV+8y/icyDyJFZpvVHQdy9roA=='
    assert salt == 'test'


def test_random_salt_length(valid_password):
    password, salt = make_password(raw_password=valid_password)

    assert len(salt) == 32

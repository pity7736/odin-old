from odin.auth.utils import make_password


def test_make_password():
    password = make_password(raw_password='Th1s is a Pa$sword', salt='test')
    assert password == 'test$sha512$200000$J5Za93zpx6imqOXST9Gn8JupUukV8wVG0tvvkkpUlIi1SR' \
                       'SX2YELwIoQQBMvxb7wYmNQV4IwojPNn3IDoR5U9g=='

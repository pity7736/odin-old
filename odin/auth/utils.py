import base64

from odin.utils.crypto import pbkdf2, get_random_string


def make_password(raw_password, salt=None):
    salt = salt or get_random_string()
    hashed = pbkdf2(password=raw_password, salt=salt)
    encoded = base64.b64encode(hashed)
    return f'{salt}$sha512$100000${encoded.decode()}'

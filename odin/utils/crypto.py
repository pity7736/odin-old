import hashlib
import secrets
import string
from typing import Union


def pbkdf2(password: Union[str, bytes],
           salt: Union[str, bytes],
           hash_name: str = 'sha512',
           iterations: int = 200_000) -> bytes:

    if isinstance(password, str):
        password = password.encode('utf-8')

    if isinstance(salt, str):
        salt = salt.encode('utf-8')

    return hashlib.pbkdf2_hmac(
        hash_name=hash_name,
        password=password,
        salt=salt,
        iterations=iterations,
        dklen=64
    )


def get_random_string(length=16, allowed_chars=None):
    allowed_chars = allowed_chars or string.ascii_letters + string.digits
    return ''.join(secrets.choice(allowed_chars) for _ in range(length))

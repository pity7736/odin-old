import base64
import hashlib
import secrets
import string
from typing import Union, Optional

from Crypto.Cipher import AES


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


class AES256:

    _block_size = 16
    _mode = AES.MODE_CBC

    def __init__(self, key: Optional[str] = None, iv: Optional[str] = None):
        self._key = key
        self._iv = iv

    def encrypt(self, data: str) -> str:
        padded_data = data + (self._block_size - len(data) % self._block_size) * \
                      chr(self._block_size - len(data) % self._block_size)
        cipher = AES.new(key=self.key, IV=self.iv, mode=self._mode)
        return base64.b64encode(cipher.encrypt(padded_data)).decode()

    @property
    def key(self) -> str:
        self._key = self._key or get_random_string(length=32)
        return self._key

    @property
    def iv(self) -> str:
        self._iv = self._iv or get_random_string()
        return self._iv

    def decrypt(self, data: str) -> str:
        cipher = AES.new(key=self._key, IV=self._iv, mode=self._mode)
        padded_data = cipher.decrypt(base64.b64decode(data)).decode()
        return padded_data[:-ord(padded_data[len(padded_data) - 1:])]

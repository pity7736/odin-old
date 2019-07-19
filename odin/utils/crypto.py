import base64
import hashlib
import secrets
import string
from typing import Union, Optional

from Cryptodome.Cipher import AES

from odin.exceptions import AESKeyError


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
    _key_length = 32

    def __init__(self, key: Optional[str] = None, iv: Optional[str] = None):
        if key:
            assert len(key) == self._key_length

        if iv:
            assert len(iv) == 16

        self._key = key
        self._iv = iv

    def encrypt(self, data: str) -> str:
        length_missing = self._block_size - len(data) % self._block_size
        padded_data = data + length_missing * chr(length_missing)
        cipher = AES.new(key=self.key.encode(), iv=self.iv.encode(), mode=self._mode)
        return base64.b64encode(cipher.encrypt(padded_data.encode())).decode()

    @property
    def key(self) -> str:
        self._key = self._key or get_random_string(length=self._key_length)
        return self._key

    @property
    def iv(self) -> str:
        self._iv = self._iv or get_random_string()
        return self._iv

    def decrypt(self, data: str) -> str:
        cipher = AES.new(key=self._key.encode(), iv=self._iv.encode(), mode=self._mode)
        try:
            padded_data = cipher.decrypt(base64.b64decode(data)).decode()
        except UnicodeDecodeError:
            raise AESKeyError('wrong key')
        return padded_data[:-ord(padded_data[len(padded_data) - 1:])]

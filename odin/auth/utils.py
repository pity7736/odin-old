import base64
from typing import Tuple, Union, Optional

from odin.utils.crypto import pbkdf2, get_random_string


def make_password(raw_password: Union[str, bytes], salt: Optional[Union[str, bytes]] = None) -> Tuple[str, str]:
    salt = salt or get_random_string(length=32)
    hashed = pbkdf2(password=raw_password, salt=salt)
    encoded = base64.b64encode(hashed)
    return f'sha512$200000${encoded.decode()}', salt

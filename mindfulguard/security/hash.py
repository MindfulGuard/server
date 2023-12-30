import hashlib
from typing import Literal


class Hash:
    def sha(
        self,
        value: bytes | str,
        encode: Literal['utf-8', 'ascii'] = 'utf-8',
        length: Literal['256', '512'] = '256'
    ):
        if isinstance(value, bytes):
            return self.__sha256(value, length).digest()
        elif isinstance(value, str):
            if length == '256':
                return self.__sha256(value.encode(encode)).hexdigest()
        else:
            raise TypeError("Unsupported type for value")

    def __sha256(self, value: bytes, length: Literal['256', '512'] = '256'):
        if length == '256':
            return hashlib.sha256(value)
        else:
            raise ValueError("Unsupported length")
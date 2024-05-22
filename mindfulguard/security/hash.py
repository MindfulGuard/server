import hashlib
from typing import Literal
from loguru import logger

class Hash:
    def sha(
        self,
        value: bytes | str,
        encode: Literal['utf-8', 'ascii'] = 'utf-8',
        length: Literal['256', '512'] = '256'
    ):
        logger.debug("Calculating hash...")
        if isinstance(value, bytes):
            hash_value = self.__sha256(value, length).digest()
            logger.info("Hash calculated successfully.")
            return hash_value
        elif isinstance(value, str):
            logger.debug("Converting string to bytes...")
            if length == '256':
                encoded_value = value.encode(encode)
                logger.debug("Encoded string: {}", encoded_value)
                hash_value = self.__sha256(encoded_value).hexdigest()
                logger.info("Hash calculated successfully.")
                return hash_value
            else:
                logger.error("Unsupported hash length requested.")
                raise ValueError("Unsupported length")
        else:
            logger.error("Unsupported type for value.")
            raise TypeError("Unsupported type for value")

    def __sha256(self, value: bytes, length: Literal['256', '512'] = '256'):
        logger.debug("Using SHA-256 algorithm...")
        if length == '256':
            logger.info("Calculating SHA-256 hash...")
            return hashlib.sha256(value)
        else:
            logger.error("Unsupported length requested.")
            raise ValueError("Unsupported length")

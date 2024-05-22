import random
import pyotp
from loguru import logger

from mindfulguard.validation import Validation


class Totp:
    def __init__(self, secret_code: str) -> None:
        self.__secret_code = secret_code

    def generate_secret_code(self) -> str:
        logger.info("Generating secret code...")
        secret_code = pyotp.random_base32()
        logger.info("Secret code generated successfully.")
        return secret_code
    
    def generate_backup_codes(self, number_of_backup_codes: int = 6) -> list[int]:
        logger.info("Generating backup codes...")
        backup_codes = [random.randint(100000, 999999) for _ in range(number_of_backup_codes)]
        logger.info("Backup codes generated successfully.")
        return backup_codes
    
    def get(self) -> str:
        logger.debug("Generating TOTP...")
        totp = pyotp.TOTP(self.__secret_code)
        code = totp.now()
        logger.info("TOTP generated successfully.")
        return code
    
    def verify(self, code: str) -> bool:
        logger.debug("Verifying TOTP...")
        totp = pyotp.TOTP(self.__secret_code)
        verification_result = totp.verify(code)
        if verification_result:
            logger.info("TOTP verification successful.")
        else:
            logger.warning("TOTP verification failed.")
        return verification_result

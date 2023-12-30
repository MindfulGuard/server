import secrets
import string
from mindfulguard.security.hash import Hash
from mindfulguard.security.totp import Totp


class Security:
    def hash(self) -> Hash:
        return Hash()
    
    def totp(self, secret_code: str) -> Totp:
        return Totp(secret_code)

    def generate_string(self, length: int) -> str:
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
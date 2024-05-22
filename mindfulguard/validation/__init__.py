from loguru import logger
import json
import re
import uuid


class Validation:
    def is_login(self, login: str) -> bool:
        """
        Can only be present: hyphen, underscore, Latin characters only
        """
        result = bool(re.compile(r'^[A-Za-z0-9_-]{2,50}$').match(login))
        logger.debug("is_login called with login={}, result={}", login, result)
        return result
        
    def is_secret_string(self, secret_string: str) -> bool:
        result = len(secret_string) == 64
        logger.debug("is_secret_string called with secret_string={}, result={}", secret_string, result)
        return result
    
    def is_token(self, token: str) -> bool:
        result = len(token) == 128
        logger.debug("is_token called with token={}, result={}", token, result)
        return result
    
    def is_uuid(self, uuid_str: str) -> bool:
        try:
            uuid.UUID(str(uuid_str))
            result = True
        except ValueError:
            result = False
        logger.debug("is_uuid called with uuid_str={}, result={}", uuid_str, result)
        return result
        
    def is_description(self, text: str) -> bool:
        result = len(text) <= 200
        logger.debug("is_description called with text={}, result={}", text, result)
        return result

    def is_TOTP_code(self, code: str) -> bool:
        result = len(code) == 6 and code.isdigit()
        logger.debug("is_TOTP_code called with code={}, result={}", code, result)
        return result
    
    def is_device(self, text: str) -> bool:
        result = len(text) > 0 and len(text) <= 256
        logger.debug("is_device called with text={}, result={}", text, result)
        return result
    
    def is_json(self, json_string: str) -> bool:
        try:
            json.loads(json_string)
            result = True
        except ValueError:
            result = False
        logger.debug("is_json called with json_string={}, result={}", json_string, result)
        return result
        
    def is_ip(self, ip: str) -> bool:
        ipv4_pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        ipv6_pattern = r"^([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4})$"

        if not isinstance(ip, str):
            ip = str(ip)

        result = bool(re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip))
        logger.debug("is_ip called with ip={}, result={}", ip, result)
        return result
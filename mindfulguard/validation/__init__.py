import json
import re
import socket
import uuid


class Validation:
    def is_login(self, login: str) -> bool:
        """
        Can only be present: hyphen, underscore, Latin characters only
        """
        return bool(re.compile(r'^[A-Za-z0-9_-]{2,50}$').match(login))
        
    def is_secret_string(self, secret_string: str) -> bool:
        if len(secret_string) == 64:
            return True
        return False
    
    def is_token(self, token: str) -> bool:
        if len(token)==128:
            return True
        return False
    
    def is_uuid(self, uuid_str: str) -> bool:
        try:
            uuid.UUID(str(uuid_str))
            return True
        except ValueError:
            return False
        
    def is_description(self, text: str) -> bool:
        return len(text) <= 200

    def is_TOTP_code(self, code: str) -> bool:
        return len(code)==6 and code.isdigit() == True
    
    def is_device(self, text: str) -> bool:
        return len(text)>0 and len(text)<=256
    
    def is_json(self, json_string: str) -> bool:
        try:
            json.loads(json_string)
            return True
        except ValueError:
            return False
        
    def is_ip(self, ip: str) -> bool:
        ipv4_pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        ipv6_pattern = r"^([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4})$"

        if not isinstance(ip, str):
            ip = str(ip)

        if re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip):
            return True
        else:
            return False
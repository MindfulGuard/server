import re
import secrets
import uuid

from fastapi import Request

import mypass.core.configuration as configuration


class Validation:
    def validate_login(self,login:str)->bool:
        """
        Can only be present: hyphen, underscore, Latin characters only
        """
        config = configuration.ServerConfiguration()
        length = configuration.Authentication(config).public().lengths().get_login_length()
        return bool(re.compile(r'^[A-Za-z0-9_-]{2,'+str(length)+'}$').match(login))

    def validate_email(self,email:str)->bool:
        """
        2 ≤ email ≤ 320
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,320}$'# Maximum address length according to RFC 5321 standard
        
        if re.match(email_pattern, email):
            config = configuration.ServerConfiguration()
            banned_domains:list[str] = configuration.Authentication(config).get_blocked_domains()
            
            domain = email.split('@')[1]
            
            if domain in banned_domains:
                return False
            else:
                return True
        else:
            return False
        
    def validate_secret_string(self,secret_string:str)->bool:
        if len(secret_string) == 128 or len(secret_string) == 64 or len(secret_string) == 32:
            return True
        return False
    
    def validate_token(self,token:str):
        if len(token)==128:
            return True
        return False
    
    def validate_is_uuid(self,uuid_str:str)->bool:
        try:
            uuid_obj = uuid.UUID(uuid_str)
            return str(uuid_obj) == uuid_str
        except ValueError:
            return False

def get_client_ip(request: Request) -> str:
    # Let's try to get the IP from the X-Real-IP header
    client_ip = request.headers.get("x-real-ip")
    
    if client_ip is not None:
        return client_ip
    
    # If the header is not set, we use remote_addr directly
    return request.client.host

def arguments(*args)->bool:
    for i in args:
        if i == None:
            return False
    return True

def minutes_to_seconds(minutes:int):
    return minutes * 30
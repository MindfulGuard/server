import re
import secrets

import mypass.core.configuration as configuration


class Validation:
    def __validate_login(self,login:str)->bool:
        """
        Can only be present: hyphen, underscore, Latin characters only
        """
        config = configuration.ServerConfiguration()
        length = configuration.Validation(config).get_login_length()
        return bool(re.compile(r'^[A-Za-z0-9_-]{2,'+str(length)+'}$').match(login))
    def __validte_password(self,password:str)->bool:
        """
        (?=.*[A-Z]): At least one uppercase letter is required.\n
        (?=.*[a-z]): At least one lowercase letter is required.\n
        (?=.*\\d): At least one digit is required.\n
        (?=.*[@$!%*?&]): At least one of the specified special characters is required: @, $, !, %, *, ?, &.\n
        [ A-Za-z\\d@$!%*?&]{8,}: Only Latin characters (in any case), numbers and specified special characters are allowed. The password must be at least 8 characters long.
        """

        config = configuration.ServerConfiguration()
        length = configuration.Validation(config).get_password_length()
        return bool(re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,' + str(length) + '}$').match(password))

    def __validate_email(self,email:str)->bool:
        """
        2 ≤ email ≤ 320
        """
        # Регулярное выражение для проверки адреса электронной почты
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
    def validate(self,email:str)->bool:
        if self.__validate_email(email):
            return True
        else:
            return False
    
def generate_512_bit_token_string()->str:
    token_bytes = secrets.token_bytes(64)
    token_string = token_bytes.hex()
    return token_string

def arguments(*args)->bool:
    for i in args:
        if i == None:
            return False
    return True
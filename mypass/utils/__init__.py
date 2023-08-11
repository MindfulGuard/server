import re

from mypass.configuration.config import Configuration

def validate_email(email):
    """
    2 ≤ email ≤ 320

    """
    # Регулярное выражение для проверки адреса электронной почты
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Проверка длины адреса электронной почты
    if len(email) > 320:  # Maximum address length according to RFC 5321 standard
        return False
    
    if re.match(email_pattern, email):
        config = Configuration().server_configuration("auth","blocked_domains")
        banned_domains = config.split(',')
        
        domain = email.split('@')[1]
        
        if domain in banned_domains:
            return False
        else:
            return True
    else:
        return False

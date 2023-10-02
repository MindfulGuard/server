def get_authorization_token(authorization: str)->str:
        if authorization and authorization.startswith("Bearer "):
            return authorization.replace("Bearer ", "")
        return ""
from mypass import utils
from mypass.database.postgresql import authentication


class SignIn():
    async def execute(self,email:str,secret_string:bytes,device:str,ip:str):
        """
            Returns:
                -1 - registration is not allowed\n
                1 - user not was successful\n
                0 - the user already exists
        """
        valid = utils.Validation()
        token:str = utils.generate_512_bit_token_string()
        if valid.validate(email) == False:
            return -2
        elif await authentication.Authentication().sign_in(
            email,
            secret_string,
            token,
            device,
            ip
        ) == True:
            return token
        else:
            return 0
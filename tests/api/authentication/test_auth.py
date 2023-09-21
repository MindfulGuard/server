import re
import uuid
from tests.api.public.test_configuration import TestPublic
from tests.api.read_test_data import ReadTestData
from tests.api.secure import sha256s, totp_client
from tests.api.settings import *
from tests.api.validations import is_uuid


class TestAuthentication:
    def sign_up(self,login:str,secret_string:str):
        data = {
            "login": login,
            "secret_string": secret_string,
        }
        headers = get_headers("")
        print(data,headers)
        response = client.post(AUTH_PATH_V1+ "/sign_up", data=data, headers=headers)

        try:
            return (response.json()["secret_code"],response.json()["backup_codes"],response.status_code)
        except KeyError:
            return ("",[],response.status_code)
        
    def sign_in(self,login:str,secret_string:str,code:str,expiration:int,type:str):
        data = {
            "login": login,
            "secret_string": secret_string,
            "code": code,
            "expiration":expiration
        }
        headers = get_headers("")
        print(data,headers)
        response = client.post(AUTH_PATH_V1+ f"/sign_in?type={type}", data=data, headers=headers)
        try:
            return (response.json()["token"],response.status_code)
        except KeyError:
            return ("",response.status_code)


    def tests(self):
        test_data = ReadTestData()
        get_login = test_data.get_login()
        get_secret_string = test_data.get_secret_string()
        
        uuid = "ace2e062-0c44-4c82-b282-88dbd36d7731"

        login = []
        l_status_code = []

        secret_string = []
        s_status_code = []

        for i in range(0,len(get_login)):
            login.append(get_login[i][0])
            l_status_code.append(get_login[i][1]) 

            secret_string.append(get_secret_string[i][0])  
            s_status_code.append(get_secret_string[i][1])

        for i in range(0,len(login)):
            assert self.sign_up(
                                login[i],
                                self.__get_secret_string(
                                login[i],
                                secret_string[i],
                                uuid
                                ))[2] == l_status_code[i] and s_status_code[i]
            
            if l_status_code[i] == 200:
                assert self.sign_in(login[i],
                    self.__get_secret_string(
                        login[i],
                        secret_string[i],
                        uuid
                    ),
                    self.sign_up(
                        login[i],
                        self.__get_secret_string(
                        login[i],
                        secret_string[i],
                        uuid
                    ))[1][0],
                    76,
                    "backup"
                    )[1] == l_status_code[i]
                
                assert self.sign_in(
                    login[i],
                    self.__get_secret_string(
                        login[i],
                        secret_string[i],
                        uuid
                    ),
                    totp_client(
                    self.sign_up(
                        login[i],
                        self.__get_secret_string(
                        login[i],
                        secret_string[i],
                        uuid
                    ))[0]
                    ),
                    76,
                    "basic"
                    )[1] == l_status_code[i]
            
    def __get_salt(self,uuid:str)->str:
        salt  = uuid.replace("-", "")
        return salt

    def __get_secret_string(self,login:str,password:str,salt:str):
        password_rule = TestPublic().get_config()[0]
        pattern = re.compile(password_rule)
        match = bool(pattern.match(password))

        print(sha256s(f"{login}{password}{salt}"))

        if match == True and is_uuid(salt) == True and len(login) > 2:
            print("SECRET_STRING:",pattern,match,salt,"\n")
            return sha256s(f"{login}{password}{self.__get_salt(salt)}")
        return "NULL"
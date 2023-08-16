import asyncio
import unittest
import uuid
from mypass.authentication import *
from tests.security import *

class TestAuthMethods(unittest.TestCase):

    async def test_sign_up(self):
        email:str = 'rfe@efmail.com'
        
        private_key:bytes = uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da").bytes
        password:str = '12345'

        sign_up = SignUp()
        secure = Security()
        result = await sign_up.execute(email,secure.encrypt(email,password,private_key),secure.encrypt('niclknamef',password,private_key),'192.168.1.1')
        self.assertEqual(result, 1)
    def test_encryption(self):
        secure = Security()

        text = 'Hello'
        password = '12345'
        private_key = uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da").bytes

        encrypt = secure.encrypt(text,password,private_key)
        decrypt = secure.decrypt(encrypt,password,private_key)

        self.assertEqual(text, decrypt)
        
    async def test_sign_in(self):
        secure = Security()

        email:str = 'rfe@efmail.com'
        private_key:bytes = uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da").bytes
        password:str = '12345'
        secret_string = secure.encrypt(email,password,private_key)

        sign_in = SignIn()

        result = await sign_in.execute(email,secret_string,"Windows",'192.168.1.1')
        self.assertNotEqual(1,result)
        print(result)

    
test = TestAuthMethods()
asyncio.run(test.test_sign_in())
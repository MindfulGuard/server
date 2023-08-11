import uuid
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib


class Security:
    def __init__(self):
        self._iterations = 100000
    def encrypt(self,text:str,password:str,private_key:bytes)->bytes:
        """
        Args:
            text (str): the text that needs to be encrypted\n
            password (str)\n
            private_key (bytes): uuid.uuid4().bytes
        """

        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), private_key, self._iterations)
        
        # Generate a random IV
        iv = private_key
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
        
        # Return the IV along with the ciphertext
        return iv + ciphertext
    
    def decrypt(self,text:bytes,password:str,private_key:bytes)->str:

        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), private_key, self._iterations)
        
        iv = text[:AES.block_size]
        ciphertext = text[AES.block_size:]
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        return decrypted.decode('utf-8')

"""
# Ваш пароль и соль для PBKDF2
password = "your_password_here"
salt = get_random_bytes(16)

# Генерируем ключ с помощью PBKDF2
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

# Ваша строка для шифрования
data = "Hello nugets"

# Создание объекта AES для шифрования
cipher = AES.new(key, AES.MODE_CBC)

# Шифрование данных
cipher_text = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

# Добавление соли и IV к зашифрованным данным (не забудьте сохранить соль для дешифрования)
encrypted_data = salt + cipher.iv + cipher_text

# Дешифрование данных
cipher = AES.new(key, AES.MODE_CBC, iv=encrypted_data[16:32])  # Используем IV из зашифрованных данных
decrypted_data = unpad(cipher.decrypt(encrypted_data[32:]), AES.block_size)

print("Original Data:", data)
print("Decrypted Data:", decrypted_data.decode('utf-8'))
"""
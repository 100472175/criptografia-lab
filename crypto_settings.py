import base64
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

class CryptoSettings:
    def __init__(self):
        self.salt = os.urandom(16)
        self.length = 32
        self.n = 2 ** 14
        self.r = 8
        self.p = 1

    def encode(self, password: str):
        kdf = Scrypt(salt=self.salt, length=self.length, n=self.n, r=self.r, p=self.p)
        passwd = kdf.derive(password.encode())
        passwd = base64.b64encode(passwd)
        return passwd, self.salt

    def decode(self, contrasena, key, salt):
        key = base64.b64decode(key)
        kdf = Scrypt(salt=salt, length=self.length, n=self.n, r=self.r, p=self.p)
        return kdf.verify(contrasena.encode(), key)
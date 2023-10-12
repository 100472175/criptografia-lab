import base64
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


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

    def verify(self, contrasena, key, salt):
        key = base64.b64decode(key)
        kdf = Scrypt(salt=salt, length=self.length, n=self.n, r=self.r, p=self.p)
        return kdf.verify(contrasena.encode(), key)

KEY = base64.b64decode(b'43qDrljAC/3Qn3DfvKyMd0WifJlA5Lsd1E7AgyAUwwo=')



def check_ChaCha_id(dni):
    data = dni.encode()
    chacha = ChaCha20Poly1305(KEY)
    nonce = os.urandom(12)
    ct = chacha.encrypt(nonce, data, None)
    print(base64.b64encode(nonce), type(base64.b64encode(nonce)))
    print("########## DEBUG ##########")
    nonce2 = base64.b64decode(base64.b64encode(nonce))
    chacha2 = ChaCha20Poly1305(KEY)
    print("Paso por aqui")
    ct2 = chacha.decrypt(nonce, ct, None).decode()
    print(ct2)
    print("########## FIN DEBUG ##########")
    print(base64.b64encode(ct))
    return ct, base64.b64encode(nonce)

def decrypt_id(id):
    print("Esto es el id: ", id)
    from database_importer import execute_sql_command
    user = execute_sql_command('Select * from USER WHERE id = ?', (id,))
    print(user)
    nonce = base64.b64decode(user[0][6])
    chacha = ChaCha20Poly1305(KEY)
    print("Type of nonce:", type(nonce), len(nonce), nonce)
    print("Type of id:", type(id), len(id), id)
    print("fffffffffffffffffffffffffffffffffffffffffff")
    ct = chacha.decrypt(nonce, id, None)
    return ct.decode()


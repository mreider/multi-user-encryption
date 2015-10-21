# -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import AES
from Crypto import Random
from uuid import uuid4


def generate_key():
    return str(uuid4()).replace('-', '')


class Encrypter:
    """
    Class handling all encryption/decryption related methods.
    """
    BS = 16

    def pad(self, s):
        return s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def __init__(self, key):
        self.key = key

    def encrypt(self, unencrypted):
        unencrypted = self.pad(unencrypted)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(unencrypted))

    def decrypt(self, encrypted):
        enc = base64.b64decode(encrypted)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))


if __name__ == '__main__':
    content = '898e6d0eacce4fbfac976dbdc29e30b0'
    en1 = Encrypter('08724a9cd8ef4cd3b08d27682c6fc58a')
    encrypted1 = en1.encrypt(content)
    print 'Encrypted 1 %s'%encrypted1

    en2 = Encrypter('56ec26e8958145ab975e574e72cfb1a3')
    encrypted2 = en2.encrypt(content)
    print 'Encrypted 2 %s'%encrypted2



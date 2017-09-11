#-*-coding:utf8-*-
'''
random_generator = Random.new().read
rsa = RSA.generate(1024, random_generator)
prikey = rsa.exportKey()
pubkey = rsa.publickey().exportKey()
'''
import base64
import bcrypt
from Crypto import Random 
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5 
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5 
from Crypto.PublicKey import RSA

prikey = '''-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQC8QEybkn8CYcYYkUbVFLgtiHrVmnE1IRJm5hDdWbr9LAL6Oogq
lQ3YIZgUZWjHvHbeP9uU1koVrPYrAdV9Vm7eyoQM5wKv9mNpBb8NGXWyXL4dg3F5
+3ZiVC9aTy7KOnBEHR9X2HMpq4K+mgXa55FibBp9e8nxoD9DMft3PUQLGQIDAQAB
AoGAfYr8C/xEy5fc/mFUNaJdua/9Cxq2SNJHbWwc7yF6PIDvc2U5jfxdgTfWLjP7
Dsk3FLzNeZL3UUFJ4iCU+cN8p95wuUpXG/2hIdJPxtV16bnUx5oA6FPmmHQEbadH
/odgRMWHkFUruJ2vnyQVX4xdAJqz7dYHGsFxQW4Bq7Q0QqkCQQDPp3Z6ye9zYF/3
PgHlz2iJUG015GYYnFtSuAr9yfV7VlCVN5mXZ+VnvAmRST8i6uck+Qz1LngoVY2Z
VeBDRysjAkEA6BRi0EMqFGtJg4whfMqYyLfkfLAUPptmGgDIdfITV2wR7noGUXe1
13YVCY3Dh3km5idaL63fo+m9SRAW17ACkwJAW1D1VUIAPuieywdFpl3zRo9Lt2td
Sm1X66RrkPeDMF3gyf3NWTujMl8Khg2D6kMKqsOq4xcwV+xnfIq7OFrPqQJBAIXQ
m1kyIOU9J1ouRnDJ8GZrgddTP5kJyUldAjjfp79UlNJIkbQPrk3ZzC+CCifm90Ll
ld7ABp9ger/SAxnCZvkCQDQe+mPdHl/0Mp8ZnDlj8SbtmTMZmOZ/bVXiBN8ZLLn2
DIfLwC7yYz3HJR0PWOcGG7piHQShlpN105/aYE6VgaM=
-----END RSA PRIVATE KEY-----'''

pubkey = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC8QEybkn8CYcYYkUbVFLgtiHrV
mnE1IRJm5hDdWbr9LAL6OogqlQ3YIZgUZWjHvHbeP9uU1koVrPYrAdV9Vm7eyoQM
5wKv9mNpBb8NGXWyXL4dg3F5+3ZiVC9aTy7KOnBEHR9X2HMpq4K+mgXa55FibBp9
e8nxoD9DMft3PUQLGQIDAQAB
-----END PUBLIC KEY-----'''


def encrypt(message):
    message = message.encode('utf-8')
    cipher_text = bcrypt.hashpw(message, bcrypt.gensalt())
    return cipher_text

def decrypt(message):
    random_generator =  Random.new().read
    rsakey = RSA.importKey(prikey)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = cipher.decrypt(base64.b64decode(message), random_generator)
    return cipher_text

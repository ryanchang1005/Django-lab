from base64 import b64decode, b64encode
from binascii import Error as binasciiError
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA


def rsa_import_key_pem(file_path):
    rsa_object = RSA.import_key(open(file_path, 'r').read())
    return rsa_object


rsa_pub_key = rsa_import_key_pem('pub.pem')
rsa_pri_key = rsa_import_key_pem('pri.pem')


def en(text):
    cipher = Cipher_pkcs1_v1_5.new(rsa_pub_key)
    cipher_text = cipher.encrypt(text.encode())
    return b64encode(cipher_text).decode()


def de(text):
    try:
        cipher_text = b64decode(text)
    except binasciiError:
        return ''
    else:
        cipher = Cipher_pkcs1_v1_5.new(rsa_pri_key)
        try:
            message = cipher.decrypt(cipher_text, None)
        except ValueError:
            return ''
        else:
            return message.decode() if message else ''


def sign(text):
    msg_hash = SHA256.new(b64encode(text.encode()))
    return b64encode(Signature_pkcs1_v1_5.new(rsa_pri_key).sign(msg_hash))


def verify(text_hash, signature):
    try:
        return Signature_pkcs1_v1_5.new(rsa_pub_key).verify(text_hash, b64decode(signature))
    except (ValueError, TypeError):
        return False


t = 'abc'
e = en(t)
d = de(e)

print(t)
print(e)
print(d)
print('---')

s = sign(t)
msg = SHA256.new(b64encode(t.encode()))
v = verify(msg, s)
print(t)
print(s)
print(msg)
print(v)
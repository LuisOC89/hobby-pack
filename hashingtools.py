import hashlib
import random
import string

def making_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])

def make_password_hashing(password, salt=None):
    if not salt:
        salt = making_salt()
    hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{0},{1}'.format(hash, salt)

def checking_password_hash(password, hash):
    salt = hash.split(',')[1]
    if make_password_hashing(password, salt) == hash:
        return True
    return False
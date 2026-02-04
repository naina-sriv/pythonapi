from pwdlib import PasswordHash
pwd_hash=PasswordHash.recommended()


def hash(password):
    return pwd_hash.hash(password)

def verify(hashedpwd,password):
    return pwd_hash.verify(hashedpwd,password)
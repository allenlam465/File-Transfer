#hash and salt a password
import hashlib
import crypt
password = "password123"
salt = crypt.mksalt(crypt.METHOD_SHA512)
hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()
print (password)
print (hashed_password)

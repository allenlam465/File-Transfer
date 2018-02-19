#hash and salt a password
import hashlib, uuid
salt = uuid.uuid4().hex
hashed_password = hashlib.sha512(password + salt).hexdigest()

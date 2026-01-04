from passlib.context import CryptContext
import hashlib

pass_context = CryptContext(schemes=["argon2"],deprecated="auto") # bcrypt allows only 72 bytes long (argon2_cffi)

def hash_password(password:str):
    sha256_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pass_context.hash(sha256_hash)

def verify_password(plain_password:str, hashed_password: str):
    sha256_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return pass_context.verify(sha256_hash,hashed_password)

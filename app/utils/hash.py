from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return bcrypt_context.encrypt(password)


def verify_password(password, hashed):
    return bcrypt_context.verify(password, hashed)

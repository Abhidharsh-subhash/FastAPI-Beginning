from passlib.context import CryptContext

# schemes=["bcrypt"] specifies the algorith used for password hashing
# deprecated="auto" will automatically handle deprecated schemes based on a predefined policy
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)
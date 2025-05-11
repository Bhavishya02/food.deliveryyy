from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed_password = pwd_context.hash("test123")
print("Hashed Password:", hashed_password)

is_verified = pwd_context.verify("test123", hashed_password)
print("Password Verified:", is_verified)

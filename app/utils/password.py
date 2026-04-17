from passlib.context import CryptContext

# 创建密码上下文，使用sha256_crypt算法，没有72字节的限制
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# 哈希密码
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

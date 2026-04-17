from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.password import get_password_hash, verify_password
from app.utils.jwt import create_access_token
from typing import Optional

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        """
        创建新用户
        :param user_data: 用户数据
        :return: 创建的用户
        """
        # 检查用户名是否已存在
        existing_user = self.db.query(User).filter(
            (User.username == user_data.username) |
            (User.email == user_data.email) |
            (User.phone == user_data.phone)
        ).first()
        
        if existing_user:
            raise ValueError("用户名、邮箱或手机号已存在")
        
        # 检查密码长度
        if len(user_data.password) > 72:
            raise ValueError("密码长度不能超过72个字符")
        
        # 创建新用户
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            phone=user_data.phone,
            hashed_password=hashed_password
        )
        
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        
        return new_user
    
    def authenticate_user(self, user_login: UserLogin) -> Optional[User]:
        """
        验证用户身份
        :param user_login: 登录信息
        :return: 验证通过的用户
        """
        # 查找用户
        user = self.db.query(User).filter(User.username == user_login.username).first()
        
        if not user:
            return None
        
        # 验证密码
        if not verify_password(user_login.password, user.hashed_password):
            return None
        
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        根据ID获取用户
        :param user_id: 用户ID
        :return: 用户信息
        """
        return self.db.query(User).filter(User.id == user_id).first()

# 创建用户服务工厂
def get_user_service(db: Session) -> UserService:
    return UserService(db)

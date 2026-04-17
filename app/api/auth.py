from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.schemas.user import UserCreate, UserLogin, Token, User
from app.services.user_service import get_user_service, UserService
from app.utils.jwt import create_access_token

router = APIRouter()

@router.post("/register", response_model=User)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册
    """
    user_service = get_user_service(db)
    try:
        user = user_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录
    """
    user_service = get_user_service(db)
    user = user_service.authenticate_user(user_login)
    
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

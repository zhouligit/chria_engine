from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.schemas.user import UserCreate, UserLogin, Token, User
from app.services.user_service import get_user_service, UserService
from app.utils.jwt import create_access_token, verify_token

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

@router.get("/me", response_model=User)
def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    获取当前用户信息
    """
    # 从请求头中获取令牌
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="未提供认证令牌")
    
    # 提取令牌（去掉Bearer前缀）
    if token.startswith("Bearer "):
        token = token[7:]
    
    # 验证令牌
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的认证令牌")
    
    # 获取用户ID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="无效的认证令牌")
    
    # 获取用户信息
    user_service = get_user_service(db)
    user = user_service.get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return user

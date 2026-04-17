from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.schemas.product import Product, ProductPurchase, OrderResponse, ProductContent, PaymentCreate, PaymentResponse
from app.services.product_service import get_product_service, ProductService
from app.utils.jwt import verify_token
import time
from typing import List

router = APIRouter()

def get_current_user_id(request: Request) -> int:
    """
    从请求头中获取当前用户ID
    """
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="未提供认证令牌")
    
    if token.startswith("Bearer "):
        token = token[7:]
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的认证令牌")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="无效的认证令牌")
    
    return int(user_id)

@router.get("/", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):
    """
    获取产品列表
    """
    product_service = get_product_service(db)
    products = product_service.get_products()
    return products

@router.post("/purchase", response_model=OrderResponse)
def purchase_product(product_purchase: ProductPurchase, request: Request, db: Session = Depends(get_db)):
    """
    购买产品
    """
    # 获取用户ID
    user_id = get_current_user_id(request)
    
    product_service = get_product_service(db)
    order = product_service.create_order(user_id, product_purchase)
    return order

@router.post("/payment", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, request: Request, db: Session = Depends(get_db)):
    """
    创建支付（Mock）
    """
    # 获取用户ID
    user_id = get_current_user_id(request)
    
    # Mock支付处理
    payment_response = {
        "payment_id": f"pay_{user_id}_{int(time.time())}",
        "status": "success",
        "message": "支付成功（Mock）",
        "order_id": payment.order_id,
        "amount": payment.amount
    }
    
    return payment_response

@router.get("/content/{product_id}", response_model=ProductContent)
def get_product_content(product_id: str, request: Request, db: Session = Depends(get_db)):
    """
    获取产品内容
    """
    # 获取用户ID
    user_id = get_current_user_id(request)
    
    product_service = get_product_service(db)
    content = product_service.get_product_content(user_id, product_id)
    
    if not content:
        raise HTTPException(status_code=404, detail="产品内容不存在或未购买")
    
    return content

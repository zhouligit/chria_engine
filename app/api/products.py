from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.schemas.product import Product, ProductPurchase, OrderResponse, ProductContent
from app.services.product_service import get_product_service, ProductService
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):
    """
    获取产品列表
    """
    product_service = get_product_service(db)
    products = product_service.get_products()
    return products

@router.post("/purchase", response_model=OrderResponse)
def purchase_product(product_purchase: ProductPurchase, db: Session = Depends(get_db)):
    """
    购买产品
    """
    # 模拟用户ID（实际应该从认证中获取）
    user_id = 1
    
    product_service = get_product_service(db)
    order = product_service.create_order(user_id, product_purchase)
    return order

@router.get("/content/{product_id}", response_model=ProductContent)
def get_product_content(product_id: str, db: Session = Depends(get_db)):
    """
    获取产品内容
    """
    # 模拟用户ID（实际应该从认证中获取）
    user_id = 1
    
    product_service = get_product_service(db)
    content = product_service.get_product_content(user_id, product_id)
    
    if not content:
        raise HTTPException(status_code=404, detail="产品内容不存在或未购买")
    
    return content

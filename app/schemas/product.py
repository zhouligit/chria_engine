from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    id: str
    name: str
    price: float
    description: str

class Product(ProductBase):
    features: List[str]

class ProductPurchase(BaseModel):
    product_id: str

class OrderResponse(BaseModel):
    id: int
    product_id: str
    product_name: str
    price: float
    status: str
    created_at: datetime

class ProductContent(BaseModel):
    title: str
    content: dict

class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    payment_method: str = "alipay"

class PaymentResponse(BaseModel):
    payment_id: str
    status: str
    message: str
    order_id: int
    amount: float

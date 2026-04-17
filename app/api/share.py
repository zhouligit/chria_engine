from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from pydantic import BaseModel
from typing import Dict
import hashlib
import time

router = APIRouter()

class ShareGenerate(BaseModel):
    user_id: int
    product_id: str

@router.post("/generate", response_model=Dict)
def generate_share_link(share: ShareGenerate):
    """
    生成分享链接
    """
    # 生成唯一的分享码
    share_code = hashlib.md5(f"{share.user_id}_{share.product_id}_{time.time()}".encode()).hexdigest()
    
    # 生成分享链接
    share_link = f"https://example.com/share/{share_code}"
    
    return {
        "share_code": share_code,
        "share_link": share_link,
        "expires_at": time.time() + 7 * 24 * 3600  # 7天过期
    }

@router.get("/process/{share_code}", response_model=Dict)
def process_share(share_code: str, db: Session = Depends(get_db)):
    """
    处理分享
    """
    # 模拟处理分享逻辑
    # 实际应该从数据库中查询分享信息
    
    return {
        "share_code": share_code,
        "status": "success",
        "message": "分享处理成功",
        "rewards": [
            "获得改判申请书5元优惠券",
            "获得1次同案犯匹配资格"
        ]
    }

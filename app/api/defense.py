from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.ai_service import ai_service
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class ProjectInfo(BaseModel):
    name: str
    industry: str
    business_model: str

class DefenseSubmit(BaseModel):
    question: str
    defense: str
    style: str = "vc"

@router.post("/question", response_model=Dict)
def get_defense_question(project_info: ProjectInfo):
    """
    获取AI质疑问题
    """
    # 获取AI质疑问题
    question = ai_service.get_defense_question(project_info.dict())
    return question

@router.post("/submit", response_model=Dict)
def submit_defense(defense: DefenseSubmit):
    """
    提交辩护
    """
    # 验证风格是否合法
    if defense.style not in ["vc", "cto", "operation"]:
        raise HTTPException(status_code=400, detail="风格不存在")
    
    # 获取AI回应
    response = ai_service.get_defense_response(defense.question, defense.defense, defense.style)
    return response

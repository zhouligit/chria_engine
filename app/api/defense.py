from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.ai_service import ai_service
from app.schemas.submission import SubmissionCreate
from app.services.submission_service import get_submission_service, SubmissionService
from app.utils.jwt import verify_token
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class ProjectInfo(BaseModel):
    name: str
    industry: str
    description: str

class DefenseSubmit(BaseModel):
    question_id: str
    response: str
    style: str = "vc"

@router.post("/question", response_model=Dict)
def get_defense_question(project_info: ProjectInfo):
    """
    获取AI质疑问题
    """
    # 获取AI质疑问题
    question = ai_service.get_defense_question(project_info.dict())
    return question

def get_current_user_id(request: Request) -> int:
    """
    从请求头中获取当前用户ID
    """
    token = request.headers.get("Authorization")
    if not token:
        return None
    
    if token.startswith("Bearer "):
        token = token[7:]
    
    payload = verify_token(token)
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    return int(user_id)

@router.post("/submit", response_model=Dict)
def submit_defense(defense: DefenseSubmit, request: Request, db: Session = Depends(get_db)):
    """
    提交辩护
    """
    # 验证风格是否合法
    if defense.style not in ["vc", "cto", "operation"]:
        raise HTTPException(status_code=400, detail="风格不存在")
    
    # 获取AI回应
    response = ai_service.get_defense_response(defense.question_id, defense.response, defense.style)
    
    # 构建结果
    result = {
        "question_id": defense.question_id,
        "response": defense.response,
        "style": defense.style,
        "response": response
    }
    
    # 尝试获取用户ID并存储提交记录
    user_id = get_current_user_id(request)
    if user_id:
        submission_service = get_submission_service(db)
        submission_data = SubmissionCreate(
            module_type="defense",
            module_id="general",
            answers={"question_id": defense.question_id, "response": defense.response, "style": defense.style},
            result=result
        )
        submission_service.create_submission(user_id, submission_data)
    
    return response

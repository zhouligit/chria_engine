from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
import json
from app.utils.database import get_db
from app.schemas.submission import Submission, SubmissionCreate
from app.services.submission_service import get_submission_service, SubmissionService
from app.utils.jwt import verify_token

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

@router.post("/", response_model=Submission)
def create_submission(
    submission_data: SubmissionCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    创建提交记录
    """
    user_id = get_current_user_id(request)
    submission_service = get_submission_service(db)
    
    submission = submission_service.create_submission(user_id, submission_data)
    return submission

@router.get("/", response_model=List[dict])
def get_submissions(
    module_type: str = None,
    limit: int = 100,
    request: Request = None,
    db: Session = Depends(get_db)
):
    """
    获取用户的提交记录
    """
    user_id = get_current_user_id(request)
    submission_service = get_submission_service(db)
    
    submissions = submission_service.get_submissions_by_user(user_id, module_type, limit)
    
    # 转换为字典列表
    result = []
    for submission in submissions:
        submission_dict = {
            "id": submission.id,
            "user_id": submission.user_id,
            "module_type": submission.module_type,
            "module_id": submission.module_id,
            "answers": submission.answers if submission.answers else [],
            "score": submission.score,
            "result": submission.result if submission.result else {},
            "created_at": submission.created_at
        }
        result.append(submission_dict)
    
    return result

@router.get("/{submission_id}", response_model=dict)
def get_submission(
    submission_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    获取提交记录详情
    """
    user_id = get_current_user_id(request)
    submission_service = get_submission_service(db)
    
    submission = submission_service.get_submission_by_id(submission_id, user_id)
    if not submission:
        raise HTTPException(status_code=404, detail="提交记录不存在")
    
    # 转换为字典
    submission_dict = {
        "id": submission.id,
        "user_id": submission.user_id,
        "module_type": submission.module_type,
        "module_id": submission.module_id,
        "answers": submission.answers if submission.answers else [],
        "score": submission.score,
        "result": submission.result if submission.result else {},
        "created_at": submission.created_at
    }
    
    return submission_dict

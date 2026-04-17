from sqlalchemy.orm import Session
from app.models.submission import Submission
from app.schemas.submission import SubmissionCreate
from typing import List
import json

class SubmissionService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_submission(self, user_id: int, submission_data: SubmissionCreate) -> Submission:
        """
        创建提交记录
        """
        # 将字典转换为JSON字符串
        answers_json = json.dumps(submission_data.answers)
        result_json = json.dumps(submission_data.result) if submission_data.result else None
        
        new_submission = Submission(
            user_id=user_id,
            module_type=submission_data.module_type,
            module_id=submission_data.module_id,
            answers=answers_json,
            score=submission_data.score,
            result=result_json
        )
        
        self.db.add(new_submission)
        self.db.commit()
        self.db.refresh(new_submission)
        
        return new_submission
    
    def get_submissions_by_user(self, user_id: int, module_type: str = None, limit: int = 100) -> List[Submission]:
        """
        获取用户的提交记录
        """
        query = self.db.query(Submission).filter(Submission.user_id == user_id)
        
        if module_type:
            query = query.filter(Submission.module_type == module_type)
        
        submissions = query.order_by(Submission.created_at.desc()).limit(limit).all()
        
        # 将JSON字符串转换为Python对象
        for submission in submissions:
            if submission.answers:
                submission.answers = json.loads(submission.answers)
            if submission.result:
                submission.result = json.loads(submission.result)
        
        return submissions
    
    def get_submission_by_id(self, submission_id: int, user_id: int) -> Submission:
        """
        根据ID获取提交记录
        """
        submission = self.db.query(Submission).filter(
            Submission.id == submission_id,
            Submission.user_id == user_id
        ).first()
        
        # 将JSON字符串转换为Python对象
        if submission:
            if submission.answers:
                submission.answers = json.loads(submission.answers)
            if submission.result:
                submission.result = json.loads(submission.result)
        
        return submission

def get_submission_service(db: Session):
    return SubmissionService(db)

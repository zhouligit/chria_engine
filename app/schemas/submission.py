from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List

class SubmissionBase(BaseModel):
    module_type: str
    module_id: str
    answers: List[Dict[str, Any]]
    score: Optional[int] = None
    result: Optional[Dict[str, Any]] = None

class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

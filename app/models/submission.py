from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.utils.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    module_type = Column(String(50), index=True)  # 题库、情景推演、辩护博弈
    module_id = Column(String(50), index=True)  # 题目ID、情景ID等
    answers = Column(Text)  # JSON格式的答案
    score = Column(Integer, nullable=True)  # 得分
    result = Column(Text, nullable=True)  # JSON格式的结果
    created_at = Column(DateTime(timezone=True), server_default=func.now())

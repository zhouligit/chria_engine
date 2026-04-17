from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.schemas.question import Question, QuestionSubmit, QuestionResult
import json
import os

router = APIRouter()

# 加载题库数据
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "questions.json")

if not os.path.exists(QUESTIONS_FILE):
    # 如果文件不存在，创建默认题库数据
    default_questions = {
        "version": "1.0",
        "description": "通用创业题库，用于评估用户创业潜力",
        "questions": [
            {
                "id": "q1",
                "category": "资金筹备",
                "question": "您的创业启动资金来源是什么？",
                "options": [
                    {"id": "q1a", "text": "个人积蓄", "score": 3},
                    {"id": "q1b", "text": "亲友借款", "score": 2},
                    {"id": "q1c", "text": "银行贷款", "score": 2},
                    {"id": "q1d", "text": "风险投资", "score": 4},
                    {"id": "q1e", "text": "还没有确定", "score": 0}
                ],
                "feedback": {
                    "low": "启动资金是创业的基础，建议您先明确资金来源再考虑创业。",
                    "medium": "您有一定的资金准备，但需要合理规划资金使用。",
                    "high": "您的资金来源较为可靠，为创业提供了有力保障。"
                }
            },
            {
                "id": "q2",
                "category": "市场分析",
                "question": "您对目标市场的了解程度如何？",
                "options": [
                    {"id": "q2a", "text": "非常了解，做过详细的市场调研", "score": 4},
                    {"id": "q2b", "text": "有一定了解，知道基本情况", "score": 2},
                    {"id": "q2c", "text": "了解不多，打算边做边学", "score": 1},
                    {"id": "q2d", "text": "不太了解，凭感觉进入", "score": 0}
                ],
                "feedback": {
                    "low": "市场分析是创业成功的关键，建议您在创业前做充分的市场调研。",
                    "medium": "您对市场有一定了解，但仍需进一步深入分析。",
                    "high": "您的市场调研工作做得很充分，为创业奠定了良好基础。"
                }
            }
        ],
        "scoring": {
            "totalScore": 8,
            "levels": [
                {"range": [0, 2], "level": "低潜力", "message": "您目前的创业条件还不够成熟，建议先积累经验和资源。"},
                {"range": [3, 4], "level": "中潜力", "message": "您有一定的创业潜力，但需要在多个方面进一步提升。"},
                {"range": [5, 6], "level": "高潜力", "message": "您的创业潜力较高，只要做好充分准备，成功的机会很大。"},
                {"range": [7, 8], "level": "极高潜力", "message": "您具备优秀的创业素质，只要把握好机会，很有可能取得成功。"}
            ]
        }
    }
    
    # 确保数据目录存在
    os.makedirs(os.path.dirname(QUESTIONS_FILE), exist_ok=True)
    
    # 写入默认数据
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(default_questions, f, ensure_ascii=False, indent=2)

# 读取题库数据
with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
    questions_data = json.load(f)

@router.get("/", response_model=list[Question])
def get_questions():
    """
    获取创业题库
    """
    return questions_data["questions"]

@router.post("/submit", response_model=QuestionResult)
def submit_answers(answers: QuestionSubmit):
    """
    提交答案
    """
    # 计算总分
    total_score = 0
    feedback = []
    
    for answer in answers.answers:
        # 查找对应的问题
        question = next((q for q in questions_data["questions"] if q["id"] == answer.question_id), None)
        if not question:
            raise HTTPException(status_code=400, detail=f"问题ID不存在: {answer.question_id}")
        
        # 检查选项ID是否为空
        if not answer.option_id:
            raise HTTPException(status_code=400, detail=f"问题 {answer.question_id} 未选择选项")
        
        # 查找对应的选项
        option = next((o for o in question["options"] if o["id"] == answer.option_id), None)
        if not option:
            raise HTTPException(status_code=400, detail=f"选项ID不存在: {answer.option_id}")
        
        # 累加分数
        total_score += option["score"]
        
        # 生成反馈
        if option["score"] <= 1:
            feedback.append({"question": question["question"], "feedback": question["feedback"]["low"]})
        elif option["score"] <= 2:
            feedback.append({"question": question["question"], "feedback": question["feedback"]["medium"]})
        else:
            feedback.append({"question": question["question"], "feedback": question["feedback"]["high"]})
    
    # 确定评估等级
    level = ""
    message = ""
    for lvl in questions_data["scoring"]["levels"]:
        if lvl["range"][0] <= total_score <= lvl["range"][1]:
            level = lvl["level"]
            message = lvl["message"]
            break
    
    return {
        "total_score": total_score,
        "level": level,
        "message": message,
        "feedback": feedback
    }

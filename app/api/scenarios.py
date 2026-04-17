from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.ai_service import ai_service
import json
import os
from typing import Dict, List

router = APIRouter()

# 加载情景推演数据
SCENARIOS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "scenarios.json")

if not os.path.exists(SCENARIOS_FILE):
    # 如果文件不存在，创建默认情景数据
    default_scenarios = {
        "version": "1.0",
        "description": "情景推演案例库，用于模拟创业过程中的挑战和风险",
        "industries": [
            {
                "id": "ecommerce",
                "name": "电商",
                "scenarios": [
                    {
                        "id": "ecommerce_1",
                        "title": "新电商平台的流量困境",
                        "description": "您创建了一个新的电商平台，专注于销售特色农产品。平台上线后，您发现流量非常少，用户转化率低。",
                        "challenges": [
                            "如何获取初始流量",
                            "如何提高用户转化率",
                            "如何与大型电商平台竞争"
                        ],
                        "risks": [
                            "烧钱买流量导致资金链断裂",
                            "产品同质化严重，缺乏竞争力",
                            "运营成本过高，入不敷出"
                        ],
                        "failurePaths": [
                            "持续烧钱买流量，最终资金耗尽",
                            "无法找到差异化竞争优势，被市场淘汰",
                            "运营管理不善，导致用户体验差"
                        ],
                        "options": [
                            {
                                "id": "e1a",
                                "text": "加大营销投入，通过社交媒体和KOL推广",
                                "outcome": "短期流量可能增加，但长期来看成本过高，难以持续。"
                            },
                            {
                                "id": "e1b",
                                "text": "专注于产品差异化，打造特色农产品品牌",
                                "outcome": "长期来看有潜力，但短期内可能增长缓慢。"
                            },
                            {
                                "id": "e1c",
                                "text": "与本地超市合作，线上线下结合",
                                "outcome": "可能会有稳定的客流，但增长空间有限。"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    # 确保数据目录存在
    os.makedirs(os.path.dirname(SCENARIOS_FILE), exist_ok=True)
    
    # 写入默认数据
    with open(SCENARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(default_scenarios, f, ensure_ascii=False, indent=2)

# 读取情景推演数据
with open(SCENARIOS_FILE, "r", encoding="utf-8") as f:
    scenarios_data = json.load(f)

@router.get("/", response_model=List[Dict])
def get_scenarios():
    """
    获取情景列表
    """
    all_scenarios = []
    for industry in scenarios_data["industries"]:
        for scenario in industry["scenarios"]:
            all_scenarios.append({
                "id": scenario["id"],
                "title": scenario["title"],
                "industry": industry["name"]
            })
    return all_scenarios

@router.get("/{id}", response_model=Dict)
def get_scenario(id: str):
    """
    获取情景详情
    """
    for industry in scenarios_data["industries"]:
        for scenario in industry["scenarios"]:
            if scenario["id"] == id:
                return scenario
    raise HTTPException(status_code=404, detail="情景不存在")

from pydantic import BaseModel

class ChoiceSubmit(BaseModel):
    scenario_id: str
    option_id: str
    style: str = "vc"

@router.post("/submit", response_model=Dict)
def submit_choice(choice: ChoiceSubmit):
    """
    提交选择
    """
    # 验证情景是否存在
    scenario = None
    for industry in scenarios_data["industries"]:
        for s in industry["scenarios"]:
            if s["id"] == choice.scenario_id:
                scenario = s
                break
        if scenario:
            break
    
    if not scenario:
        raise HTTPException(status_code=404, detail="情景不存在")
    
    # 验证选项是否存在
    option = next((o for o in scenario["options"] if o["id"] == choice.option_id), None)
    if not option:
        raise HTTPException(status_code=400, detail="选项不存在")
    
    # 验证风格是否合法
    if choice.style not in ["vc", "cto", "operation"]:
        raise HTTPException(status_code=400, detail="风格不存在")
    
    # 获取AI点评
    ai_comment = ai_service.get_ai_comment(choice.scenario_id, choice.option_id, choice.style)
    
    return {
        "scenario_id": choice.scenario_id,
        "option_id": choice.option_id,
        "option_text": option["text"],
        "outcome": option["outcome"],
        "ai_comment": ai_comment
    }

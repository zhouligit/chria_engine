import os
from dotenv import load_dotenv
from typing import Dict, List, Optional

# 加载环境变量
load_dotenv()

class AIService:
    def __init__(self):
        # 模拟AI API配置
        self.api_key = os.getenv("AI_API_KEY", "mock-api-key")
        self.api_url = os.getenv("AI_API_URL", "mock-api-url")
        self.model = os.getenv("AI_MODEL", "mock-model")
        
    def get_ai_comment(self, scenario_id: str, option_id: str, style: str) -> Dict:
        """
        获取AI点评
        :param scenario_id: 情景ID
        :param option_id: 选择的选项ID
        :param style: AI风格（vc, cto, operation）
        :return: AI点评内容
        """
        # 模拟AI点评
        mock_comments = {
            "e1a": {
                "vc": "烧钱买流量？你以为你是阿里巴巴啊？没有足够的资金储备，这就是自杀行为。",
                "cto": "技术上没问题，但你想过ROI吗？投100万进去能带来多少转化？",
                "operation": "KOL推广？现在KOL费用多高你知道吗？小品牌根本玩不起。"
            },
            "e1b": {
                "vc": "总算说了句人话，差异化是小电商的唯一出路。但你知道怎么做差异化吗？",
                "cto": "技术上支持，但需要时间和资源来打造品牌。",
                "operation": "方向对了，但执行起来没那么简单，需要专业的品牌运营。"
            },
            "e1c": {
                "vc": "线下合作？那你的电商平台还有什么优势？",
                "cto": "技术上可行，但需要整合线上线下系统。",
                "operation": "这个思路不错，可以降低获客成本，但需要找到合适的合作伙伴。"
            }
        }
        
        return {
            "comment": mock_comments.get(option_id, {}).get(style, "AI正在思考中..."),
            "style": style
        }
    
    def get_defense_question(self, project_info: Dict) -> Dict:
        """
        获取AI质疑问题
        :param project_info: 项目信息
        :return: AI质疑问题
        """
        # 模拟AI质疑问题
        mock_questions = [
            "你的项目没有核心竞争力，如何与现有竞争对手抗衡？",
            "你的团队没有行业经验，如何应对行业挑战？",
            "你的资金规划太乐观了，如何确保项目能够持续运营？",
            "你的市场分析太肤浅了，如何证明市场需求？",
            "你的商业模式不清晰，如何实现盈利？"
        ]
        
        return {
            "question": mock_questions[0],
            "round": 1
        }
    
    def get_defense_response(self, question: str, defense: str, style: str) -> Dict:
        """
        获取AI回应
        :param question: 问题
        :param defense: 辩护内容
        :param style: AI风格
        :return: AI回应
        """
        # 模拟AI回应
        mock_responses = {
            "vc": "你的辩护有一定道理，但还不够充分。你需要提供更具体的数据和案例来支持你的观点。",
            "cto": "技术上可行，但需要更多的资源和时间。你需要制定详细的技术路线图。",
            "operation": "运营策略合理，但需要更详细的执行计划。你需要考虑如何获取初始用户。"
        }
        
        return {
            "response": mock_responses.get(style, "AI正在思考中..."),
            "style": style,
            "deep_analysis": "你的项目在技术创新方面有潜力，但在市场推广方面存在风险。建议你制定更详细的市场推广计划。"
        }
    
    def generate_death_sentence(self, user_info: Dict, project_info: Dict) -> Dict:
        """
        生成创业死刑判决书
        :param user_info: 用户信息
        :param project_info: 项目信息
        :return: 死刑判决书内容
        """
        # 模拟死刑判决书
        return {
            "title": "创业死刑判决书",
            "guilty_verdict": {
                "crimes": [
                    {
                        "name": "空想罪",
                        "description": "你的项目缺乏具体的实施计划，只是一个美好的愿景。"
                    },
                    {
                        "name": "资源匮乏罪",
                        "description": "你缺乏必要的资金、技术和人脉资源。"
                    },
                    {
                        "name": "风险无知罪",
                        "description": "你对创业过程中的风险缺乏认识和应对措施。"
                    }
                ]
            },
            "failure_reasons": [
                "资金链断裂",
                "市场需求不足",
                "团队能力不足",
                "竞争过于激烈",
                "运营策略失误"
            ],
            "success_rate": "3.7%",
            "probation_suggestions": [
                "先积累行业经验和资源",
                "制定详细的商业计划",
                "寻找合适的合作伙伴"
            ]
        }
    
    def generate_appeal_application(self, death_sentence: Dict) -> Dict:
        """
        生成改判申请书
        :param death_sentence: 死刑判决书
        :return: 改判申请书内容
        """
        # 模拟改判申请书
        return {
            "title": "改判申请书",
            "rectification_plan": {
                "solutions": [
                    {
                        "problem": "资金链断裂",
                        "solution": "制定详细的资金规划，寻找天使投资人或众筹"
                    },
                    {
                        "problem": "市场需求不足",
                        "solution": "进行详细的市场调研，找到目标用户的真实需求"
                    },
                    {
                        "problem": "团队能力不足",
                        "solution": "招募有经验的团队成员，或寻求行业顾问的指导"
                    },
                    {
                        "problem": "竞争过于激烈",
                        "solution": "找到差异化竞争优势，专注于细分市场"
                    },
                    {
                        "problem": "运营策略失误",
                        "solution": "制定详细的运营计划，分阶段实施"
                    }
                ]
            },
            "feasibility_revision": "将原来的空想项目改为一个能落地的最小版本，先验证市场需求，再逐步扩大规模。",
            "reduced_sentence_proof": {
                "abilities": [
                    {"name": "创新能力", "score": 7},
                    {"name": "执行能力", "score": 5},
                    {"name": "团队管理", "score": 4},
                    {"name": "市场分析", "score": 6},
                    {"name": "资金管理", "score": 3}
                ],
                "weaknesses": "资金管理和团队管理能力需要重点提升"
            }
        }

# 创建AI服务实例
ai_service = AIService()

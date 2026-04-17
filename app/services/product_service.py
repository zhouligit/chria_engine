from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.product import ProductPurchase
from typing import List, Optional

class ProductService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_products(self) -> List[dict]:
        """
        获取产品列表
        :return: 产品列表
        """
        # 模拟产品列表
        products = [
            {
                "id": "death_sentence",
                "name": "创业死刑判决书",
                "price": 9.9,
                "description": "详细分析你的创业项目，指出存在的问题和失败风险",
                "features": [
                    "详细的创业项目分析",
                    "失败风险评估",
                    "创业成功率计算",
                    "针对性改进建议"
                ]
            },
            {
                "id": "appeal_application",
                "name": "改判申请书",
                "price": 19.9,
                "description": "针对死刑判决书中的问题，给出可执行的整改方案",
                "features": [
                    "问题整改方案",
                    "可行性修订建议",
                    "创业能力分析",
                    "一对一问题解答"
                ]
            },
            {
                "id": "accomplice_matching",
                "name": "同案犯匹配",
                "price": 29.9,
                "description": "匹配与你罪名相同、项目相似、能力互补的创业伙伴",
                "features": [
                    "创业伙伴匹配",
                    "合伙可行性分析",
                    "团队角色分配建议",
                    "社群加入权限"
                ]
            }
        ]
        return products
    
    def create_order(self, user_id: int, product_purchase: ProductPurchase) -> Order:
        """
        创建订单
        :param user_id: 用户ID
        :param product_purchase: 产品购买信息
        :return: 创建的订单
        """
        # 获取产品信息
        products = self.get_products()
        product = next((p for p in products if p["id"] == product_purchase.product_id), None)
        
        if not product:
            raise ValueError("产品不存在")
        
        # 创建订单
        new_order = Order(
            user_id=user_id,
            product_id=product["id"],
            product_name=product["name"],
            price=product["price"],
            status="completed"  # 模拟支付成功
        )
        
        self.db.add(new_order)
        self.db.commit()
        self.db.refresh(new_order)
        
        return new_order
    
    def get_product_content(self, user_id: int, product_id: str) -> Optional[dict]:
        """
        获取产品内容
        :param user_id: 用户ID
        :param product_id: 产品ID
        :return: 产品内容
        """
        # 检查用户是否购买了该产品
        order = self.db.query(Order).filter(
            Order.user_id == user_id,
            Order.product_id == product_id,
            Order.status == "completed"
        ).first()
        
        if not order:
            return None
        
        # 模拟产品内容
        product_content = {
            "death_sentence": {
                "title": "创业死刑判决书",
                "content": {
                    "guilty_verdict": "你被判处以下3大核心罪名：空想罪、资源匮乏罪、风险无知罪",
                    "failure_reasons": "你会失败的5个具体原因：资金链断裂、市场需求不足、团队能力不足、竞争过于激烈、运营策略失误",
                    "success_rate": "你的创业成功率：3.7%",
                    "probation_suggestions": "缓刑建议：先积累行业经验和资源、制定详细的商业计划、寻找合适的合作伙伴"
                }
            },
            "appeal_application": {
                "title": "改判申请书",
                "content": {
                    "rectification_plan": "针对你报告里的5个问题，我们给出以下可执行的整改方案：制定详细的资金规划、进行详细的市场调研、招募有经验的团队成员、找到差异化竞争优势、制定详细的运营计划",
                    "feasibility_revision": "将原来的空想项目改为一个能落地的最小版本，先验证市场需求，再逐步扩大规模",
                    "reduced_sentence_proof": "创业能力雷达图分析：创新能力7/10、执行能力5/10、团队管理4/10、市场分析6/10、资金管理3/10。需要重点提升的能力：资金管理和团队管理",
                    "one_on_one_question": "毒舌评审团1v1提问：你的问题：如何获取初始用户？AI回答：初始用户获取是创业的关键，建议你从身边的朋友和家人开始，通过口碑传播获取第一批用户。"
                }
            },
            "accomplice_matching": {
                "title": "同案犯匹配报告",
                "content": {
                    "accomplices": "我们为你匹配了3个和你罪名相同、项目相似、能力互补的同案犯：张三（电商运营专家）、李四（技术开发工程师）、王五（市场营销专员）",
                    "partnership_feasibility": "合伙可行性报告：团队角色分配建议：张三负责运营，李四负责技术，王五负责营销。潜在矛盾点：股权分配问题。合伙建议：签订详细的合伙协议，明确各方权利义务。",
                    "community_access": "缓刑观察室社群：社群名称：创业同案犯交流群，加入方式：扫描二维码加入，社群规则：禁止发布广告，禁止恶意攻击，鼓励分享真实经验。"
                }
            }
        }
        
        return product_content.get(product_id)

# 创建产品服务工厂
def get_product_service(db: Session) -> ProductService:
    return ProductService(db)

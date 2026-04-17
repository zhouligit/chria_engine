from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.api import auth, questions, scenarios, defense, products, share
from app.utils.database import Base, engine

# 加载环境变量
load_dotenv()

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title=os.getenv("APP_NAME", "Chira Engine"),
    description="赤壤引擎 - 劝退创业软件后端服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(questions.router, prefix="/api/questions", tags=["题库"])
app.include_router(scenarios.router, prefix="/api/scenarios", tags=["情景推演"])
app.include_router(defense.router, prefix="/api/defense", tags=["辩护博弈"])
app.include_router(products.router, prefix="/api/products", tags=["付费产品"])
app.include_router(share.router, prefix="/api/share", tags=["裂变分享"])

# 根路径
@app.get("/")
def read_root():
    return {"message": "Welcome to Chira Engine"}

# 健康检查
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# API 根路径
@app.get("/api")
async def api_root():
    return {"message": "Chira Engine API"}

"""
AI Agent Demo 主应用入口
"""
import os
import sys
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from loguru import logger

from app.core.config import settings
from app.utils.logger import setup_logger
from app.utils.database import create_tables
from app.api import agents, health


def check_environment():
    """检查运行环境"""
    logger.info("检查运行环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 9):
        logger.error("需要Python 3.9或更高版本")
        return False
    
    # 检查必要的目录
    directories = ["data", "logs", "data/uploads"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"✅ 目录已准备: {directory}")
    
    # 检查环境变量文件
    if not os.path.exists(".env") and os.path.exists("env.example"):
        import shutil
        shutil.copy("env.example", ".env")
        logger.info("✅ 创建.env文件")
        logger.warning("⚠️  请编辑.env文件，配置您的API密钥")
    
    logger.info("✅ 环境检查完成")
    return True


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("启动AI Agent Demo应用...")
    
    # 创建数据库表
    try:
        create_tables()
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"数据库表创建失败: {e}")
    
    # 创建必要的目录
    import os
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data/uploads", exist_ok=True)
    
    logger.info("应用启动完成")
    
    yield
    
    # 关闭时执行
    logger.info("关闭AI Agent Demo应用...")


# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    description="AI Agent Demo - 集成多种AI服务的智能代理系统",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(agents.router)
app.include_router(health.router)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用AI Agent Demo",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"未处理的异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "内部服务器错误"}
    )


if __name__ == "__main__":
    # 设置日志
    setup_logger()
    
    # 检查环境
    if not check_environment():
        logger.error("环境检查失败，应用无法启动")
        sys.exit(1)
    
    logger.info("🚀 启动AI Agent Demo应用...")
    logger.info(f"📋 访问地址:")
    logger.info(f"   主页: http://{settings.host}:{settings.port}")
    logger.info(f"   API文档: http://{settings.host}:{settings.port}/docs")
    logger.info(f"   健康检查: http://{settings.host}:{settings.port}/health")
    logger.info("=" * 50)
    
    # 启动服务器
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 
"""
健康检查API路由
"""
from fastapi import APIRouter
from typing import Dict, Any
from datetime import datetime
from loguru import logger
from app.core.config import settings
from app.services.ai_service import AIServiceFactory

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """健康检查"""
    try:
        # 检查AI服务可用性
        providers = AIServiceFactory.get_available_providers()
        
        return {
            "status": "healthy",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "available_ai_providers": providers,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@router.get("/ai")
async def ai_health_check() -> Dict[str, Any]:
    """AI服务健康检查"""
    try:
        results = {}
        providers = AIServiceFactory.get_available_providers()
        
        for provider in providers:
            try:
                service = AIServiceFactory.get_service(provider)
                # 简单的连接测试
                if provider == "ollama":
                    import httpx
                    async with httpx.AsyncClient() as client:
                        response = await client.get(f"{settings.ollama_base_url}/api/tags")
                        results[provider] = {
                            "status": "healthy",
                            "models": response.json().get("models", [])
                        }
                else:
                    results[provider] = {"status": "available"}
            except Exception as e:
                results[provider] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
        
        return {
            "ai_services": results,
            "overall_status": "healthy" if all(r.get("status") == "healthy" for r in results.values()) else "degraded"
        }
    except Exception as e:
        logger.error(f"AI健康检查失败: {e}")
        return {
            "ai_services": {},
            "overall_status": "unhealthy",
            "error": str(e)
        } 
"""
基础Agent类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from loguru import logger
from app.services.ai_service import AIServiceFactory


class BaseAgent(ABC):
    """基础Agent类"""
    
    def __init__(self, name: str, agent_type: str, provider: str = "ollama", **kwargs):
        self.name = name
        self.agent_type = agent_type
        self.provider = provider
        self.ai_service = AIServiceFactory.get_service(provider)
        self.config = kwargs.get("config", {})
        self.model_name = kwargs.get("model_name")
        
        logger.info(f"初始化Agent: {name} (类型: {agent_type}, 提供商: {provider})")
    
    @abstractmethod
    async def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """处理消息（子类实现）"""
        pass
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """生成AI响应"""
        try:
            result = await self.ai_service.generate_response(prompt, **kwargs)
            logger.info(f"Agent {self.name} 生成响应成功，耗时: {result.get('processing_time', 0):.2f}秒")
            return result
        except Exception as e:
            logger.error(f"Agent {self.name} 生成响应失败: {e}")
            raise
    
    def get_info(self) -> Dict[str, Any]:
        """获取Agent信息"""
        return {
            "name": self.name,
            "agent_type": self.agent_type,
            "provider": self.provider,
            "model_name": self.model_name,
            "config": self.config
        } 
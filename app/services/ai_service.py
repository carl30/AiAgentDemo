"""
AI服务模块
"""
import time
import httpx
import openai
from typing import Optional, Dict, Any, List
from loguru import logger
from app.core.config import settings


class AIService:
    """AI服务基类"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def _start_timer(self):
        """开始计时"""
        self.start_time = time.time()
    
    def _end_timer(self):
        """结束计时"""
        self.end_time = time.time()
        return self.end_time - self.start_time
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """生成响应（子类实现）"""
        raise NotImplementedError


class OllamaService(AIService):
    """Ollama服务"""
    
    def __init__(self):
        super().__init__()
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """使用Ollama生成响应"""
        self._start_timer()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": kwargs.get("model", self.model),
                        "prompt": prompt,
                        "stream": kwargs.get("stream", False),
                        "options": kwargs.get("options", {})
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()
                
                processing_time = self._end_timer()
                
                return {
                    "response": result.get("response", ""),
                    "model_used": kwargs.get("model", self.model),
                    "tokens_used": result.get("eval_count", 0),
                    "processing_time": processing_time,
                    "provider": "ollama",
                    "metadata": result
                }
                
        except Exception as e:
            logger.error(f"Ollama API错误: {e}")
            raise


class DeepSeekService(AIService):
    """DeepSeek服务"""
    
    def __init__(self):
        super().__init__()
        self.api_key = settings.deepseek_api_key
        self.base_url = settings.deepseek_api_base_url
        
        if self.api_key:
            openai.api_key = self.api_key
            openai.api_base = self.base_url
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """使用DeepSeek生成响应"""
        if not self.api_key:
            raise ValueError("DeepSeek API密钥未配置")
        
        self._start_timer()
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=kwargs.get("model", "deepseek-chat"),
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get("max_tokens", 1000),
                temperature=kwargs.get("temperature", 0.7),
                stream=kwargs.get("stream", False)
            )
            
            processing_time = self._end_timer()
            
            return {
                "response": response.choices[0].message.content,
                "model_used": kwargs.get("model", "deepseek-chat"),
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else 0,
                "processing_time": processing_time,
                "provider": "deepseek",
                "metadata": response.model_dump() if hasattr(response, 'model_dump') else {}
            }
            
        except Exception as e:
            logger.error(f"DeepSeek API错误: {e}")
            raise


class DifyService(AIService):
    """Dify服务"""
    
    def __init__(self):
        super().__init__()
        self.api_key = settings.dify_api_key
        self.base_url = settings.dify_api_base_url
    
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """使用Dify生成响应"""
        if not self.api_key:
            raise ValueError("Dify API密钥未配置")
        
        self._start_timer()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat-messages",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "inputs": {},
                        "query": prompt,
                        "response_mode": "streaming" if kwargs.get("stream", False) else "blocking",
                        "conversation_id": kwargs.get("conversation_id"),
                        "user": kwargs.get("user", "default")
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()
                
                processing_time = self._end_timer()
                
                return {
                    "response": result.get("answer", ""),
                    "model_used": "dify",
                    "tokens_used": result.get("usage", {}).get("total_tokens", 0),
                    "processing_time": processing_time,
                    "provider": "dify",
                    "metadata": result
                }
                
        except Exception as e:
            logger.error(f"Dify API错误: {e}")
            raise


class AIServiceFactory:
    """AI服务工厂"""
    
    @staticmethod
    def get_service(provider: str) -> AIService:
        """获取AI服务实例"""
        if provider == "ollama":
            return OllamaService()
        elif provider == "deepseek":
            return DeepSeekService()
        elif provider == "dify":
            return DifyService()
        else:
            raise ValueError(f"不支持的AI提供商: {provider}")
    
    @staticmethod
    def get_available_providers() -> List[str]:
        """获取可用的AI提供商"""
        providers = ["ollama"]
        
        if settings.deepseek_api_key:
            providers.append("deepseek")
        
        if settings.dify_api_key:
            providers.append("dify")
        
        return providers 
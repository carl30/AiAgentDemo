"""
聊天Agent实现
"""
from typing import Dict, Any, Optional
from loguru import logger
from .base import BaseAgent


class ChatAgent(BaseAgent):
    """聊天Agent"""
    
    def __init__(self, name: str = "ChatAgent", provider: str = "ollama", **kwargs):
        super().__init__(name, "chat", provider, **kwargs)
        self.conversation_history = []
        self.max_history = kwargs.get("max_history", 10)
    
    async def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """处理聊天消息"""
        try:
            # 构建对话历史
            prompt = self._build_prompt(message, context)
            
            # 生成响应
            result = await self.generate_response(prompt, **self.config)
            
            # 更新对话历史
            self._update_history(message, result["response"])
            
            return {
                "agent_id": self.name,
                "response": result["response"],
                "model_used": result["model_used"],
                "tokens_used": result["tokens_used"],
                "processing_time": result["processing_time"],
                "metadata": {
                    "conversation_length": len(self.conversation_history),
                    "provider": result["provider"]
                }
            }
            
        except Exception as e:
            logger.error(f"ChatAgent处理消息失败: {e}")
            raise
    
    def _build_prompt(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """构建提示词"""
        prompt_parts = []
        
        # 添加系统提示
        system_prompt = self.config.get("system_prompt", "你是一个有用的AI助手。请用中文回答问题。")
        prompt_parts.append(f"系统: {system_prompt}")
        
        # 添加对话历史
        if self.conversation_history:
            for i, (user_msg, ai_msg) in enumerate(self.conversation_history[-self.max_history:], 1):
                prompt_parts.append(f"用户{i}: {user_msg}")
                prompt_parts.append(f"助手{i}: {ai_msg}")
        
        # 添加当前消息
        prompt_parts.append(f"用户: {message}")
        prompt_parts.append("助手:")
        
        return "\n".join(prompt_parts)
    
    def _update_history(self, user_message: str, ai_response: str):
        """更新对话历史"""
        self.conversation_history.append((user_message, ai_response))
        
        # 保持历史记录在限制范围内
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history.clear()
        logger.info(f"ChatAgent {self.name} 对话历史已清空")
    
    def get_history(self) -> list:
        """获取对话历史"""
        return self.conversation_history.copy() 
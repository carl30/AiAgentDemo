"""
代码生成Agent
"""
from typing import Dict, Any, Optional
from loguru import logger
from .base import BaseAgent


class CodeAgent(BaseAgent):
    """代码生成Agent"""
    
    def __init__(self, name: str = "CodeAgent", provider: str = "ollama", **kwargs):
        super().__init__(name, "code", provider, **kwargs)
        self.language = kwargs.get("language", "python")
        self.framework = kwargs.get("framework", "")
    
    async def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """处理代码生成请求"""
        try:
            # 构建代码生成提示词
            prompt = self._build_code_prompt(message, context)
            
            # 生成响应
            result = await self.generate_response(prompt, **self.config)
            
            # 提取代码块
            code_blocks = self._extract_code_blocks(result["response"])
            
            return {
                "agent_id": self.name,
                "response": result["response"],
                "code_blocks": code_blocks,
                "model_used": result["model_used"],
                "tokens_used": result["tokens_used"],
                "processing_time": result["processing_time"],
                "metadata": {
                    "language": self.language,
                    "framework": self.framework,
                    "code_block_count": len(code_blocks),
                    "provider": result["provider"]
                }
            }
            
        except Exception as e:
            logger.error(f"CodeAgent处理消息失败: {e}")
            raise
    
    def _build_code_prompt(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """构建代码生成提示词"""
        prompt_parts = []
        
        # 系统提示
        system_prompt = f"""你是一个专业的{self.language}程序员。请根据用户的需求生成高质量的代码。

要求：
1. 代码要简洁、高效、易读
2. 添加必要的注释
3. 遵循最佳实践
4. 如果涉及特定框架，请使用{self.framework}（如果指定）
5. 提供完整的代码示例

请用中文回复，代码用markdown格式。"""
        
        prompt_parts.append(f"系统: {system_prompt}")
        
        # 添加上下文信息
        if context:
            if "requirements" in context:
                prompt_parts.append(f"需求: {context['requirements']}")
            if "constraints" in context:
                prompt_parts.append(f"约束: {context['constraints']}")
        
        # 添加用户消息
        prompt_parts.append(f"用户: {message}")
        prompt_parts.append("助手:")
        
        return "\n".join(prompt_parts)
    
    def _extract_code_blocks(self, response: str) -> list:
        """提取代码块"""
        code_blocks = []
        lines = response.split('\n')
        in_code_block = False
        current_block = []
        language = ""
        
        for line in lines:
            if line.startswith('```'):
                if not in_code_block:
                    # 开始代码块
                    in_code_block = True
                    language = line[3:].strip()
                    current_block = []
                else:
                    # 结束代码块
                    in_code_block = False
                    if current_block:
                        code_blocks.append({
                            "language": language,
                            "code": "\n".join(current_block)
                        })
                    current_block = []
            elif in_code_block:
                current_block.append(line)
        
        return code_blocks
    
    def set_language(self, language: str):
        """设置编程语言"""
        self.language = language
        logger.info(f"CodeAgent {self.name} 设置语言为: {language}")
    
    def set_framework(self, framework: str):
        """设置框架"""
        self.framework = framework
        logger.info(f"CodeAgent {self.name} 设置框架为: {framework}") 
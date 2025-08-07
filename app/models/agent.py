"""
Agent数据模型
"""
from sqlalchemy import Column, String, Text, JSON, Boolean
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

from .base import BaseModel as DBBaseModel


class Agent(DBBaseModel):
    """Agent数据库模型"""
    __tablename__ = "agents"
    
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    agent_type = Column(String(50), nullable=False, index=True)
    config = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    model_name = Column(String(100), nullable=True)
    provider = Column(String(50), nullable=True)  # ollama, deepseek, dify, openai


# Pydantic模型
class AgentBase(BaseModel):
    """Agent基础模型"""
    name: str
    description: Optional[str] = None
    agent_type: str
    config: Optional[Dict[str, Any]] = None
    model_name: Optional[str] = None
    provider: Optional[str] = None


class AgentCreate(AgentBase):
    """创建Agent模型"""
    pass


class AgentUpdate(BaseModel):
    """更新Agent模型"""
    name: Optional[str] = None
    description: Optional[str] = None
    agent_type: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    model_name: Optional[str] = None
    provider: Optional[str] = None


class AgentResponse(AgentBase):
    """Agent响应模型"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AgentRequest(BaseModel):
    """Agent请求模型"""
    message: str
    context: Optional[Dict[str, Any]] = None
    stream: bool = False


class AgentResponse(BaseModel):
    """Agent响应模型"""
    response: str
    agent_id: int
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None 
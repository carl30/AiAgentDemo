"""
Agent API路由
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from loguru import logger

from app.models.agent import AgentCreate, AgentUpdate, AgentResponse, AgentRequest
from app.utils.database import get_db
from app.agents.chat_agent import ChatAgent
from app.agents.code_agent import CodeAgent
from app.agents.search_agent import SearchAgent
from app.services.ai_service import AIServiceFactory

router = APIRouter(prefix="/agents", tags=["agents"])

# 内存中的Agent实例
_agents: Dict[str, Any] = {}


@router.get("/", response_model=List[Dict[str, Any]])
async def list_agents():
    """获取所有Agent列表"""
    try:
        agents_info = []
        for agent_id, agent in _agents.items():
            agents_info.append({
                "id": agent_id,
                **agent.get_info()
            })
        return agents_info
    except Exception as e:
        logger.error(f"获取Agent列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取Agent列表失败")


@router.post("/chat", response_model=Dict[str, Any])
async def create_chat_agent(agent_data: AgentCreate):
    """创建聊天Agent"""
    try:
        agent_id = f"chat_{len(_agents) + 1}"
        agent = ChatAgent(
            name=agent_data.name,
            provider=agent_data.provider or "ollama",
            config=agent_data.config or {},
            model_name=agent_data.model_name
        )
        _agents[agent_id] = agent
        
        logger.info(f"创建聊天Agent: {agent_id}")
        return {
            "agent_id": agent_id,
            **agent.get_info()
        }
    except Exception as e:
        logger.error(f"创建聊天Agent失败: {e}")
        raise HTTPException(status_code=500, detail="创建聊天Agent失败")


@router.post("/code", response_model=Dict[str, Any])
async def create_code_agent(agent_data: AgentCreate):
    """创建代码生成Agent"""
    try:
        agent_id = f"code_{len(_agents) + 1}"
        agent = CodeAgent(
            name=agent_data.name,
            provider=agent_data.provider or "ollama",
            config=agent_data.config or {},
            model_name=agent_data.model_name,
            language=agent_data.config.get("language", "python") if agent_data.config else "python",
            framework=agent_data.config.get("framework", "") if agent_data.config else ""
        )
        _agents[agent_id] = agent
        
        logger.info(f"创建代码生成Agent: {agent_id}")
        return {
            "agent_id": agent_id,
            **agent.get_info()
        }
    except Exception as e:
        logger.error(f"创建代码生成Agent失败: {e}")
        raise HTTPException(status_code=500, detail="创建代码生成Agent失败")


@router.post("/search", response_model=Dict[str, Any])
async def create_search_agent(agent_data: AgentCreate):
    """创建搜索引擎Agent"""
    try:
        agent_id = f"search_{len(_agents) + 1}"
        agent = SearchAgent(
            name=agent_data.name,
            provider=agent_data.provider or "ollama",
            config=agent_data.config or {},
            model_name=agent_data.model_name,
            search_engines=agent_data.config.get("search_engines", ["duckduckgo"]) if agent_data.config else ["duckduckgo"],
            max_results=agent_data.config.get("max_results", 1) if agent_data.config else 1,
            timeout=agent_data.config.get("timeout", 10.0) if agent_data.config else 10.0
        )
        _agents[agent_id] = agent
        
        logger.info(f"创建搜索引擎Agent: {agent_id}")
        return {
            "agent_id": agent_id,
            **agent.get_info()
        }
    except Exception as e:
        logger.error(f"创建搜索引擎Agent失败: {e}")
        raise HTTPException(status_code=500, detail="创建搜索引擎Agent失败")


@router.post("/{agent_id}/chat", response_model=Dict[str, Any])
async def chat_with_agent(agent_id: str, request: AgentRequest):
    """与Agent聊天"""
    try:
        if agent_id not in _agents:
            raise HTTPException(status_code=404, detail="Agent不存在")
        
        agent = _agents[agent_id]
        result = await agent.process_message(request.message, request.context)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"与Agent聊天失败: {e}")
        raise HTTPException(status_code=500, detail="与Agent聊天失败")


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    """删除Agent"""
    try:
        if agent_id not in _agents:
            raise HTTPException(status_code=404, detail="Agent不存在")
        
        del _agents[agent_id]
        logger.info(f"删除Agent: {agent_id}")
        
        return {"message": "Agent删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除Agent失败: {e}")
        raise HTTPException(status_code=500, detail="删除Agent失败")


@router.get("/{agent_id}/history")
async def get_agent_history(agent_id: str):
    """获取Agent对话历史"""
    try:
        if agent_id not in _agents:
            raise HTTPException(status_code=404, detail="Agent不存在")
        
        agent = _agents[agent_id]
        if hasattr(agent, 'get_history'):
            history = agent.get_history()
            return {"history": history}
        else:
            return {"history": []}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取Agent历史失败: {e}")
        raise HTTPException(status_code=500, detail="获取Agent历史失败")


@router.delete("/{agent_id}/history")
async def clear_agent_history(agent_id: str):
    """清空Agent对话历史"""
    try:
        if agent_id not in _agents:
            raise HTTPException(status_code=404, detail="Agent不存在")
        
        agent = _agents[agent_id]
        if hasattr(agent, 'clear_history'):
            agent.clear_history()
            return {"message": "对话历史已清空"}
        else:
            return {"message": "该Agent不支持历史记录"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"清空Agent历史失败: {e}")
        raise HTTPException(status_code=500, detail="清空Agent历史失败")


@router.get("/providers")
async def get_available_providers():
    """获取可用的AI提供商"""
    try:
        providers = AIServiceFactory.get_available_providers()
        return {"providers": providers}
    except Exception as e:
        logger.error(f"获取AI提供商失败: {e}")
        raise HTTPException(status_code=500, detail="获取AI提供商失败") 
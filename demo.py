"""
AI Agent Demo 演示脚本
"""
import asyncio
import httpx
from loguru import logger


async def demo_chat_agent():
    """演示聊天Agent功能"""
    logger.info("🤖 演示聊天Agent功能")
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        # 创建聊天Agent
        logger.info("1. 创建聊天Agent...")
        response = await client.post(
            "http://localhost:8000/agents/chat",
            json={
                "name": "智能助手",
                "agent_type": "chat", # 此处可更改
                "provider": "ollama",
                "config": {
                    "system_prompt": "你是一个有用的AI助手。请用中文回答问题，回答要简洁明了。"
                }
            }
        )
        
        if response.status_code == 200:
            agent_data = response.json()
            agent_id = agent_data["agent_id"]
            logger.info(f"✅ Agent创建成功，ID: {agent_id}")
            
            # 与Agent聊天
            logger.info("2. 与Agent聊天...")
            chat_response = await client.post(
                f"http://localhost:8000/agents/{agent_id}/chat",
                json={
                    "message": "你好，请介绍一下你自己",
                    "context": {},
                    "stream": False
                }
            )
            
            if chat_response.status_code == 200:
                result = chat_response.json()
                logger.info(f"✅ Agent回复: {result['response'][:100]}...")
                logger.info(f"   模型: {result['model_used']}")
                logger.info(f"   处理时间: {result['processing_time']:.2f}秒")
            else:
                logger.error(f"❌ 聊天失败: {chat_response.status_code}")
        else:
            logger.error(f"❌ Agent创建失败: {response.status_code}")


async def demo_code_agent():
    """演示代码生成Agent功能"""
    logger.info("💻 演示代码生成Agent功能")
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        # 创建代码生成Agent
        logger.info("1. 创建代码生成Agent...")
        response = await client.post(
            "http://localhost:8000/agents/code",
            json={
                "name": "Python代码助手",
                "agent_type": "code",
                "provider": "ollama",
                "config": {
                    "language": "python",
                    "framework": "fastapi"
                }
            }
        )
        
        if response.status_code == 200:
            agent_data = response.json()
            agent_id = agent_data["agent_id"]
            logger.info(f"✅ 代码Agent创建成功，ID: {agent_id}")
            
            # 生成代码
            logger.info("2. 生成代码...")
            code_response = await client.post(
                f"http://localhost:8000/agents/{agent_id}/chat",
                json={
                    "message": "请生成一个简单的FastAPI Hello World应用",
                    "context": {
                        "requirements": "使用FastAPI框架",
                        "constraints": "代码要简洁易懂，包含注释"
                    },
                    "stream": False
                }
            )
            
            if code_response.status_code == 200:
                result = code_response.json()
                logger.info(f"✅ 代码生成成功")
                logger.info(f"   代码块数量: {result['metadata']['code_block_count']}")
                logger.info(f"   处理时间: {result['processing_time']:.2f}秒")
                
                # 显示部分代码
                code_preview = result['response'][:200] + "..." if len(result['response']) > 200 else result['response']
                logger.info(f"   代码预览: {code_preview}")
            else:
                logger.error(f"❌ 代码生成失败: {code_response.status_code}")
        else:
            logger.error(f"❌ 代码Agent创建失败: {response.status_code}")


async def demo_search_agent():
    """演示搜索引擎Agent功能"""
    logger.info("🔍 演示搜索引擎Agent功能")
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        # 创建搜索引擎Agent
        logger.info("1. 创建搜索引擎Agent...")
        response = await client.post(
            "http://localhost:8000/agents/search",
            json={
                "name": "智能搜索助手",
                "agent_type": "search",
                "provider": "ollama",
                "config": {
                    "search_engines": ["duckduckgo"],
                    "max_results": 1,
                    "timeout": 10.0
                }
            }
        )
        
        if response.status_code == 200:
            agent_data = response.json()
            agent_id = agent_data["agent_id"]
            logger.info(f"✅ 搜索Agent创建成功，ID: {agent_id}")
            
            # 执行搜索
            logger.info("2. 执行搜索...")
            search_response = await client.post(
                f"http://localhost:8000/agents/{agent_id}/chat",
                json={
                    "message": "搜索Python最新版本信息",
                    "context": {
                        "search_query": "Python最新版本 2024"
                    },
                    "stream": False
                }
            )
            
            if search_response.status_code == 200:
                result = search_response.json()
                logger.info(f"✅ 搜索成功")
                logger.info(f"   搜索查询: {result['metadata']['search_query']}")
                logger.info(f"   搜索结果数: {result['metadata']['results_count']}")
                logger.info(f"   使用的搜索引擎: {result['metadata']['search_engines_used']}")
                logger.info(f"   处理时间: {result['processing_time']:.2f}秒")
                
                # 显示搜索结果
                response_preview = result['response'][:300] + "..." if len(result['response']) > 300 else result['response']
                logger.info(f"   搜索结果: {response_preview}")
            else:
                logger.error(f"❌ 搜索失败: {search_response.status_code}")
        else:
            logger.error(f"❌ 搜索Agent创建失败: {response.status_code}")


async def demo_health_check():
    """演示健康检查功能"""
    logger.info("🏥 演示健康检查功能")
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        # 检查应用健康状态
        logger.info("1. 检查应用健康状态...")
        response = await client.get("http://localhost:8000/health", follow_redirects=True)
        
        if response.status_code == 200:
            health_data = response.json()
            logger.info(f"✅ 应用状态: {health_data['status']}")
            logger.info(f"   应用名称: {health_data['app_name']}")
            logger.info(f"   版本: {health_data['version']}")
            logger.info(f"   环境: {health_data['environment']}")
            logger.info(f"   可用AI提供商: {health_data['available_ai_providers']}")
        else:
            logger.error(f"❌ 健康检查失败: {response.status_code}")
        
        # 检查AI服务健康状态
        logger.info("2. 检查AI服务健康状态...")
        ai_response = await client.get("http://localhost:8000/health/ai", follow_redirects=True)
        
        if ai_response.status_code == 200:
            ai_health = ai_response.json()
            logger.info(f"✅ AI服务状态: {ai_health['overall_status']}")
            for provider, status in ai_health['ai_services'].items():
                logger.info(f"   {provider}: {status['status']}")
        else:
            logger.error(f"❌ AI健康检查失败: {ai_response.status_code}")


async def demo_api_docs():
    """演示API文档功能"""
    logger.info("📚 演示API文档功能")
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        # 获取API文档
        logger.info("1. 获取API文档...")
        response = await client.get("http://localhost:8000/docs")
        
        if response.status_code == 200:
            logger.info("✅ API文档可访问")
            logger.info("   访问地址: http://localhost:8000/docs")
            logger.info("   交互式API文档，可以测试所有接口")
        else:
            logger.error(f"❌ API文档访问失败: {response.status_code}")


async def main():
    """主演示函数"""
    logger.info("🚀 AI Agent Demo 功能演示")
    logger.info("=" * 50)
    
    try:
        # 等待应用启动
        logger.info("等待应用启动...")
        await asyncio.sleep(3)
        
        # 演示健康检查
        await demo_health_check()
        logger.info("")
        
        # 演示聊天Agent
        await demo_chat_agent()
        logger.info("")
        
        # 演示代码生成Agent
        await demo_code_agent()
        logger.info("")
        
        # 演示搜索引擎Agent
        await demo_search_agent()
        logger.info("")
        
        # 演示API文档
        await demo_api_docs()
        logger.info("")
        
        logger.info("🎉 演示完成！")
        logger.info("=" * 50)
        logger.info("📋 下一步:")
        logger.info("1. 访问 http://localhost:8000/docs 查看完整API文档")
        logger.info("2. 尝试创建更多类型的Agent")
        logger.info("3. 集成其他AI提供商（DeepSeek、Dify等）")
        logger.info("4. 开发自定义Agent类型")
        
    except Exception as e:
        logger.error(f"演示过程中出现错误: {e}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        logger.info("请确保应用正在运行: python main.py")


if __name__ == "__main__":
    asyncio.run(main()) 
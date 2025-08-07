"""
搜索引擎Agent使用示例
"""
import asyncio
import httpx
from loguru import logger


async def simple_search_example():
    """简单的搜索示例"""
    logger.info("🔍 搜索引擎Agent使用示例")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # 1. 创建搜索引擎Agent
            logger.info("1. 创建搜索引擎Agent...")
            response = await client.post(
                "http://localhost:8000/agents/search",
                json={
                    "name": "示例搜索助手",
                    "agent_type": "search",
                    "provider": "ollama",
                    "config": {
                        "search_engines": ["bing"],
                        "max_results": 1,
                        "timeout": 10.0
                    }
                }
            )
            
            if response.status_code != 200:
                logger.error(f"❌ 创建Agent失败: {response.status_code}")
                return
            
            agent_data = response.json()
            agent_id = agent_data["agent_id"]
            logger.info(f"✅ Agent创建成功，ID: {agent_id}")
            
            # 2. 执行搜索
            search_queries = [
                "Python最新版本",
                # "FastAPI框架",
                # "人工智能发展"
            ]
            
            for query in search_queries:
                logger.info(f"\n🔍 搜索: {query}")
                
                search_response = await client.post(
                    f"http://localhost:8000/agents/{agent_id}/chat",
                    json={
                        "message": f"请搜索{query}的相关信息",
                        "context": {},
                        "stream": False
                    }
                )
                
                if search_response.status_code == 200:
                    result = search_response.json()
                    logger.info(f"✅ 搜索成功")
                    logger.info(f"   查询: {result['metadata']['search_query']}")
                    logger.info(f"   结果数: {result['metadata']['results_count']}")
                    logger.info(f"   处理时间: {result['processing_time']:.2f}秒")
                    
                    # 显示搜索结果
                    response_text = result['response']
                    logger.info(f"   搜索结果:")
                    logger.info(f"   {response_text}")
                else:
                    logger.error(f"❌ 搜索失败: {search_response.status_code}")
            
            logger.info("\n🎉 示例完成！")
            
        except Exception as e:
            logger.error(f"示例执行失败: {e}")
            import traceback
            logger.error(f"详细错误: {traceback.format_exc()}")


if __name__ == "__main__":
    asyncio.run(simple_search_example()) 
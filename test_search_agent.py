"""
搜索引擎Agent测试脚本
"""
import asyncio
import httpx
from loguru import logger


async def test_search_agent():
    """测试搜索引擎Agent"""
    logger.info("🔍 测试搜索引擎Agent功能")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # 1. 创建搜索引擎Agent
            logger.info("1. 创建搜索引擎Agent...")
            response = await client.post(
                "http://localhost:8000/agents/search",
                json={
                    "name": "测试搜索助手",
                    "agent_type": "search",
                    "provider": "ollama",
                    "config": {
                        "search_engines": ["duckduckgo"],
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
            
            # 2. 测试搜索功能
            test_queries = [
                "Python最新版本",
                "FastAPI框架介绍",
                "人工智能发展趋势"
            ]
            
            for i, query in enumerate(test_queries, 1):
                logger.info(f"\n2.{i} 测试搜索: {query}")
                
                search_response = await client.post(
                    f"http://localhost:8000/agents/{agent_id}/chat",
                    json={
                        "message": f"搜索{query}",
                        "context": {
                            "search_query": query
                        },
                        "stream": False
                    }
                )
                
                if search_response.status_code == 200:
                    result = search_response.json()
                    logger.info(f"✅ 搜索成功")
                    logger.info(f"   查询: {result['metadata']['search_query']}")
                    logger.info(f"   结果数: {result['metadata']['results_count']}")
                    logger.info(f"   处理时间: {result['processing_time']:.2f}秒")
                    
                    # 显示部分响应
                    response_preview = result['response'][:200] + "..." if len(result['response']) > 200 else result['response']
                    logger.info(f"   响应: {response_preview}")
                else:
                    logger.error(f"❌ 搜索失败: {search_response.status_code}")
            
            # 3. 测试直接搜索查询
            logger.info("\n3. 测试直接搜索查询...")
            direct_response = await client.post(
                f"http://localhost:8000/agents/{agent_id}/chat",
                json={
                    "message": "请帮我搜索一下机器学习的最新发展",
                    "context": {},
                    "stream": False
                }
            )
            
            if direct_response.status_code == 200:
                result = direct_response.json()
                logger.info(f"✅ 直接搜索成功")
                logger.info(f"   查询: {result['metadata']['search_query']}")
                logger.info(f"   结果数: {result['metadata']['results_count']}")
                
                response_preview = result['response'][:300] + "..." if len(result['response']) > 300 else result['response']
                logger.info(f"   响应: {response_preview}")
            else:
                logger.error(f"❌ 直接搜索失败: {direct_response.status_code}")
            
            logger.info("\n🎉 搜索引擎Agent测试完成！")
            
        except Exception as e:
            logger.error(f"测试过程中出现错误: {e}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")


if __name__ == "__main__":
    asyncio.run(test_search_agent()) 
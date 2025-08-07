"""
搜索引擎Agent实现
"""
import re
import asyncio
from typing import Dict, Any, Optional, List
from urllib.parse import quote_plus
import httpx
from bs4 import BeautifulSoup
from loguru import logger
from .base import BaseAgent


class SearchAgent(BaseAgent):
    """搜索引擎Agent"""
    
    def __init__(self, name: str = "SearchAgent", provider: str = "ollama", **kwargs):
        super().__init__(name, "search", provider, **kwargs)
        self.search_engines = kwargs.get("search_engines", ["duckduckgo"])
        self.max_results = kwargs.get("max_results", 1)
        self.timeout = kwargs.get("timeout", 10.0)
        
    async def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """处理搜索请求"""
        try:
            # 提取搜索关键词
            search_query = self._extract_search_query(message, context)
            
            # 执行搜索
            search_results = await self._perform_search(search_query)
            
            # 构建响应
            response = self._build_response(search_query, search_results)
            
            # 使用AI服务优化响应
            ai_response = await self._enhance_with_ai(message, search_results, context)
            
            return {
                "agent_id": self.name,
                "response": ai_response["response"],
                "model_used": ai_response["model_used"],
                "tokens_used": ai_response["tokens_used"],
                "processing_time": ai_response["processing_time"],
                "metadata": {
                    "search_query": search_query,
                    "search_results": search_results,
                    "search_engines_used": self.search_engines,
                    "results_count": len(search_results)
                }
            }
            
        except Exception as e:
            logger.error(f"SearchAgent处理消息失败: {e}")
            raise
    
    def _extract_search_query(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """提取搜索关键词"""
        # 如果context中有明确的搜索查询，使用它
        if context and "search_query" in context:
            return context["search_query"]
        
        # 从消息中提取搜索关键词
        # 移除常见的搜索指示词
        search_indicators = [
            "搜索", "查找", "查询", "搜索一下", "帮我搜索", "请搜索",
            "search", "find", "look up", "search for"
        ]
        
        query = message.strip()
        for indicator in search_indicators:
            if query.startswith(indicator):
                query = query[len(indicator):].strip()
                break
        
        return query if query else message.strip()
    
    async def _perform_search(self, query: str) -> List[Dict[str, Any]]:
        """执行搜索"""
        all_results = []
        
        for engine in self.search_engines:
            try:
                if engine == "duckduckgo":
                    results = await self._search_google(query)  # 使用DuckDuckGo
                elif engine == "bing":
                    results = await self._search_bing(query)
                elif engine == "google":
                    results = await self._search_google(query)  # 也使用DuckDuckGo作为Google替代
                else:
                    logger.warning(f"不支持的搜索引擎: {engine}")
                    continue
                
                all_results.extend(results)
                
            except Exception as e:
                logger.error(f"搜索引擎 {engine} 搜索失败: {e}")
                continue
        
        # 去重并限制结果数量
        unique_results = self._deduplicate_results(all_results)
        return unique_results[:self.max_results]
    
    async def _search_google(self, query: str) -> List[Dict[str, Any]]:
        """使用DuckDuckGo搜索（Google替代）"""
        try:
            # 使用DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": "1",
                "skip_disambig": "1"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                results = []
                
                # 处理即时答案
                if data.get("Abstract"):
                    results.append({
                        "title": data.get("AbstractSource", "DuckDuckGo"),
                        "snippet": data.get("Abstract", ""),
                        "url": data.get("AbstractURL", ""),
                        "engine": "duckduckgo"
                    })
                
                # 处理相关主题
                for topic in data.get("RelatedTopics", [])[:3]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        results.append({
                            "title": topic.get("FirstURL", "").split("/")[-1] if topic.get("FirstURL") else "相关主题",
                            "snippet": topic.get("Text", ""),
                            "url": topic.get("FirstURL", ""),
                            "engine": "duckduckgo"
                        })
                
                return results
                
        except Exception as e:
            logger.error(f"DuckDuckGo搜索失败: {e}")
            return []
    
    async def _search_bing(self, query: str) -> List[Dict[str, Any]]:
        """使用Bing搜索（简化版）"""
        try:
            # 使用Bing的简化搜索API
            url = "https://www.bing.com/search"
            params = {
                "q": query,
                "format": "json",
                "cc": "CN"
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                
                # 由于Bing API限制，这里返回模拟结果
                # 在实际使用中，可以考虑使用Bing Search API（需要API密钥）
                results = [{
                    "title": f"关于 {query} 的搜索结果",
                    "snippet": f"这是关于 {query} 的搜索结果。由于API限制，这里显示的是模拟数据。",
                    "url": f"https://www.bing.com/search?q={quote_plus(query)}",
                    "engine": "bing"
                }]
                
                return results
                
        except Exception as e:
            logger.error(f"Bing搜索失败: {e}")
            return []
    
    def _is_advertisement(self, title: str, snippet: str) -> bool:
        """判断是否为广告"""
        ad_indicators = [
            "广告", "推广", "赞助", "ad", "sponsored", "promoted",
            "购买", "优惠", "折扣", "限时", "特价"
        ]
        
        text = (title + " " + snippet).lower()
        return any(indicator in text for indicator in ad_indicators)
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """去重搜索结果"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
    
    def _build_response(self, query: str, results: List[Dict[str, Any]]) -> str:
        """构建搜索响应"""
        if not results:
            return f"抱歉，没有找到关于 '{query}' 的相关信息。"
        
        response_parts = [f"关于 '{query}' 的搜索结果：\n"]
        
        for i, result in enumerate(results, 1):
            response_parts.append(f"{i}. {result['title']}")
            response_parts.append(f"   {result['snippet']}")
            if result.get('url'):
                response_parts.append(f"   链接: {result['url']}")
            response_parts.append("")
        
        return "\n".join(response_parts)
    
    async def _enhance_with_ai(self, original_message: str, search_results: List[Dict[str, Any]], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """使用AI增强搜索结果"""
        if not search_results:
            prompt = f"用户询问: {original_message}\n\n没有找到相关信息，请给出合适的回复。"
        else:
            # 构建包含搜索结果的提示
            search_info = "\n".join([
                f"- {result['title']}: {result['snippet']}"
                for result in search_results
            ])
            
            prompt = f"""基于以下搜索结果回答用户的问题:

用户问题: {original_message}

搜索结果:
{search_info}

请根据搜索结果提供准确、有用的回答。如果搜索结果不足以回答问题，请说明这一点。"""

        return await self.generate_response(prompt, **self.config)
    
    def get_search_history(self) -> List[Dict[str, Any]]:
        """获取搜索历史（如果需要的话）"""
        # 这里可以实现搜索历史记录功能
        return [] 
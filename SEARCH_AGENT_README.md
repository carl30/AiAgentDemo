# 搜索引擎Agent使用说明

## 概述

搜索引擎Agent是一个能够调用搜索引擎并获取前1个非广告结果的智能代理。它支持多种搜索引擎，并能够使用AI服务来优化和总结搜索结果。

## 功能特性

- 🔍 **多搜索引擎支持**: 支持DuckDuckGo、Bing等搜索引擎
- 🚫 **广告过滤**: 自动过滤广告和推广内容
- 🤖 **AI增强**: 使用AI服务优化搜索结果
- ⚡ **快速响应**: 异步处理，支持超时控制
- 📊 **结果去重**: 自动去除重复的搜索结果

## 安装依赖

确保已安装必要的依赖：

```bash
pip install beautifulsoup4 lxml
```

## API使用

### 1. 创建搜索引擎Agent

```bash
POST /agents/search
```

请求体：
```json
{
    "name": "智能搜索助手",
    "agent_type": "search",
    "provider": "ollama",
    "config": {
        "search_engines": ["duckduckgo"],
        "max_results": 1,
        "timeout": 10.0
    }
}
```

### 2. 与Agent交互

```bash
POST /agents/{agent_id}/chat
```

请求体：
```json
{
    "message": "搜索Python最新版本信息",
    "context": {
        "search_query": "Python最新版本 2024"
    },
    "stream": false
}
```

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `search_engines` | List[str] | `["duckduckgo"]` | 使用的搜索引擎列表 |
| `max_results` | int | `1` | 最大返回结果数量 |
| `timeout` | float | `10.0` | 搜索超时时间（秒） |

## 支持的搜索引擎

### 1. DuckDuckGo
- **API**: 免费，无需API密钥
- **特点**: 隐私保护，无广告
- **配置**: `"duckduckgo"`

### 2. Bing
- **API**: 需要API密钥（当前使用模拟数据）
- **特点**: 微软官方搜索引擎
- **配置**: `"bing"`

## 使用示例

### Python示例

```python
import httpx
import asyncio

async def search_example():
    async with httpx.AsyncClient() as client:
        # 创建搜索Agent
        response = await client.post(
            "http://localhost:8000/agents/search",
            json={
                "name": "搜索助手",
                "agent_type": "search",
                "provider": "ollama",
                "config": {
                    "search_engines": ["duckduckgo"],
                    "max_results": 1
                }
            }
        )
        
        agent_id = response.json()["agent_id"]
        
        # 执行搜索
        search_response = await client.post(
            f"http://localhost:8000/agents/{agent_id}/chat",
            json={
                "message": "搜索人工智能最新发展",
                "context": {},
                "stream": False
            }
        )
        
        result = search_response.json()
        print(f"搜索结果: {result['response']}")
        print(f"查询: {result['metadata']['search_query']}")
        print(f"结果数: {result['metadata']['results_count']}")

# 运行示例
asyncio.run(search_example())
```

### cURL示例

```bash
# 创建搜索Agent
curl -X POST "http://localhost:8000/agents/search" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "搜索助手",
    "agent_type": "search",
    "provider": "ollama",
    "config": {
      "search_engines": ["duckduckgo"],
      "max_results": 1
    }
  }'

# 执行搜索
curl -X POST "http://localhost:8000/agents/search_1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "搜索Python最新版本",
    "context": {},
    "stream": false
  }'
```

## 测试

运行测试脚本：

```bash
python test_search_agent.py
```

## 演示

运行完整演示：

```bash
python demo.py
```

## 注意事项

1. **网络连接**: 确保服务器能够访问搜索引擎
2. **超时设置**: 根据网络情况调整timeout参数
3. **API限制**: 某些搜索引擎可能有请求频率限制
4. **结果质量**: 搜索结果的质量取决于搜索引擎的算法

## 扩展功能

### 添加新的搜索引擎

1. 在`SearchAgent`类中添加新的搜索方法
2. 在`_perform_search`方法中添加对应的处理逻辑
3. 更新配置参数支持

### 自定义广告过滤

修改`_is_advertisement`方法来自定义广告识别规则。

### 结果缓存

可以添加缓存机制来避免重复搜索相同查询。

## 故障排除

### 常见问题

1. **搜索失败**: 检查网络连接和搜索引擎可用性
2. **超时错误**: 增加timeout参数值
3. **无结果**: 尝试不同的搜索关键词
4. **API错误**: 检查搜索引擎API状态

### 日志查看

查看详细日志来诊断问题：

```python
from loguru import logger
logger.add("search_agent.log", rotation="1 day")
```

## 贡献

欢迎提交Issue和Pull Request来改进搜索引擎Agent的功能。 
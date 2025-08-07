# AI Agent Demo 使用指南

## 快速开始

### 1. 环境准备

确保您已安装：
- Python 3.9+
- Ollama（本地运行）
- Docker Desktop（可选）

### 2. 安装和配置

```bash
# 克隆项目
git clone <repository-url>
cd AiAgentDemo

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env.example .env
# 编辑 .env 文件，填入您的API密钥
```

### 3. 启动应用

```bash
# 使用启动脚本（推荐）
python main.py

# 或直接启动
python main.py
```

### 4. 验证安装

访问以下URL验证应用是否正常运行：
- http://localhost:8000 - 主页
- http://localhost:8000/health - 健康检查
- http://localhost:8000/docs - API文档

## API使用示例

### 1. 创建聊天Agent

```bash
curl -X POST "http://localhost:8000/agents/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "我的聊天助手",
    "provider": "ollama",
    "config": {
      "system_prompt": "你是一个有用的AI助手。请用中文回答问题。"
    }
  }'
```

### 2. 与Agent聊天

```bash
curl -X POST "http://localhost:8000/agents/chat_1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好，请介绍一下你自己",
    "context": {},
    "stream": false
  }'
```

### 3. 创建代码生成Agent

```bash
curl -X POST "http://localhost:8000/agents/code" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python代码助手",
    "provider": "ollama",
    "config": {
      "language": "python",
      "framework": "fastapi"
    }
  }'
```

### 4. 生成代码

```bash
curl -X POST "http://localhost:8000/agents/code_1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "请生成一个简单的FastAPI Hello World应用",
    "context": {
      "requirements": "使用FastAPI框架",
      "constraints": "代码要简洁易懂"
    },
    "stream": false
  }'
```

## Python客户端示例

```python
import httpx
import asyncio

async def chat_with_agent():
    async with httpx.AsyncClient() as client:
        # 创建聊天Agent
        response = await client.post(
            "http://localhost:8000/agents/chat",
            json={
                "name": "测试Agent",
                "provider": "ollama",
                "config": {"system_prompt": "你是一个有用的AI助手。"}
            }
        )
        
        if response.status_code == 200:
            agent_data = response.json()
            agent_id = agent_data["agent_id"]
            
            # 与Agent聊天
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
                print(f"Agent回复: {result['response']}")

# 运行示例
asyncio.run(chat_with_agent())
```

## 支持的AI提供商

### 1. Ollama（本地）

- **优点**: 本地部署，数据安全，免费
- **配置**: 确保Ollama服务运行在 http://localhost:11434
- **模型**: 支持多种开源模型，如 deepseek-r1-8b

### 2. DeepSeek API

- **优点**: 云端服务，性能稳定
- **配置**: 在 `.env` 文件中设置 `DEEPSEEK_API_KEY`
- **模型**: deepseek-chat 等

### 3. Dify

- **优点**: 可视化AI应用开发平台
- **配置**: 在 `.env` 文件中设置 `DIFY_API_KEY`
- **功能**: 支持工作流编排

## 环境变量配置

### 必需配置

```bash
# Ollama配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1-8b

# 应用配置
DEBUG=true
LOG_LEVEL=INFO
```

### 可选配置

```bash
# DeepSeek API
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_API_BASE_URL=https://api.deepseek.com/v1

# Dify API
DIFY_API_KEY=your_dify_api_key_here
DIFY_API_BASE_URL=https://api.dify.ai/v1

# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE_URL=https://api.openai.com/v1
```

## 故障排除

### 1. Ollama连接失败

```bash
# 检查Ollama服务状态
curl http://localhost:11434/api/tags

# 启动Ollama服务
ollama serve

# 下载模型
ollama pull deepseek-r1-8b
```

### 2. 依赖安装失败

```bash
# 升级pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt

# 如果仍有问题，尝试使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 端口被占用

```bash
# 检查端口占用
netstat -an | grep 8000

# 修改端口（在.env文件中）
PORT=8001
```

## 开发指南

### 1. 添加新的Agent类型

1. 在 `app/agents/` 目录下创建新的Agent类
2. 继承 `BaseAgent` 类
3. 实现 `process_message` 方法
4. 在 `app/api/agents.py` 中添加API路由

### 2. 添加新的AI提供商

1. 在 `app/services/ai_service.py` 中创建新的服务类
2. 继承 `AIService` 类
3. 实现 `generate_response` 方法
4. 在 `AIServiceFactory` 中注册新服务

### 3. 自定义配置

可以通过修改 `.env` 文件或环境变量来自定义应用行为：

```bash
# 日志配置
LOG_LEVEL=DEBUG
LOG_FILE=./logs/app.log

# 数据库配置
DATABASE_URL=sqlite:///./data/ai_agent_demo.db

# 限流配置
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

## 监控和日志

### 1. 查看日志

```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
tail -f logs/error.log
```

### 2. 健康检查

```bash
# 检查应用状态
curl http://localhost:8000/health

# 检查AI服务状态
curl http://localhost:8000/health/ai
```

### 3. 性能监控

应用内置了性能监控功能，可以通过以下方式查看：

- 访问 http://localhost:8000/docs 查看API文档
- 查看日志文件中的性能指标
- 使用第三方监控工具（如Prometheus）

## 部署指南

### 1. Docker部署

```bash
# 构建镜像
docker build -t ai-agent-demo .

# 运行容器
docker run -p 8000:8000 ai-agent-demo

# 使用Docker Compose
docker-compose up -d
```

### 2. 生产环境部署

1. 设置环境变量
2. 配置反向代理（如Nginx）
3. 设置SSL证书
4. 配置监控和告警
5. 设置日志轮转

### 3. 性能优化

- 使用Redis缓存
- 配置连接池
- 启用压缩
- 使用CDN加速静态资源

## 常见问题

### Q: 如何切换AI提供商？

A: 在创建Agent时指定 `provider` 参数，或在 `.env` 文件中设置默认提供商。

### Q: 如何添加自定义模型？

A: 在Ollama中下载新模型，然后在配置中指定模型名称。

### Q: 如何实现流式响应？

A: 在请求中设置 `"stream": true`，并处理流式响应数据。

### Q: 如何扩展Agent功能？

A: 继承 `BaseAgent` 类，实现自定义的 `process_message` 方法。

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

MIT License 
# AI Agent Demo

这是一个AI Agent的演示项目，集成了多种AI服务和技术栈。

## 项目特性

- 🤖 支持多种AI模型（Ollama、DeepSeek、Dify）
- 🔍 搜索引擎Agent（支持DuckDuckGo、Bing等）
- 🐳 Docker容器化部署
- 🔧 模块化设计，易于扩展
- 📊 完整的日志和监控
- 🎯 实用的Agent示例

## 技术栈

- **Python 3.9+**
- **FastAPI** - Web框架
- **Ollama** - 本地大语言模型
- **DeepSeek API** - 云端AI服务
- **Dify** - AI应用开发平台
- **Docker** - 容器化部署
- **SQLite** - 轻量级数据库

## Todos
- [ ] search engine invoke (free engine instead)
- [ ] opit prompt

## 快速开始

### 1. 环境准备

确保您已安装：
- Python 3.9+
- Docker Desktop
- Ollama（本地运行）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `env.example` 到 `.env` 并配置：

```bash
cp env.example .env
```

编辑 `.env` 文件，填入您的API密钥和配置。

### 4. 运行项目

```bash
# 直接运行应用
python main.py

# 或使用Docker
docker-compose up
```

### 5. 访问应用

打开浏览器访问：
- 主页：http://localhost:8000
- API文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

### 6. 测试功能

```bash
# 运行演示脚本
python demo.py

# 运行搜索引擎Agent测试
python test_search_agent.py

# 运行搜索引擎Agent示例
python search_example.py
```

## 项目结构

```
AiAgentDemo/
├── app/                    # 主应用目录
│   ├── agents/            # Agent实现
│   ├── api/               # API路由
│   ├── core/              # 核心配置
│   ├── models/            # 数据模型
│   ├── services/          # 业务服务
│   └── utils/             # 工具函数
├── config/                # 配置文件
├── data/                  # 数据文件
├── logs/                  # 日志文件
├── tests/                 # 测试文件
├── docker-compose.yml     # Docker配置
├── Dockerfile             # Docker镜像
├── main.py                # 应用入口
├── demo.py                # 演示脚本
├── requirements.txt       # Python依赖
├── env.example            # 环境变量示例
└── README.md             # 项目说明
```

## 配置说明

### 环境变量

- `DEEPSEEK_API_KEY`: DeepSeek API密钥
- `DIFY_API_KEY`: Dify API密钥
- `OLLAMA_BASE_URL`: Ollama服务地址
- `LOG_LEVEL`: 日志级别

### AI模型配置

项目支持多种AI模型：

1. **Ollama本地模型**
   - 支持多种开源模型
   - 本地部署，数据安全

2. **DeepSeek API**
   - 云端AI服务
   - 高性能，功能丰富

3. **Dify平台**
   - 可视化AI应用开发
   - 工作流编排

## 开发指南

### 添加新的Agent

1. 在 `app/agents/` 目录下创建新的Agent类
2. 继承 `BaseAgent` 类
3. 实现必要的方法
4. 在 `app/api/` 中添加API路由

### 现有Agent类型

- **ChatAgent**: 聊天对话Agent
- **CodeAgent**: 代码生成Agent
- **SearchAgent**: 搜索引擎Agent（新增）

### 添加新的服务

1. 在 `app/services/` 目录下创建服务类
2. 实现业务逻辑
3. 在Agent中调用服务

## 部署

### Docker部署

```bash
# 构建镜像
docker build -t ai-agent-demo .

# 运行容器
docker run -p 8000:8000 ai-agent-demo
```

### 生产环境

1. 配置环境变量
2. 设置日志轮转
3. 配置监控告警
4. 设置反向代理

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

None

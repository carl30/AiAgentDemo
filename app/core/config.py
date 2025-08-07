"""
应用配置管理模块
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基本信息
    app_name: str = Field(default="AiAgentDemo", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # 服务器配置
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")
    
    # 数据库配置
    database_url: str = Field(default="sqlite:///./data/ai_agent_demo.db", env="DATABASE_URL")
    
    # 日志配置
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="./logs/app.log", env="LOG_FILE")
    
    # AI服务配置
    
    # DeepSeek API
    deepseek_api_key: Optional[str] = Field(default=None, env="DEEPSEEK_API_KEY")
    deepseek_api_base_url: str = Field(default="https://api.deepseek.com/v1", env="DEEPSEEK_API_BASE_URL")
    
    # Dify API
    dify_api_key: Optional[str] = Field(default=None, env="DIFY_API_KEY")
    dify_api_base_url: str = Field(default="https://api.dify.ai/v1", env="DIFY_API_BASE_URL")
    
    # Ollama配置
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="deepseek-r1:8b", env="OLLAMA_MODEL")
    
    # OpenAI API (可选)
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_api_base_url: str = Field(default="https://api.openai.com/v1", env="OPENAI_API_BASE_URL")
    
    # Anthropic API (可选)
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    
    # 安全配置
    secret_key: str = Field(default="your_secret_key_here_change_in_production", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # 监控配置
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    
    # 缓存配置
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    
    # 文件存储
    upload_dir: str = Field(default="./data/uploads", env="UPLOAD_DIR")
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    
    # 限流配置
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    rate_limit_per_hour: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 创建全局配置实例
settings = Settings()


def get_settings() -> Settings:
    """获取配置实例"""
    return settings


def is_development() -> bool:
    """检查是否为开发环境"""
    return settings.environment.lower() == "development"


def is_production() -> bool:
    """检查是否为生产环境"""
    return settings.environment.lower() == "production" 
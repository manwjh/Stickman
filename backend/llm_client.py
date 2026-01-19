"""
LLM Client - Unified LLM Interface
统一的LLM客户端

职责：
1. 统一管理LLM配置和连接
2. 提供统一的completion接口
3. 处理不同provider的差异
4. 支持依赖注入和测试

Author: Shenzhen Wang & AI
License: MIT
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
import litellm

logger = logging.getLogger(__name__)


class LLMClient:
    """统一的LLM客户端"""
    
    def __init__(self, provider: Optional[str] = None):
        """
        初始化LLM客户端
        
        Args:
            provider: LLM提供商，如果不指定则从环境变量读取
        """
        self.provider = provider or self._get_required_env('LLM_PROVIDER')
        self._load_config()
        logger.info(
            f"LLM Client initialized: provider={self.provider}, "
            f"model={self.model}, max_tokens={self.max_tokens}"
        )
    
    def _get_required_env(self, key: str) -> str:
        """获取必需的环境变量，如果不存在则报错"""
        value = os.getenv(key)
        if not value:
            raise ValueError(
                f"Required environment variable not set: {key}\n"
                f"Please ensure config.yml is properly loaded."
            )
        return value
    
    def _load_config(self):
        """从环境变量加载配置"""
        provider = self.provider.lower()
        
        if provider == 'perfxcloud':
            self.model = f"openai/{self._get_required_env('PERFXCLOUD_MODEL')}"
            self.api_key = self._get_required_env('PERFXCLOUD_API_KEY')
            self.api_base = self._get_required_env('PERFXCLOUD_API_BASE')
            self.temperature = float(self._get_required_env('PERFXCLOUD_TEMPERATURE'))
            self.max_tokens = int(self._get_required_env('PERFXCLOUD_MAX_TOKENS'))
            self.max_context_tokens = int(self._get_required_env('PERFXCLOUD_MAX_CONTEXT_TOKENS'))
            
        elif provider == 'openai':
            self.model = f"openai/{self._get_required_env('OPENAI_MODEL')}"
            self.api_key = self._get_required_env('OPENAI_API_KEY')
            self.api_base = os.getenv('OPENAI_API_BASE')  # optional
            self.temperature = float(self._get_required_env('OPENAI_TEMPERATURE'))
            self.max_tokens = int(self._get_required_env('OPENAI_MAX_TOKENS'))
            self.max_context_tokens = None  # OpenAI自动管理
            
        elif provider == 'anthropic':
            self.model = f"anthropic/{self._get_required_env('ANTHROPIC_MODEL')}"
            self.api_key = self._get_required_env('ANTHROPIC_API_KEY')
            self.api_base = None
            self.temperature = float(self._get_required_env('ANTHROPIC_TEMPERATURE'))
            self.max_tokens = int(self._get_required_env('ANTHROPIC_MAX_TOKENS'))
            self.max_context_tokens = None
            
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def get_service_max_tokens(self, service_name: str) -> int:
        """
        获取特定服务的max_tokens配置
        
        Args:
            service_name: 服务名称，如 'story_planner', 'choreographer', 'animator'
            
        Returns:
            该服务的max_tokens，如果没有专门配置则返回通用配置
        """
        env_key = f"{self.provider.upper()}_{service_name.upper()}_MAX_TOKENS"
        service_max_tokens = os.getenv(env_key)
        
        if service_max_tokens:
            logger.debug(f"Using service-specific max_tokens for {service_name}: {service_max_tokens}")
            return int(service_max_tokens)
        
        logger.debug(f"Using default max_tokens for {service_name}: {self.max_tokens}")
        return self.max_tokens
    
    def completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        response_format: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Any:
        """
        调用LLM completion
        
        Args:
            messages: 消息列表
            max_tokens: 最大token数，如果不指定则使用配置值
            temperature: 温度参数，如果不指定则使用配置值
            response_format: 响应格式，如 {"type": "json_object"}
            **kwargs: 其他litellm参数
            
        Returns:
            LLM响应对象
        """
        request_params = {
            'model': self.model,
            'api_key': self.api_key,
            'messages': messages,
            'temperature': temperature if temperature is not None else self.temperature,
            'max_tokens': max_tokens if max_tokens is not None else self.max_tokens,
        }
        
        # 添加api_base（如果有）
        if self.api_base:
            request_params['api_base'] = self.api_base
        
        # 添加response_format（如果有）
        if response_format:
            request_params['response_format'] = response_format
        
        # 添加其他参数
        request_params.update(kwargs)
        
        logger.debug(f"Calling LLM: model={self.model}, max_tokens={request_params['max_tokens']}")
        
        try:
            response = litellm.completion(**request_params)
            return response
        except Exception as e:
            logger.error(f"LLM completion failed: {str(e)}")
            raise
    
    def get_config_summary(self) -> Dict[str, Any]:
        """获取配置摘要（用于调试）"""
        return {
            'provider': self.provider,
            'model': self.model,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'max_context_tokens': self.max_context_tokens,
            'api_base': self.api_base if self.api_base else 'default'
        }


# 单例模式（可选）
_global_client: Optional[LLMClient] = None


def get_llm_client(provider: Optional[str] = None) -> LLMClient:
    """
    获取全局LLM客户端实例（单例模式）
    
    Args:
        provider: LLM提供商，如果不指定则使用环境变量
        
    Returns:
        LLMClient实例
    """
    global _global_client
    
    if _global_client is None:
        _global_client = LLMClient(provider)
    
    return _global_client


def reset_llm_client():
    """重置全局客户端（主要用于测试）"""
    global _global_client
    _global_client = None

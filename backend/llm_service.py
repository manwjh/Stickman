"""
LLM Service - 统一 LLM 调用服务

使用 LiteLLM 作为统一接入层，支持多个 LLM 提供商。

支持的提供商:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude-3)
- PerfXCloud (Qwen)
- 更多 100+ 提供商...

Author: Your Name
License: MIT
"""
import os
import json
from typing import Dict, Any, Optional
import litellm
from .prompt_template import get_animation_prompt

# 配置 LiteLLM
litellm.suppress_debug_info = True  # 抑制调试信息
litellm.set_verbose = False  # 关闭详细日志


class LLMService:
    """Service for generating animations using LLM via LiteLLM"""
    
    def __init__(self):
        # 从环境变量读取配置
        self.provider = os.getenv('LLM_PROVIDER', 'openai').lower()
        self._setup_provider()
    
    def _setup_provider(self):
        """配置 LLM 提供商"""
        if self.provider == 'openai':
            self._setup_openai()
        elif self.provider == 'anthropic':
            self._setup_anthropic()
        elif self.provider == 'perfxcloud':
            self._setup_perfxcloud()
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _setup_openai(self):
        """配置 OpenAI"""
        self.model = f"openai/{os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')}"
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.api_base = os.getenv('OPENAI_API_BASE', None)
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '4096'))
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        # 设置 LiteLLM 环境变量
        os.environ['OPENAI_API_KEY'] = self.api_key
        if self.api_base:
            os.environ['OPENAI_API_BASE'] = self.api_base
    
    def _setup_anthropic(self):
        """配置 Anthropic"""
        self.model = f"anthropic/{os.getenv('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229')}"
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.api_base = os.getenv('ANTHROPIC_API_BASE', None)
        self.temperature = float(os.getenv('ANTHROPIC_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.getenv('ANTHROPIC_MAX_TOKENS', '4096'))
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        # 设置 LiteLLM 环境变量
        os.environ['ANTHROPIC_API_KEY'] = self.api_key
        if self.api_base:
            os.environ['ANTHROPIC_API_BASE'] = self.api_base
    
    def _setup_perfxcloud(self):
        """配置 PerfXCloud (OpenAI 兼容)"""
        self.model = os.getenv('PERFXCLOUD_MODEL', 'Qwen3-Next-80B-Instruct')
        self.api_key = os.getenv('PERFXCLOUD_API_KEY')
        self.api_base = os.getenv('PERFXCLOUD_API_BASE')
        self.temperature = float(os.getenv('PERFXCLOUD_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.getenv('PERFXCLOUD_MAX_TOKENS', '4096'))
        
        if not self.api_key:
            raise ValueError("PERFXCLOUD_API_KEY not found in environment")
        if not self.api_base:
            raise ValueError("PERFXCLOUD_API_BASE not found in environment")
        
        # LiteLLM 使用 openai/ 前缀配合 api_base 来调用 OpenAI 兼容接口
        self.model = f"openai/{self.model}"
    
    def generate_animation(self, story: str) -> Dict[str, Any]:
        """
        Generate animation from story description
        
        Args:
            story: Natural language story description
            
        Returns:
            Dict containing animation data with scenes and frames
        """
        prompt = get_animation_prompt(story)
        
        try:
            # 构建请求参数
            kwargs = {
                'model': self.model,
                'messages': [
                    {
                        "role": "system",
                        "content": "You are an expert animation generator. You convert story descriptions into precise SVG animation data. Always respond with valid JSON only, no additional text."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                'temperature': self.temperature,
                'max_tokens': self.max_tokens,
            }
            
            # 添加 API key
            kwargs['api_key'] = self.api_key
            
            # 如果是自定义 API base (PerfXCloud)
            if self.provider == 'perfxcloud':
                kwargs['api_base'] = self.api_base
            
            # 对于 OpenAI 和兼容接口，请求 JSON 格式
            if self.provider in ['openai', 'perfxcloud']:
                kwargs['response_format'] = {"type": "json_object"}
            
            # 调用 LiteLLM
            response = litellm.completion(**kwargs)
            
            # 解析响应
            content = response.choices[0].message.content
            
            # 对于 Anthropic，可能需要提取 JSON
            if self.provider == 'anthropic':
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
            
        except Exception as e:
            raise Exception(f"Error generating animation: {str(e)}")


# Singleton instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create LLM service singleton"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service

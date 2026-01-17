#!/usr/bin/env python3
"""
配置加载器 - 从 YAML 配置文件加载配置到环境变量

采用双配置文件设计:
- llm_config.yml: LLM API 令牌（敏感信息，不提交到Git）
- config.yml: 系统配置（可提交到Git）

使用方法:
    from backend.config_loader import load_config_to_env
    load_config_to_env()

Author: Your Name
License: MIT
"""
import os
import sys
import yaml
from pathlib import Path


class ConfigLoader:
    """配置加载器"""
    
    def __init__(self, config_file='config.yml', llm_config_file='llm_config.yml'):
        """
        初始化配置加载器
        
        Args:
            config_file: 系统配置文件路径
            llm_config_file: LLM令牌配置文件路径
        """
        self.config_file = Path(config_file)
        self.llm_config_file = Path(llm_config_file)
        self.config = None
        self.llm_config = None
    
    def load(self):
        """加载配置文件"""
        # 加载系统配置
        if not self.config_file.exists():
            raise FileNotFoundError(
                f"系统配置文件不存在: {self.config_file}\n"
                f"该文件应该存在于代码库中"
            )
        
        # 加载LLM令牌配置
        if not self.llm_config_file.exists():
            raise FileNotFoundError(
                f"LLM令牌配置文件不存在: {self.llm_config_file}\n"
                f"请复制 llm_config.example.yml 为 llm_config.yml 并填入API密钥"
            )
        
        try:
            # 读取系统配置
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            
            if not self.config:
                raise ValueError("系统配置文件为空")
            
            # 读取LLM令牌配置
            with open(self.llm_config_file, 'r', encoding='utf-8') as f:
                self.llm_config = yaml.safe_load(f)
            
            if not self.llm_config:
                raise ValueError("LLM令牌配置文件为空")
            
            return self.config, self.llm_config
        
        except yaml.YAMLError as e:
            raise ValueError(f"YAML解析错误: {e}")
        except Exception as e:
            raise Exception(f"加载配置文件失败: {e}")
    
    def to_env(self):
        """将配置转换为环境变量"""
        if not self.config or not self.llm_config:
            self.load()
        
        # LLM提供商配置
        llm_system_config = self.config.get('llm', {})
        provider = llm_system_config.get('provider', 'openai')
        os.environ['LLM_PROVIDER'] = provider
        
        # OpenAI配置
        if 'openai' in llm_system_config:
            openai_system = llm_system_config['openai']
            openai_tokens = self.llm_config.get('openai', {})
            
            # API密钥来自 llm_config.yml
            os.environ['OPENAI_API_KEY'] = openai_tokens.get('api_key', '')
            
            # 其他配置来自 config.yml
            os.environ['OPENAI_MODEL'] = openai_system.get('model', 'gpt-4-turbo-preview')
            os.environ['OPENAI_API_BASE'] = openai_system.get('api_base', '')
            os.environ['OPENAI_ORGANIZATION'] = openai_system.get('organization', '')
            os.environ['OPENAI_TIMEOUT'] = str(openai_system.get('timeout', 60))
            os.environ['OPENAI_MAX_RETRIES'] = str(openai_system.get('max_retries', 3))
            os.environ['OPENAI_TEMPERATURE'] = str(openai_system.get('temperature', 0.7))
        
        # Anthropic配置
        if 'anthropic' in llm_system_config:
            anthropic_system = llm_system_config['anthropic']
            anthropic_tokens = self.llm_config.get('anthropic', {})
            
            # API密钥来自 llm_config.yml
            os.environ['ANTHROPIC_API_KEY'] = anthropic_tokens.get('api_key', '')
            
            # 其他配置来自 config.yml
            os.environ['ANTHROPIC_MODEL'] = anthropic_system.get('model', 'claude-3-sonnet-20240229')
            os.environ['ANTHROPIC_API_BASE'] = anthropic_system.get('api_base', '')
            os.environ['ANTHROPIC_TIMEOUT'] = str(anthropic_system.get('timeout', 60))
            os.environ['ANTHROPIC_MAX_RETRIES'] = str(anthropic_system.get('max_retries', 3))
            os.environ['ANTHROPIC_TEMPERATURE'] = str(anthropic_system.get('temperature', 0.7))
            os.environ['ANTHROPIC_MAX_TOKENS'] = str(anthropic_system.get('max_tokens', 4096))
        
        # PerfXCloud配置
        if 'perfxcloud' in llm_system_config:
            perfxcloud_system = llm_system_config['perfxcloud']
            perfxcloud_tokens = self.llm_config.get('perfxcloud', {})
            
            # API密钥来自 llm_config.yml
            os.environ['PERFXCLOUD_API_KEY'] = perfxcloud_tokens.get('api_key', '')
            
            # 其他配置来自 config.yml
            os.environ['PERFXCLOUD_MODEL'] = perfxcloud_system.get('model', 'Qwen3-Next-80B-Instruct')
            os.environ['PERFXCLOUD_API_BASE'] = perfxcloud_system.get('api_base', '')
            os.environ['PERFXCLOUD_TIMEOUT'] = str(perfxcloud_system.get('timeout', 120))
            os.environ['PERFXCLOUD_MAX_RETRIES'] = str(perfxcloud_system.get('max_retries', 3))
            os.environ['PERFXCLOUD_TEMPERATURE'] = str(perfxcloud_system.get('temperature', 0.7))
            os.environ['PERFXCLOUD_MAX_TOKENS'] = str(perfxcloud_system.get('max_tokens', 4096))
            os.environ['PERFXCLOUD_MAX_CONTEXT_TOKENS'] = str(perfxcloud_system.get('max_context_tokens', 128000))
        
        # 服务器配置
        if 'server' in self.config:
            server_config = self.config['server']
            os.environ['FLASK_HOST'] = server_config.get('host', '0.0.0.0')
            os.environ['FLASK_PORT'] = str(server_config.get('port', 5000))
            os.environ['FLASK_DEBUG'] = str(server_config.get('debug', True))
            os.environ['SECRET_KEY'] = server_config.get('secret_key', 'dev-secret-key')
        
        # 动画配置
        if 'animation' in self.config:
            animation_config = self.config['animation']
            if 'canvas' in animation_config:
                os.environ['CANVAS_WIDTH'] = str(animation_config['canvas'].get('width', 800))
                os.environ['CANVAS_HEIGHT'] = str(animation_config['canvas'].get('height', 600))
            
            if 'colors' in animation_config:
                os.environ['DEFAULT_COLORS'] = ','.join(animation_config['colors'])
            
            os.environ['MAX_SCENES'] = str(animation_config.get('max_scenes', 10))
            os.environ['MAX_CHARACTERS'] = str(animation_config.get('max_characters', 5))
            os.environ['MAX_FRAMES_PER_SCENE'] = str(animation_config.get('max_frames_per_scene', 20))
        
        # 日志配置
        if 'logging' in self.config:
            logging_config = self.config['logging']
            os.environ['LOG_LEVEL'] = logging_config.get('level', 'INFO')
            os.environ['LOG_FORMAT'] = logging_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            os.environ['LOG_FILE'] = logging_config.get('file', '')
    
    def validate(self):
        """验证配置"""
        if not self.config or not self.llm_config:
            self.load()
        
        errors = []
        
        # 验证LLM配置
        llm_system_config = self.config.get('llm', {})
        provider = llm_system_config.get('provider')
        
        if not provider:
            errors.append("未指定LLM提供商 (config.yml -> llm.provider)")
        elif provider not in ['openai', 'anthropic', 'perfxcloud', 'custom']:
            errors.append(f"不支持的LLM提供商: {provider}")
        
        # 验证选定提供商的API密钥
        if provider == 'openai':
            api_key = self.llm_config.get('openai', {}).get('api_key', '')
            if not api_key or 'your_' in api_key:
                errors.append("未配置OpenAI API密钥 (llm_config.yml -> openai.api_key)")
        
        elif provider == 'anthropic':
            api_key = self.llm_config.get('anthropic', {}).get('api_key', '')
            if not api_key or 'your_' in api_key:
                errors.append("未配置Anthropic API密钥 (llm_config.yml -> anthropic.api_key)")
        
        elif provider == 'perfxcloud':
            api_key = self.llm_config.get('perfxcloud', {}).get('api_key', '')
            if not api_key or 'your_' in api_key:
                errors.append("未配置PerfXCloud API密钥 (llm_config.yml -> perfxcloud.api_key)")
        
        if errors:
            raise ValueError("配置验证失败:\n" + "\n".join(f"  - {e}" for e in errors))
        
        return True
    
    def get(self, key_path, default=None, from_llm_config=False):
        """
        获取配置值
        
        Args:
            key_path: 配置路径，如 'llm.openai.model'
            default: 默认值
            from_llm_config: 是否从LLM配置读取
            
        Returns:
            配置值
        """
        if not self.config or not self.llm_config:
            self.load()
        
        source = self.llm_config if from_llm_config else self.config
        keys = key_path.split('.')
        value = source
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def display(self):
        """显示当前配置（隐藏敏感信息）"""
        if not self.config or not self.llm_config:
            self.load()
        
        def mask_sensitive(obj, path=''):
            """递归遮蔽敏感信息"""
            if isinstance(obj, dict):
                result = {}
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if 'key' in key.lower() or 'secret' in key.lower():
                        if value and len(str(value)) > 8:
                            result[key] = str(value)[:4] + '***' + str(value)[-4:]
                        else:
                            result[key] = '***'
                    else:
                        result[key] = mask_sensitive(value, current_path)
                return result
            elif isinstance(obj, list):
                return [mask_sensitive(item, path) for item in obj]
            else:
                return obj
        
        import json
        
        display_config = {
            'system_config': mask_sensitive(self.config),
            'llm_tokens': mask_sensitive(self.llm_config)
        }
        
        return json.dumps(display_config, indent=2, ensure_ascii=False)


def load_config_to_env(config_file='config.yml', llm_config_file='llm_config.yml'):
    """
    加载配置到环境变量（便捷函数）
    
    Args:
        config_file: 系统配置文件路径
        llm_config_file: LLM令牌配置文件路径
    """
    loader = ConfigLoader(config_file, llm_config_file)
    loader.load()
    loader.validate()
    loader.to_env()
    return loader


# 导出
__all__ = ['ConfigLoader', 'load_config_to_env']


if __name__ == '__main__':
    """测试配置加载"""
    print("=" * 60)
    print("🔧 配置加载器测试")
    print("=" * 60)
    print()
    
    try:
        loader = ConfigLoader()
        
        print("1️⃣  加载配置文件...")
        loader.load()
        print("   ✅ 系统配置: config.yml")
        print("   ✅ LLM令牌: llm_config.yml")
        print()
        
        print("2️⃣  验证配置...")
        loader.validate()
        print("   ✅ 配置验证通过")
        print()
        
        print("3️⃣  转换为环境变量...")
        loader.to_env()
        print("   ✅ 环境变量设置完成")
        print()
        
        print("4️⃣  当前配置（敏感信息已遮蔽）:")
        print(loader.display())
        print()
        
        print("=" * 60)
        print("✅ 配置加载测试完成")
        print("=" * 60)
        print()
        print("配置文件说明:")
        print("  - config.yml: 系统配置（可提交到Git）")
        print("  - llm_config.yml: API令牌（不提交到Git）")
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)

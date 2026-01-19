#!/usr/bin/env python3
"""
Configuration Loader - Load configuration from YAML files to environment variables

Configuration design:
- llm_config.yml: LLM API tokens (set via set_env.sh script to environment variables)
- config.yml: System configuration (loaded by this module)

API Keys are ONLY read from environment variables set by set_env.sh script.
No fallback values provided - missing keys will cause immediate failure.

Usage:
    # Step 1: Set API keys to environment (run once per shell session)
    source ./set_env.sh
    
    # Step 2: Load system configuration
    from backend.config_loader import load_config_to_env
    load_config_to_env()

Author: Shenzhen Wang & AI
License: MIT
"""
import os
import sys
import yaml
from pathlib import Path


class ConfigLoader:
    """Configuration loader - reads system config and API keys from environment"""
    
    def __init__(self, config_file='config.yml'):
        """
        Initialize configuration loader
        
        Args:
            config_file: System configuration file path
        """
        self.config_file = Path(config_file)
        self.config = None
    
    def load(self):
        """Load system configuration file"""
        # Load system configuration
        if not self.config_file.exists():
            raise FileNotFoundError(
                f"System configuration file not found: {self.config_file}\n"
                f"This file should exist in the codebase"
            )
        
        try:
            # Read system configuration
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            
            if not self.config:
                raise ValueError("System configuration file is empty")
            
            return self.config
        
        except yaml.YAMLError as e:
            raise ValueError(f"YAML parsing error: {e}")
        except Exception as e:
            raise Exception(f"Failed to load configuration file: {e}")
    
    def to_env(self):
        """
        Convert configuration to environment variables
        
        Note: API keys MUST be already set in environment by set_env.py script.
        This method only sets non-sensitive configuration from config.yml.
        """
        if not self.config:
            self.load()
        
        # LLM provider configuration
        llm_system_config = self.config.get('llm', {})
        provider = llm_system_config.get('provider', 'openai')
        os.environ['LLM_PROVIDER'] = provider
        
        # OpenAI configuration
        if 'openai' in llm_system_config:
            openai_system = llm_system_config['openai']
            
            # API key MUST be already set by set_env.py - no fallback
            # We do NOT set OPENAI_API_KEY here
            
            # Other configs from config.yml
            os.environ['OPENAI_MODEL'] = openai_system.get('model', 'gpt-4-turbo-preview')
            os.environ['OPENAI_API_BASE'] = openai_system.get('api_base', '')
            os.environ['OPENAI_ORGANIZATION'] = openai_system.get('organization', '')
            os.environ['OPENAI_TIMEOUT'] = str(openai_system.get('timeout', 60))
            os.environ['OPENAI_MAX_RETRIES'] = str(openai_system.get('max_retries', 3))
            os.environ['OPENAI_TEMPERATURE'] = str(openai_system.get('temperature', 0.7))
            os.environ['OPENAI_MAX_TOKENS'] = str(openai_system.get('max_tokens', 16384))
        
        # Anthropic configuration
        if 'anthropic' in llm_system_config:
            anthropic_system = llm_system_config['anthropic']
            
            # API key MUST be already set by set_env.py - no fallback
            # We do NOT set ANTHROPIC_API_KEY here
            
            # Other configs from config.yml
            os.environ['ANTHROPIC_MODEL'] = anthropic_system.get('model', 'claude-3-sonnet-20240229')
            os.environ['ANTHROPIC_API_BASE'] = anthropic_system.get('api_base', '')
            os.environ['ANTHROPIC_TIMEOUT'] = str(anthropic_system.get('timeout', 60))
            os.environ['ANTHROPIC_MAX_RETRIES'] = str(anthropic_system.get('max_retries', 3))
            os.environ['ANTHROPIC_TEMPERATURE'] = str(anthropic_system.get('temperature', 0.7))
            os.environ['ANTHROPIC_MAX_TOKENS'] = str(anthropic_system.get('max_tokens', 16384))
        
        # PerfXCloud configuration
        if 'perfxcloud' in llm_system_config:
            perfxcloud_system = llm_system_config['perfxcloud']
            
            # API key MUST be already set by set_env.py - no fallback
            # We do NOT set PERFXCLOUD_API_KEY here
            
            # Other configs from config.yml
            os.environ['PERFXCLOUD_MODEL'] = perfxcloud_system.get('model', 'Qwen3-Next-80B-Instruct')
            os.environ['PERFXCLOUD_API_BASE'] = perfxcloud_system.get('api_base', '')
            os.environ['PERFXCLOUD_TIMEOUT'] = str(perfxcloud_system.get('timeout', 120))
            os.environ['PERFXCLOUD_MAX_RETRIES'] = str(perfxcloud_system.get('max_retries', 3))
            os.environ['PERFXCLOUD_TEMPERATURE'] = str(perfxcloud_system.get('temperature', 0.7))
            os.environ['PERFXCLOUD_MAX_TOKENS'] = str(perfxcloud_system.get('max_tokens', 16384))
            os.environ['PERFXCLOUD_MAX_CONTEXT_TOKENS'] = str(perfxcloud_system.get('max_context_tokens', 128000))
            
            # 各服务的专门配置（如不设置则使用通用max_tokens）
            default_max_tokens = perfxcloud_system.get('max_tokens', 16384)
            os.environ['PERFXCLOUD_STORY_PLANNER_MAX_TOKENS'] = str(
                perfxcloud_system.get('story_planner_max_tokens', default_max_tokens)
            )
            os.environ['PERFXCLOUD_CHOREOGRAPHER_MAX_TOKENS'] = str(
                perfxcloud_system.get('choreographer_max_tokens', default_max_tokens)
            )
            os.environ['PERFXCLOUD_ANIMATOR_MAX_TOKENS'] = str(
                perfxcloud_system.get('animator_max_tokens', default_max_tokens)
            )
        
        # Server configuration
        if 'server' in self.config:
            server_config = self.config['server']
            os.environ['FLASK_HOST'] = server_config.get('host', '0.0.0.0')
            os.environ['FLASK_PORT'] = str(server_config.get('port', 5000))
            os.environ['FLASK_DEBUG'] = str(server_config.get('debug', True))
            os.environ['SECRET_KEY'] = server_config.get('secret_key', 'dev-secret-key')
        
        # Animation configuration
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
        
        # Logging configuration
        if 'logging' in self.config:
            logging_config = self.config['logging']
            os.environ['LOG_LEVEL'] = logging_config.get('level', 'INFO')
            os.environ['LOG_FORMAT'] = logging_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            os.environ['LOG_FILE'] = logging_config.get('file', '')
    
    def validate(self):
        """
        Validate configuration
        
        Checks that:
        1. System configuration is valid
        2. API keys are set in environment variables (by set_env.py)
        
        Raises ValueError if validation fails.
        """
        if not self.config:
            self.load()
        
        errors = []
        
        # Validate LLM configuration
        llm_system_config = self.config.get('llm', {})
        provider = llm_system_config.get('provider')
        
        if not provider:
            errors.append("LLM provider not specified (config.yml -> llm.provider)")
        elif provider not in ['openai', 'anthropic', 'perfxcloud', 'custom']:
            errors.append(f"Unsupported LLM provider: {provider}")
        
        # Validate API key from ENVIRONMENT VARIABLES (set by set_env.py)
        # NO fallback - if not in environment, fail immediately
        if provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                errors.append(
                    "OPENAI_API_KEY not found in environment variables.\n"
                    "  Please run: source ./set_env.sh"
                )
        
        elif provider == 'anthropic':
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                errors.append(
                    "ANTHROPIC_API_KEY not found in environment variables.\n"
                    "  Please run: source ./set_env.sh"
                )
        
        elif provider == 'perfxcloud':
            api_key = os.getenv('PERFXCLOUD_API_KEY')
            if not api_key:
                errors.append(
                    "PERFXCLOUD_API_KEY not found in environment variables.\n"
                    "  Please run: source ./set_env.sh"
                )
        
        if errors:
            raise ValueError("Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
        
        return True
    
    def get(self, key_path, default=None):
        """
        Get configuration value from system config
        
        Args:
            key_path: Configuration path, e.g. 'llm.openai.model'
            default: Default value
            
        Returns:
            Configuration value
        """
        if not self.config:
            self.load()
        
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def display(self):
        """Display current configuration (mask sensitive information)"""
        if not self.config:
            self.load()
        
        def mask_sensitive(obj, path=''):
            """Recursively mask sensitive information"""
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
        
        # Get API keys from environment (masked)
        env_keys = {}
        for key in ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'PERFXCLOUD_API_KEY']:
            value = os.getenv(key)
            if value:
                if len(value) > 8:
                    env_keys[key] = value[:4] + '***' + value[-4:]
                else:
                    env_keys[key] = '***'
            else:
                env_keys[key] = 'NOT_SET'
        
        display_config = {
            'system_config': mask_sensitive(self.config),
            'environment_api_keys': env_keys
        }
        
        return json.dumps(display_config, indent=2, ensure_ascii=False)


def load_config_to_env(config_file='config.yml'):
    """
    Load configuration to environment variables (convenience function)
    
    Note: API keys must be already set in environment by set_env.py script.
    
    Args:
        config_file: System configuration file path
    """
    loader = ConfigLoader(config_file)
    loader.load()
    loader.validate()
    loader.to_env()
    return loader


# Export
__all__ = ['ConfigLoader', 'load_config_to_env']


if __name__ == '__main__':
    """Test configuration loader"""
    print("=" * 60)
    print("🔧 Configuration Loader Test")
    print("=" * 60)
    print()
    
    try:
        loader = ConfigLoader()
        
        print("1️⃣  Loading system configuration...")
        loader.load()
        print("   ✅ System config: config.yml")
        print()
        
        print("2️⃣  Validating configuration...")
        print("   Checking environment variables for API keys...")
        loader.validate()
        print("   ✅ Configuration validation passed")
        print()
        
        print("3️⃣  Converting to environment variables...")
        loader.to_env()
        print("   ✅ Environment variables set")
        print()
        
        print("4️⃣  Current configuration (sensitive info masked):")
        print(loader.display())
        print()
        
        print("=" * 60)
        print("✅ Configuration loader test completed")
        print("=" * 60)
        print()
        print("Configuration setup:")
        print("  - Step 1: Run 'source ./set_env.sh' to set API keys")
        print("  - Step 2: config.yml provides system configuration")
        print("  - API keys are ONLY read from environment variables")
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

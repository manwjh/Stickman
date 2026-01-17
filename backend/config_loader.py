#!/usr/bin/env python3
"""
Configuration Loader - Load configuration from YAML files to environment variables

Uses a dual configuration file design:
- llm_config.yml: LLM API tokens (sensitive info, not committed to Git)
- config.yml: System configuration (can be committed to Git)

Usage:
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
    """Configuration loader"""
    
    def __init__(self, config_file='config.yml', llm_config_file='llm_config.yml'):
        """
        Initialize configuration loader
        
        Args:
            config_file: System configuration file path
            llm_config_file: LLM token configuration file path
        """
        self.config_file = Path(config_file)
        self.llm_config_file = Path(llm_config_file)
        self.config = None
        self.llm_config = None
    
    def load(self):
        """Load configuration files"""
        # Load system configuration
        if not self.config_file.exists():
            raise FileNotFoundError(
                f"System configuration file not found: {self.config_file}\n"
                f"This file should exist in the codebase"
            )
        
        # Load LLM token configuration
        if not self.llm_config_file.exists():
            raise FileNotFoundError(
                f"LLM token configuration file not found: {self.llm_config_file}\n"
                f"Please copy llm_config.example.yml to llm_config.yml and fill in your API key"
            )
        
        try:
            # Read system configuration
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            
            if not self.config:
                raise ValueError("System configuration file is empty")
            
            # Read LLM token configuration
            with open(self.llm_config_file, 'r', encoding='utf-8') as f:
                self.llm_config = yaml.safe_load(f)
            
            if not self.llm_config:
                raise ValueError("LLM token configuration file is empty")
            
            return self.config, self.llm_config
        
        except yaml.YAMLError as e:
            raise ValueError(f"YAML parsing error: {e}")
        except Exception as e:
            raise Exception(f"Failed to load configuration files: {e}")
    
    def to_env(self):
        """Convert configuration to environment variables"""
        if not self.config or not self.llm_config:
            self.load()
        
        # LLM provider configuration
        llm_system_config = self.config.get('llm', {})
        provider = llm_system_config.get('provider', 'openai')
        os.environ['LLM_PROVIDER'] = provider
        
        # OpenAI configuration
        if 'openai' in llm_system_config:
            openai_system = llm_system_config['openai']
            openai_tokens = self.llm_config.get('openai', {})
            
            # API key from llm_config.yml
            os.environ['OPENAI_API_KEY'] = openai_tokens.get('api_key', '')
            
            # Other configs from config.yml
            os.environ['OPENAI_MODEL'] = openai_system.get('model', 'gpt-4-turbo-preview')
            os.environ['OPENAI_API_BASE'] = openai_system.get('api_base', '')
            os.environ['OPENAI_ORGANIZATION'] = openai_system.get('organization', '')
            os.environ['OPENAI_TIMEOUT'] = str(openai_system.get('timeout', 60))
            os.environ['OPENAI_MAX_RETRIES'] = str(openai_system.get('max_retries', 3))
            os.environ['OPENAI_TEMPERATURE'] = str(openai_system.get('temperature', 0.7))
        
        # Anthropic configuration
        if 'anthropic' in llm_system_config:
            anthropic_system = llm_system_config['anthropic']
            anthropic_tokens = self.llm_config.get('anthropic', {})
            
            # API key from llm_config.yml
            os.environ['ANTHROPIC_API_KEY'] = anthropic_tokens.get('api_key', '')
            
            # Other configs from config.yml
            os.environ['ANTHROPIC_MODEL'] = anthropic_system.get('model', 'claude-3-sonnet-20240229')
            os.environ['ANTHROPIC_API_BASE'] = anthropic_system.get('api_base', '')
            os.environ['ANTHROPIC_TIMEOUT'] = str(anthropic_system.get('timeout', 60))
            os.environ['ANTHROPIC_MAX_RETRIES'] = str(anthropic_system.get('max_retries', 3))
            os.environ['ANTHROPIC_TEMPERATURE'] = str(anthropic_system.get('temperature', 0.7))
            os.environ['ANTHROPIC_MAX_TOKENS'] = str(anthropic_system.get('max_tokens', 4096))
        
        # PerfXCloud configuration
        if 'perfxcloud' in llm_system_config:
            perfxcloud_system = llm_system_config['perfxcloud']
            perfxcloud_tokens = self.llm_config.get('perfxcloud', {})
            
            # API key from llm_config.yml
            os.environ['PERFXCLOUD_API_KEY'] = perfxcloud_tokens.get('api_key', '')
            
            # Other configs from config.yml
            os.environ['PERFXCLOUD_MODEL'] = perfxcloud_system.get('model', 'Qwen3-Next-80B-Instruct')
            os.environ['PERFXCLOUD_API_BASE'] = perfxcloud_system.get('api_base', '')
            os.environ['PERFXCLOUD_TIMEOUT'] = str(perfxcloud_system.get('timeout', 120))
            os.environ['PERFXCLOUD_MAX_RETRIES'] = str(perfxcloud_system.get('max_retries', 3))
            os.environ['PERFXCLOUD_TEMPERATURE'] = str(perfxcloud_system.get('temperature', 0.7))
            os.environ['PERFXCLOUD_MAX_TOKENS'] = str(perfxcloud_system.get('max_tokens', 4096))
            os.environ['PERFXCLOUD_MAX_CONTEXT_TOKENS'] = str(perfxcloud_system.get('max_context_tokens', 128000))
        
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
        """Validate configuration"""
        if not self.config or not self.llm_config:
            self.load()
        
        errors = []
        
        # Validate LLM configuration
        llm_system_config = self.config.get('llm', {})
        provider = llm_system_config.get('provider')
        
        if not provider:
            errors.append("LLM provider not specified (config.yml -> llm.provider)")
        elif provider not in ['openai', 'anthropic', 'perfxcloud', 'custom']:
            errors.append(f"Unsupported LLM provider: {provider}")
        
        # Validate API key for selected provider
        if provider == 'openai':
            api_key = self.llm_config.get('openai', {}).get('api_key', '')
            if not api_key or 'your_' in api_key:
                errors.append("OpenAI API key not configured (llm_config.yml -> openai.api_key)")
        
        elif provider == 'anthropic':
            api_key = self.llm_config.get('anthropic', {}).get('api_key', '')
            if not api_key or 'your_' in api_key:
                errors.append("Anthropic API key not configured (llm_config.yml -> anthropic.api_key)")
        
        elif provider == 'perfxcloud':
            api_key = self.llm_config.get('perfxcloud', {}).get('api_key', '')
            if not api_key or 'your_' in api_key:
                errors.append("PerfXCloud API key not configured (llm_config.yml -> perfxcloud.api_key)")
        
        if errors:
            raise ValueError("Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
        
        return True
    
    def get(self, key_path, default=None, from_llm_config=False):
        """
        Get configuration value
        
        Args:
            key_path: Configuration path, e.g. 'llm.openai.model'
            default: Default value
            from_llm_config: Whether to read from LLM config
            
        Returns:
            Configuration value
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
        """Display current configuration (mask sensitive information)"""
        if not self.config or not self.llm_config:
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
        
        display_config = {
            'system_config': mask_sensitive(self.config),
            'llm_tokens': mask_sensitive(self.llm_config)
        }
        
        return json.dumps(display_config, indent=2, ensure_ascii=False)


def load_config_to_env(config_file='config.yml', llm_config_file='llm_config.yml'):
    """
    Load configuration to environment variables (convenience function)
    
    Args:
        config_file: System configuration file path
        llm_config_file: LLM token configuration file path
    """
    loader = ConfigLoader(config_file, llm_config_file)
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
        
        print("1️⃣  Loading configuration files...")
        loader.load()
        print("   ✅ System config: config.yml")
        print("   ✅ LLM tokens: llm_config.yml")
        print()
        
        print("2️⃣  Validating configuration...")
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
        print("Configuration file description:")
        print("  - config.yml: System configuration (can be committed to Git)")
        print("  - llm_config.yml: API tokens (not committed to Git)")
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

# Configuration Guide

[中文](../zh-CN/CONFIG.md) | English

This guide explains all configuration options for the AI Stick Figure Story Animator.

## Table of Contents

- [Overview](#overview)
- [Configuration Files](#configuration-files)
- [LLM Provider Configuration](#llm-provider-configuration)
- [Server Configuration](#server-configuration)
- [Animation Settings](#animation-settings)
- [Logging Configuration](#logging-configuration)

## Overview

The application uses a **two-file configuration system**:

1. **`config.yml`** - System configuration (can be committed to Git)
2. **`llm_config.yml`** - API keys and sensitive data (should NOT be committed)

This separation keeps sensitive information secure while allowing you to version control system settings.

## Configuration Files

### config.yml (System Configuration)

Location: Project root directory

Contains non-sensitive configuration:
- LLM provider selection
- Model parameters
- Server settings
- Animation limits
- Logging options

**Example:**

```yaml
llm:
  provider: openai
  
  openai:
    model: gpt-4-turbo-preview
    temperature: 0.7
    max_tokens: 4096
    timeout: 60
    max_retries: 3

server:
  host: 0.0.0.0
  port: 5001
  debug: true

animation:
  canvas:
    width: 800
    height: 600
  colors:
    - "#2196F3"
    - "#4CAF50"
    - "#FF9800"
  max_scenes: 10
  max_characters: 5

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### llm_config.yml (API Keys)

Location: Project root directory (gitignored)

Contains sensitive information:
- API keys
- Access tokens
- Credentials

**Example:**

```yaml
openai:
  api_key: "sk-your-api-key-here"

anthropic:
  api_key: "your-anthropic-key"

perfxcloud:
  api_key: "your-perfx-key"
```

**⚠️ Important:** Never commit `llm_config.yml` to Git! It's already in `.gitignore`.

## LLM Provider Configuration

### OpenAI

```yaml
# config.yml
llm:
  provider: openai
  openai:
    model: gpt-4-turbo-preview  # or gpt-3.5-turbo
    temperature: 0.7            # 0.0-2.0, controls randomness
    max_tokens: 4096            # Maximum response length
    timeout: 60                 # Request timeout in seconds
    max_retries: 3              # Number of retry attempts
    api_base: ""                # Optional: custom API endpoint
    organization: ""            # Optional: OpenAI organization ID

# llm_config.yml
openai:
  api_key: "sk-your-key-here"
```

**Recommended Models:**
- `gpt-4-turbo-preview` - Best quality, slower
- `gpt-3.5-turbo` - Fast and cost-effective

### Anthropic (Claude)

```yaml
# config.yml
llm:
  provider: anthropic
  anthropic:
    model: claude-3-sonnet-20240229
    temperature: 0.7
    max_tokens: 4096
    timeout: 60

# llm_config.yml
anthropic:
  api_key: "your-anthropic-key"
```

### PerfXCloud (Qwen)

```yaml
# config.yml
llm:
  provider: perfxcloud
  perfxcloud:
    model: Qwen3-Next-80B-Instruct
    api_base: https://api.perfxcloud.com/v1
    temperature: 0.7
    max_tokens: 4096

# llm_config.yml
perfxcloud:
  api_key: "your-perfx-key"
```

## Server Configuration

```yaml
server:
  host: 0.0.0.0           # Listen address (0.0.0.0 = all interfaces)
  port: 5001              # Server port
  debug: true             # Enable debug mode
  secret_key: "your-secret-key"  # Flask secret key
```

**Settings:**

- **host**: 
  - `0.0.0.0` - Accessible from network
  - `127.0.0.1` - Localhost only
  
- **port**: Choose an available port (default: 5001)

- **debug**: 
  - `true` - Development mode (auto-reload, detailed errors)
  - `false` - Production mode

- **secret_key**: Change this in production!

## Animation Settings

```yaml
animation:
  canvas:
    width: 800            # Canvas width in pixels
    height: 600           # Canvas height in pixels
  
  colors:                 # Default character colors
    - "#2196F3"           # Blue
    - "#4CAF50"           # Green
    - "#FF9800"           # Orange
    - "#E91E63"           # Pink
    - "#9C27B0"           # Purple
  
  max_scenes: 10          # Maximum number of scenes
  max_characters: 5       # Maximum number of characters
  max_frames_per_scene: 20  # Maximum frames per scene
```

## Logging Configuration

```yaml
logging:
  level: INFO             # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: ""                # Optional: log file path
```

**Log Levels:**

- `DEBUG` - Detailed information, useful for debugging
- `INFO` - General informational messages
- `WARNING` - Warning messages (default)
- `ERROR` - Error messages
- `CRITICAL` - Critical issues

**Example with log file:**

```yaml
logging:
  level: DEBUG
  file: "logs/app.log"
```

## Environment Variables

You can override configuration using environment variables:

```bash
# LLM Configuration
export LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-your-key
export OPENAI_MODEL=gpt-4

# Server Configuration
export FLASK_HOST=0.0.0.0
export FLASK_PORT=5001
export FLASK_DEBUG=true

# Logging
export LOG_LEVEL=DEBUG
```

Environment variables take precedence over YAML configuration.

## Best Practices

### Security

1. **Never commit API keys** - Keep `llm_config.yml` in `.gitignore`
2. **Use environment variables** in production
3. **Rotate keys regularly** 
4. **Set strong secret_key** for production

### Performance

1. **Use GPT-3.5** for faster generation
2. **Adjust max_tokens** based on needs
3. **Set reasonable timeouts** for your network
4. **Enable logging** to diagnose issues

### Development

1. **Enable debug mode** during development
2. **Use INFO or DEBUG** log level
3. **Keep separate configs** for dev/prod
4. **Test with different models** to optimize

## Validation

The application validates configuration on startup:

```
✅ Configuration validation passed
❌ OpenAI API key not configured
❌ Unsupported LLM provider: xyz
```

Fix any errors before running the application.

## Testing Configuration

Test your configuration:

```bash
python backend/config_loader.py
```

This will display your configuration with sensitive data masked.

## Troubleshooting

### "Configuration file not found"

**Solution**: Copy the example file:
```bash
cp llm_config.example.yml llm_config.yml
```

### "API key not configured"

**Solution**: Edit `llm_config.yml` and add your actual API key.

### "Configuration validation failed"

**Solution**: Check error messages and fix the specified configuration values.

### Changes not taking effect

**Solution**: Restart the application after changing configuration files.

## Related Documentation

- [Getting Started](GETTING_STARTED.md)
- [API Documentation](API.md)
- [Development Guide](DEVELOPMENT.md)

---

For more help, see [Troubleshooting](GETTING_STARTED.md#troubleshooting) or [create an issue](https://github.com/your-repo/issues).

# 📋 配置指南

## 概述

本项目采用**双配置文件**设计：

- `config.yml` - 系统配置（可提交到 Git）
- `llm_config.yml` - API 密钥（不提交到 Git）

## 快速配置

### 1. 复制示例配置

```bash
cp llm_config.example.yml llm_config.yml
```

### 2. 填入 API 密钥

编辑 `llm_config.yml`:

```yaml
openai:
  api_key: "sk-your-actual-key"

anthropic:
  api_key: "sk-ant-your-key"

perfxcloud:
  api_key: "sk-your-key"
```

### 3. 选择 LLM 提供商

编辑 `config.yml`:

```yaml
llm:
  provider: openai  # 或 anthropic, perfxcloud
```

## 配置文件说明

### config.yml

**系统配置文件** - 可以提交到 Git

```yaml
# LLM 提供商
llm:
  provider: openai
  
  openai:
    model: "gpt-4-turbo-preview"
    api_base: ""
    temperature: 0.7
    max_tokens: 4096
  
  anthropic:
    model: "claude-3-sonnet-20240229"
    temperature: 0.7
    max_tokens: 4096
  
  perfxcloud:
    model: "Qwen3-Next-80B-Instruct"
    api_base: "https://deepseek.perfxlab.cn/v1"
    temperature: 0.7
    max_tokens: 4096

# 服务器配置
server:
  host: "0.0.0.0"
  port: 5001
  debug: true

# 动画配置
animation:
  canvas:
    width: 800
    height: 600
  max_scenes: 10
  max_characters: 5

# 日志配置
logging:
  level: "INFO"
  file: ""
```

### llm_config.yml

**敏感信息文件** - 不提交到 Git

```yaml
openai:
  api_key: "sk-your-key"

anthropic:
  api_key: "sk-ant-your-key"

perfxcloud:
  api_key: "sk-your-key"
```

## LLM 提供商配置

### OpenAI

```yaml
# config.yml
llm:
  provider: openai
  openai:
    model: "gpt-4-turbo-preview"  # 或 gpt-3.5-turbo
    temperature: 0.7
    max_tokens: 4096

# llm_config.yml
openai:
  api_key: "sk-your-openai-key"
```

获取密钥: https://platform.openai.com/api-keys

### Anthropic Claude

```yaml
# config.yml
llm:
  provider: anthropic
  anthropic:
    model: "claude-3-sonnet-20240229"
    temperature: 0.7
    max_tokens: 4096

# llm_config.yml
anthropic:
  api_key: "sk-ant-your-anthropic-key"
```

获取密钥: https://console.anthropic.com/

### PerfXCloud

```yaml
# config.yml
llm:
  provider: perfxcloud
  perfxcloud:
    model: "Qwen3-Next-80B-Instruct"
    api_base: "https://deepseek.perfxlab.cn/v1"
    temperature: 0.7
    max_tokens: 4096

# llm_config.yml
perfxcloud:
  api_key: "sk-your-perfxcloud-key"
```

## 常见配置

### 使用代理

```yaml
llm:
  openai:
    api_base: "https://your-proxy.com/v1"
```

### 更改端口

```yaml
server:
  port: 8080
```

### 生产环境

```yaml
server:
  debug: false
  secret_key: "your-strong-secret-key"

logging:
  level: "WARNING"
  file: "/var/log/stick_figure/app.log"
```

## 测试配置

```bash
python backend/config_loader.py
```

## 安全建议

1. ✅ 永远不要提交 `llm_config.yml`
2. ✅ 使用强密钥作为 `secret_key`
3. ✅ 生产环境关闭 `debug`
4. ✅ 定期轮换 API 密钥

## 更多信息

- [快速开始](GETTING_STARTED.md)
- [API 文档](API.md)
- [开发文档](DEVELOPMENT.md)

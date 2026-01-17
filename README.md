# 🎬 AI 火柴人故事动画生成器

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-1.57+-green.svg)](https://github.com/BerriAI/litellm)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 通过自然语言描述故事情节，让 AI 自动生成流畅的火柴人 SVG 动画

## ✨ 特性

- 🤖 **完全 AI 驱动** - 动作由 LLM 实时生成，无需预定义模板
- 🎭 **自然语言输入** - 用中文描述故事，AI 自动转换为动画
- 🔌 **统一接入层** - LiteLLM 支持 100+ LLM 提供商
- 🎨 **专业动画** - SVG 矢量图形 + GSAP 动画引擎
- 🌐 **现代化界面** - 响应式 Web UI，即时预览
- ⚙️ **灵活配置** - YAML 配置，敏感信息分离

## 🚀 快速开始

### 1. 安装依赖

```bash
# 复制并编辑配置
cp llm_config.example.yml llm_config.yml

# 编辑 llm_config.yml 填入你的 API 密钥
# openai.api_key: "sk-your-key-here"

# 安装依赖
pip install -r requirements.txt
```

### 2. 启动应用

```bash
# 方式 1: 使用启动脚本
./start.sh              # macOS/Linux
start.bat               # Windows

# 方式 2: 直接启动
python3 app.py
```

### 3. 访问应用

打开浏览器访问: **http://localhost:5001**

## 💡 使用示例

### 简单场景
```
一个人站着，然后挥手打招呼
```

### 复杂场景
```
小明从左边跑到右边，看到一个球，兴奋地跳起来，然后弯腰捡起球，高兴地举起球庆祝
```

### 多角色场景
```
小明站在左边，小红站在右边。他们走向对方，挥手打招呼，最后击掌庆祝
```

### 武术场景
```
小明拿着刀表演了一段武术动作
```

## 🏗️ 项目结构

```
stick_figure/
├── app.py                      # Flask 主应用
├── requirements.txt            # Python 依赖
├── config.yml                  # 系统配置 (可提交)
├── llm_config.yml             # API 令牌 (不提交)
│
├── backend/                    # 后端服务
│   ├── config_loader.py       # 配置加载器
│   ├── llm_service.py         # LLM 服务 (LiteLLM)
│   ├── prompt_template.py     # Prompt 模板
│   └── animation_validator.py # 数据验证
│
├── templates/                  # HTML 模板
│   └── index.html
│
├── static/                     # 静态资源
│   ├── css/style.css
│   └── js/
│       ├── animator.js        # SVG 动画引擎
│       └── app.js             # 前端逻辑
│
└── docs/                       # 文档目录
    ├── API.md                 # API 文档
    ├── CONFIG.md              # 配置指南
    ├── DEVELOPMENT.md         # 开发文档
    └── ARCHITECTURE.md        # 架构说明
```

## ⚙️ 配置说明

### config.yml (系统配置)
```yaml
llm:
  provider: openai              # 或 anthropic, perfxcloud
  openai:
    model: gpt-4-turbo-preview
    temperature: 0.7
    max_tokens: 4096
```

### llm_config.yml (API 密钥)
```yaml
openai:
  api_key: "sk-your-key-here"
```

详见: [配置文档](docs/CONFIG.md)

## 🔌 支持的 LLM 提供商

使用 LiteLLM 统一接入层，支持:

- ✅ OpenAI (GPT-4, GPT-3.5)
- ✅ Anthropic (Claude-3)
- ✅ PerfXCloud (Qwen)
- 🔄 Azure OpenAI
- 🔄 Google (Gemini)
- 🔄 更多 100+ 提供商...

## 📊 技术栈

| 组件 | 技术 |
|------|------|
| 后端框架 | Flask 3.0 |
| LLM 接入 | LiteLLM |
| 数据验证 | Pydantic |
| 前端 | Vanilla JavaScript |
| 动画库 | GSAP 3.12 |
| 图形 | SVG |

## 📖 文档

- [快速开始](docs/GETTING_STARTED.md) - 5 分钟上手
- [配置指南](docs/CONFIG.md) - 详细配置说明
- [API 文档](docs/API.md) - 接口文档
- [开发文档](docs/DEVELOPMENT.md) - 二次开发
- [架构说明](docs/ARCHITECTURE.md) - 系统设计

## 🎯 性能指标

- **生成速度**: 3-15 秒 (取决于复杂度)
- **动画帧率**: 60 FPS
- **支持角色**: 1-5 个
- **场景数量**: 1-10 个

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

[MIT License](LICENSE)

## 🙏 致谢

- [LiteLLM](https://github.com/BerriAI/litellm) - 统一 LLM 接入
- [GSAP](https://greensock.com/gsap/) - 动画引擎
- [Flask](https://flask.palletsprojects.com/) - Web 框架

---

<div align="center">

**Made with ❤️ and AI**

[开始使用](docs/GETTING_STARTED.md) · [查看演示](#) · [报告问题](https://github.com/your-repo/issues)

</div>

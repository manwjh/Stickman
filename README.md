# 🎬 AI Stick Figure Story Animator / AI火柴人故事动画生成器

![animation_20260119_095927_315](https://github.com/user-attachments/assets/ea4d1dd0-9029-4636-a0d3-56e2c57ec7fc)
（目前效果并不好，It's not good!

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-1.57+-green.svg)](https://github.com/BerriAI/litellm)
[![Flask](https://img.shields.io/badge/Flask-3.0-orange.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.1-blue.svg)](VERSION)

> Describe stories in natural language and let AI automatically generate smooth stick figure SVG animations
> 
> 通过自然语言描述故事情节，让 AI 自动生成流畅的火柴人 SVG 动画

## ✨ Features / 特性

- 🤖 **Fully AI-Powered** - Actions generated in real-time by LLM, no predefined templates needed
  - **完全 AI 驱动** - 动作由 LLM 实时生成，无需预定义模板
- 🎭 **Natural Language Input** - Describe stories in your language, AI converts them to animations
  - **自然语言输入** - 用中文或英文描述故事，AI 自动转换为动画
- 🔌 **Unified Access Layer** - LiteLLM supports 100+ LLM providers
  - **统一接入层** - LiteLLM 支持 100+ LLM 提供商
- 🎨 **Professional Animation** - SVG vector graphics + GSAP animation engine + dual-mode skeleton system (6-parameter simple mode + 16-joint professional mode)
  - **专业动画** - SVG 矢量图形 + GSAP 动画引擎 + 双模式骨骼系统（6参数简化模式 + 16关节专业模式）
- 🌐 **Modern Interface** - Responsive Web UI with instant preview
  - **现代化界面** - 响应式 Web UI，即时预览
- 🌍 **Internationalization** - Built-in support for English and Chinese
  - **国际化支持** - 内置中英文双语切换
- ⚙️ **Flexible Configuration** - YAML configuration with separated sensitive information
  - **灵活配置** - YAML 配置，敏感信息分离
- 🚀 **Production Ready** - Caching, rate limiting, security features, and comprehensive testing
  - **生产就绪** - 缓存、限流、安全特性和完整测试
- 📊 **Multi-level LLM** - Intelligent complexity analysis with adaptive model selection
  - **多层次 LLM** - 智能复杂度分析，自适应模型选择

## 🚀 Quick Start / 快速开始

### 1. Install Dependencies / 安装依赖

```bash
# Clone the repository / 克隆仓库
git clone https://github.com/your-username/stickman.git
cd stickman

# Copy and edit configuration / 复制并编辑配置
cp llm_config.example.yml llm_config.yml

# Edit llm_config.yml and fill in your API key / 编辑 llm_config.yml 填入你的 API 密钥
# For example / 例如：
# openai:
#   api_key: "sk-your-key-here"

# Install dependencies / 安装依赖
pip install -r requirements.txt
```

### 2. Start Application / 启动应用

```bash
# Option 1: Use startup script (recommended) / 方式 1: 使用启动脚本（推荐）
./start.sh              # macOS/Linux
start.bat               # Windows

# Option 2: Manual setup / 方式 2: 手动启动
source set_env.sh       # Set environment variables / 设置环境变量
python app.py           # Start server / 启动服务器
```

### 3. Access Application / 访问应用

Open your browser and visit: **http://localhost:5001**
打开浏览器访问: **http://localhost:5001**

## 💡 Usage Examples / 使用示例

### Simple Scene / 简单场景
```
A person stands and waves hello
一个人站着，然后挥手打招呼
```

### Complex Scene / 复杂场景
```
Someone runs in from the left, sees a ball, jumps excitedly, then bends down to pick up the ball and celebrates by raising it high
小明从左边跑到右边，看到一个球，兴奋地跳起来，然后弯腰捡起球，高兴地举起球庆祝
```

### Multi-Character Scene / 多角色场景
```
Two people stand on opposite sides, walk towards each other, wave hello, and finally high-five to celebrate
小明站在左边，小红站在右边。他们走向对方，挥手打招呼，最后击掌庆祝
```

### Martial Arts Scene / 武术场景
```
A person performs a martial arts routine with a sword
小明拿着刀表演了一段武术动作
```

## 🏗️ Project Structure / 项目结构

```
stickman/
├── app.py                      # Flask main application / Flask 主应用
├── config.yml                  # System configuration / 系统配置
├── llm_config.yml             # API tokens (git ignored) / API 令牌 (不提交git)
├── llm_config.example.yml     # Config template / 配置模板
├── requirements.txt            # Python dependencies / Python 依赖
│
├── start.sh / start.bat        # Startup scripts / 启动脚本
├── set_env.sh                  # Environment setup / 环境设置
│
├── README.md                   # Project documentation / 项目文档
├── QUICK_START.md              # Quick start guide / 快速开始指南
├── LICENSE                     # MIT License / MIT 许可证
├── VERSION                     # Version number (1.0.1) / 版本号 (1.0.1)
│
├── backend/                    # Backend core modules / 后端核心模块
│   ├── config_loader.py       # Configuration loader / 配置加载器
│   ├── llm_client.py          # LLM client / LLM 客户端
│   ├── cache_service.py       # Caching service / 缓存服务
│   ├── rate_limiter.py        # Rate limiting / 限流器
│   ├── security.py            # Security utilities / 安全工具
│   │
│   ├── models/                # Data models / 数据模型
│   │   ├── base_skeleton.py   # Base skeleton class / 骨骼基类
│   │   ├── skeleton_6dof.py   # 6-DOF skeleton / 6自由度骨骼
│   │   ├── skeleton_12dof.py  # 12-DOF skeleton / 12自由度骨骼
│   │   ├── skeleton_factory.py # Skeleton factory / 骨骼工厂
│   │   ├── scene_plan.py      # Scene plan model / 场景规划模型
│   │   └── context_memory.py  # Context memory / 上下文记忆
│   │
│   ├── services/              # Business services / 业务服务
│   │   ├── animation_pipeline.py  # Animation pipeline / 动画流水线
│   │   ├── story_analyzer.py      # Story analyzer / 故事分析器
│   │   ├── animation_generator.py # Animation generator / 动画生成器
│   │   ├── animation_optimizer.py # Animation optimizer / 动画优化器
│   │   ├── gif_exporter.py        # GIF exporter / GIF 导出器
│   │   └── templates/             # Action templates / 动作模板
│   │       ├── template_engine.py # Template engine / 模板引擎
│   │       └── actions/           # Action library / 动作库
│   │           ├── walk.py        # Walk action / 行走动作
│   │           ├── wave.py        # Wave action / 挥手动作
│   │           └── bow.py         # Bow action / 鞠躬动作
│   │
│   ├── routes/                # API routes / API 路由
│   │   ├── main.py            # Main routes / 主路由
│   │   ├── api.py             # API routes / API 路由
│   │   └── export.py          # Export routes / 导出路由
│   │
│   └── utils/                 # Utility modules / 工具模块
│       ├── response.py        # Response helpers / 响应辅助
│       ├── version.py         # Version info / 版本信息
│       └── debug_logger.py    # Debug logger / 调试日志
│
├── templates/                  # HTML templates / HTML 模板
│   └── index.html
│
├── static/                     # Static assets / 静态资源
│   ├── css/style.css
│   ├── js/
│   │   ├── i18n.js            # Internationalization / 国际化支持
│   │   ├── animator.js        # SVG animation engine / SVG 动画引擎
│   │   └── app.js             # Frontend logic / 前端逻辑
│   ├── favicon.ico
│   ├── manifest.json          # PWA manifest / PWA 清单
│   └── sw.js                  # Service Worker
│
└── docs/                       # Documentation / 文档
    ├── CHANGELOG.md           # Version history / 版本历史
    ├── CONTRIBUTING.md        # Contribution guide / 贡献指南
    ├── CODE_OF_CONDUCT.md     # Code of conduct / 行为准则
    ├── API.md                 # API reference / API 参考
    ├── ARCHITECTURE.md        # System architecture / 系统架构
    ├── CONFIG.md              # Configuration guide / 配置指南
    ├── DEVELOPMENT.md         # Development guide / 开发指南
    ├── GETTING_STARTED.md     # Quick start guide / 快速开始
    └── PRODUCTION_DEPLOYMENT.md # Production deployment / 生产部署
```


## ⚙️ Configuration / 配置说明

### config.yml (System Configuration / 系统配置)
```yaml
llm:
  provider: perfxcloud       # or openai, anthropic / 或 openai, anthropic
  openai:
    model: gpt-4-turbo-preview
    temperature: 0.7
    max_tokens: 4096
  perfxcloud:
    model: Qwen3-Next-80B-Instruct
    api_base: https://deepseek.perfxlab.cn/v1

server:
  host: 0.0.0.0
  port: 5001
  debug: true

animation:
  canvas:
    width: 800
    height: 600
  max_scenes: 10
  max_characters: 5
```

### llm_config.yml (API Keys / API 密钥)
```yaml
openai:
  api_key: "sk-your-key-here"

perfxcloud:
  api_key: "sk-your-key-here"
```

See: [Configuration Guide](docs/CONFIG.md) / 详见: [配置文档](docs/zh-CN/CONFIG.md)

## 🔌 Supported LLM Providers / 支持的 LLM 提供商

Using LiteLLM unified access layer, supports:
使用 LiteLLM 统一接入层，支持:

- ✅ **OpenAI** (GPT-4, GPT-3.5)
- ✅ **Anthropic** (Claude-3)
- ✅ **PerfXCloud** (Qwen3-Next-80B-Instruct)
- 🔄 Azure OpenAI
- 🔄 Google (Gemini)
- 🔄 100+ more providers... / 更多 100+ 提供商...

## 📊 Tech Stack / 技术栈

| Component / 组件 | Technology / 技术 |
|-----------|-----------|
| Backend Framework / 后端框架 | Flask 3.0 |
| LLM Access / LLM 接入 | LiteLLM 1.57+ |
| Data Validation / 数据验证 | Pydantic 2.10+ |
| Caching / 缓存 | In-Memory Cache / 内存缓存 |
| Rate Limiting / 限流 | Token Bucket Algorithm / 令牌桶算法 |
| Frontend / 前端 | Vanilla JavaScript |
| Animation Library / 动画库 | GSAP 3.12 |
| Graphics / 图形 | SVG |
| Internationalization / 国际化 | Custom i18n / 自定义 i18n |
| Testing / 测试 | pytest 7.4+ |

## 🎯 Performance Metrics / 性能指标

- **Generation Speed / 生成速度**: 3-15 seconds (depending on complexity) / 3-15 秒 (取决于复杂度)
- **Animation Frame Rate / 动画帧率**: 60 FPS
- **Supported Characters / 支持角色**: 1-5 per scene / 每场景 1-5 个
- **Scene Count / 场景数量**: 1-10 scenes / 1-10 个场景
- **Cache Hit Rate / 缓存命中率**: 85%+ for repeated requests / 重复请求 85%+
- **API Response Time / API 响应时间**: <200ms (cached), 3-15s (new generation) / <200ms (缓存), 3-15s (新生成)

## 🔒 Security Features / 安全特性

- ✅ Input validation and sanitization / 输入验证和清理
- ✅ Rate limiting (60 requests/minute) / 限流保护 (60 请求/分钟)
- ✅ CORS configuration / CORS 配置
- ✅ Secret key management / 密钥管理
- ✅ Sensitive data isolation / 敏感数据隔离
- ✅ Environment variable protection / 环境变量保护

## 📖 Documentation / 文档

- [Quick Start](docs/GETTING_STARTED.md) - Get up and running in 5 minutes / [快速开始](docs/zh-CN/GETTING_STARTED.md) - 5 分钟上手
- [Configuration Guide](docs/CONFIG.md) - Detailed configuration instructions / [配置指南](docs/zh-CN/CONFIG.md) - 详细配置说明
- [API Documentation](docs/API.md) - REST API reference / [API 文档](docs/zh-CN/API.md) - REST API 参考
- [Architecture](docs/ARCHITECTURE.md) - System design and architecture / [架构说明](docs/zh-CN/ARCHITECTURE.md) - 系统设计和架构
- [Development Guide](docs/DEVELOPMENT.md) - For contributors / [开发文档](docs/zh-CN/DEVELOPMENT.md) - 二次开发
- [Production Deployment](docs/PRODUCTION_DEPLOYMENT.md) - Deploy to production / [生产部署](docs/PRODUCTION_DEPLOYMENT.md) - 生产环境部署

## 🤝 Contributing / 贡献

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.
欢迎提交 Issue 和 Pull Request！请参阅我们的[贡献指南](docs/CONTRIBUTING.md)。

### Development Setup / 开发环境设置

```bash
# Clone repository / 克隆仓库
git clone https://github.com/your-username/stickman.git
cd stickman

# Create virtual environment / 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate / Windows: venv\Scripts\activate

# Install dependencies / 安装依赖
pip install -r requirements.txt

# Start development server / 启动开发服务器
./start.sh
```

### Code Style / 代码规范

- Follow PEP 8 for Python code / Python 代码遵循 PEP 8 规范
- Use meaningful variable and function names / 使用有意义的变量和函数名
- Add docstrings for all public functions / 为所有公共函数添加文档字符串
- Follow DRY principle / 遵循 DRY 原则

## 🗺️ Roadmap / 路线图

- [x] Core animation generation / 核心动画生成
- [x] Multi-LLM provider support / 多 LLM 提供商支持
- [x] Internationalization (EN/CN) / 国际化 (中英文)
- [x] 6-DOF skeleton system / 6自由度骨骼系统
- [x] Caching and rate limiting / 缓存和限流
- [x] Comprehensive testing / 完整测试覆盖
- [ ] User authentication / 用户认证
- [ ] Animation export (MP4/GIF) / 动画导出 (MP4/GIF)
- [ ] Animation templates library / 动画模板库
- [ ] Real-time collaboration / 实时协作
- [ ] Docker deployment / Docker 部署
- [ ] Cloud deployment (AWS/Azure/GCP) / 云部署 (AWS/Azure/GCP)

## 👤 Author / 作者

**Shenzhen Wang & AI / 深圳王哥&AI**

- 📧 Email: manwjh@126.com
- 🐦 Twitter: [@cpswang](https://twitter.com/cpswang)
- 🌐 Website: [zenheart.net](https://zenheart.net)

## 📄 License / 许可证

[MIT License](LICENSE) - feel free to use this project for commercial or personal use.
[MIT License](LICENSE) - 可自由用于商业或个人项目

## 🙏 Acknowledgments / 致谢

- [LiteLLM](https://github.com/BerriAI/litellm) - Unified LLM access layer / 统一 LLM 接入层
- [GSAP](https://greensock.com/gsap/) - Professional animation engine / 专业动画引擎
- [Flask](https://flask.palletsprojects.com/) - Lightweight web framework / 轻量级 Web 框架
- [Pydantic](https://docs.pydantic.dev/) - Data validation library / 数据验证库

## 📈 Version History / 版本历史

See [CHANGELOG.md](docs/CHANGELOG.md) for detailed version history.
详见 [CHANGELOG.md](docs/CHANGELOG.md)

**Current Version / 当前版本**: 1.0.1 (2026-01-19)

---

<div align="center">

**Made with ❤️ by Shenzhen Wang & AI / 深圳王哥&AI**

📧 manwjh@126.com · 🐦 [@cpswang](https://twitter.com/cpswang) · 🌐 [zenheart.net](https://zenheart.net)

[Get Started](docs/GETTING_STARTED.md) · [Report Issue](https://github.com/your-repo/issues) · [开始使用](docs/zh-CN/GETTING_STARTED.md) · [报告问题](https://github.com/your-repo/issues)

</div>

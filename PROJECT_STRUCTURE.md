# 🎬 AI Stick Figure Story Animator / AI火柴人故事动画生成器

简洁、优雅的AI火柴人故事动画生成器 / Simple and elegant AI stick figure story animator

## 📁 Project Structure / 项目结构

```
stickman/
├── 📄 app.py                    # Main application entry / 主应用入口
├── 🔧 config.yml                # System configuration file / 系统配置文件
├── 🔑 llm_config.yml            # LLM API key configuration (not committed to git) / LLM API密钥配置（不提交到git）
├── 🔑 llm_config.example.yml    # API configuration example file / API配置示例文件
├── 📦 requirements.txt          # Python dependencies / Python依赖包
│
├── 🚀 start.sh                  # Linux/Mac startup script / Linux/Mac启动脚本
├── 🚀 start.bat                 # Windows startup script / Windows启动脚本  
├── ⚙️  set_env.sh               # Environment variable setup script / 环境变量设置脚本
│
├── 📖 README.md                 # Project documentation (English/Chinese) / 项目说明（英中双语）
├── 📄 LICENSE                   # Open source license / 开源许可证
├── 📌 VERSION                   # Version number / 版本号
│
├── 🔙 backend/                  # Backend core modules / 后端核心模块
│   ├── animation_validator.py  # Animation data validation / 动画数据验证
│   ├── cache_service.py         # Caching service / 缓存服务
│   ├── config_loader.py         # Configuration loader / 配置加载器
│   ├── multilevel_llm.py        # Multi-level LLM service / 多层次LLM服务
│   ├── prompt_template.py       # Prompt templates / 提示词模板
│   ├── rate_limiter.py          # Rate limiter / 速率限制器
│   ├── security.py              # Security module / 安全模块
│   └── simple_6dof.py           # 6-DOF skeleton system / 6自由度骨骼系统
│
├── 🎨 static/                   # Frontend static resources / 前端静态资源
│   ├── css/style.css            # Stylesheet / 样式表
│   ├── js/
│   │   ├── animator.js          # Animation engine / 动画引擎
│   │   ├── app.js               # Main application logic / 主应用逻辑
│   │   └── i18n.js              # Internationalization support / 国际化支持
│   ├── favicon.ico              # Website icon / 网站图标
│   ├── manifest.json            # PWA configuration / PWA配置
│   └── sw.js                    # Service Worker
│
├── 📄 templates/                # HTML templates / HTML模板
│   └── index.html               # Main page / 主页面
│
├── 🧪 tests/                    # Test suite / 测试套件
│   ├── test_cache_ratelimit.py  # Cache and rate limit tests / 缓存和限流测试
│   ├── test_integration.py      # Integration tests / 集成测试
│   ├── test_llm_service.py      # LLM service tests / LLM服务测试
│   ├── test_security.py         # Security tests / 安全测试
│   ├── test_skeleton.py         # Skeleton system tests / 骨骼系统测试
│   └── test_validator.py        # Validator tests / 验证器测试
│
├── 📚 docs/                     # Project documentation / 项目文档
│   ├── CHANGELOG.md             # Changelog (English) / 更新日志（英文）
│   ├── CHANGELOG.zh-CN.md       # Changelog (Chinese) / 更新日志（中文）
│   ├── CODE_OF_CONDUCT.md       # Code of conduct / 行为准则
│   ├── CONTRIBUTING.md          # Contributing guide (English) / 贡献指南（英文）
│   ├── CONTRIBUTING.zh-CN.md    # Contributing guide (Chinese) / 贡献指南（中文）
│   ├── API.md                   # API documentation / API文档
│   ├── ARCHITECTURE.md          # Architecture design / 架构设计
│   ├── CONFIG.md                # Configuration guide / 配置说明
│   ├── DEVELOPMENT.md           # Development guide / 开发指南
│   ├── GETTING_STARTED.md       # Quick start / 快速开始
│   └── PRODUCTION_DEPLOYMENT.md # Production deployment / 生产部署
│
└── 🐍 venv/                     # Python virtual environment (not committed to git) / Python虚拟环境（不提交到git）
```

## 🚀 Quick Start / 快速开始

### 1️⃣ Environment Setup / 环境设置
```bash
# Copy configuration file template / 复制配置文件模板
cp llm_config.example.yml llm_config.yml

# Edit configuration file and fill in your API key / 编辑配置文件，填入你的API密钥
vim llm_config.yml
```

### 2️⃣ Install Dependencies / 安装依赖
```bash
# Create virtual environment / 创建虚拟环境
python -m venv venv

# Activate virtual environment / 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# or / 或
venv\Scripts\activate     # Windows

# Install dependencies / 安装依赖
pip install -r requirements.txt
```

### 3️⃣ Start Application / 启动应用
```bash
# Linux/Mac
./start.sh

# Windows
start.bat
```

### 4️⃣ Access Application / 访问应用
Open your browser and visit: http://localhost:5001
打开浏览器访问: http://localhost:5001

## 📝 Core Files Description / 核心文件说明

### 🎯 Application Entry / 应用入口
- **app.py**: Flask application main program, handles HTTP requests and routing / Flask应用主程序，处理HTTP请求和路由

### ⚙️ Configuration Files / 配置文件
- **config.yml**: System configuration (server, animation, logging, etc.) / 系统配置（服务器、动画、日志等）
- **llm_config.yml**: LLM service configuration (API keys, do not commit to git) / LLM服务配置（API密钥，不要提交到git）
- **llm_config.example.yml**: Configuration file template / 配置文件模板

### 📦 Dependency Management / 依赖管理
- **requirements.txt**: Contains all runtime and optional test dependencies / 包含所有运行时和可选的测试依赖

### 🚀 Startup Scripts / 启动脚本
- **start.sh**: Linux/Mac startup script, automatically checks environment and dependencies / Linux/Mac启动脚本，自动检查环境和依赖
- **start.bat**: Windows startup script / Windows启动脚本
- **set_env.sh**: Environment variable setup helper script / 环境变量设置辅助脚本

## 🔧 Configuration Guide / 配置指南

See detailed configuration documentation: `docs/CONFIG.md`
查看详细配置文档：`docs/CONFIG.md`

## 🧪 Running Tests / 运行测试

```bash
# Activate virtual environment / 激活虚拟环境
source venv/bin/activate

# Install test dependencies (if not already installed) / 安装测试依赖（如果还没安装）
pip install pytest pytest-cov

# Run all tests / 运行所有测试
pytest

# Run specific test / 运行特定测试
pytest tests/test_llm_service.py

# Generate coverage report / 生成覆盖率报告
pytest --cov=backend --cov-report=html
```

## 📚 More Documentation / 更多文档

- [API Documentation](docs/API.md) / [API文档](docs/API.md)
- [Architecture Design](docs/ARCHITECTURE.md) / [架构设计](docs/ARCHITECTURE.md)
- [Development Guide](docs/DEVELOPMENT.md) / [开发指南](docs/DEVELOPMENT.md)
- [Production Deployment](docs/PRODUCTION_DEPLOYMENT.md) / [生产部署](docs/PRODUCTION_DEPLOYMENT.md)

## 📄 License / 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🤝 Contributing / 贡献

Contributions are welcome! Please read the [Contributing Guide](docs/CONTRIBUTING.md)
欢迎贡献！请阅读 [贡献指南](docs/CONTRIBUTING.md)

---

**Current Version / 当前版本**: 0.4.0  
**Last Updated / 最后更新**: 2026-01-17

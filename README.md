# 🎬 AI Stick Figure Story Animator

[中文文档](README.zh-CN.md) | English

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-1.57+-green.svg)](https://github.com/BerriAI/litellm)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Describe stories in natural language and let AI automatically generate smooth stick figure SVG animations

## ✨ Features

- 🤖 **Fully AI-Powered** - Actions generated in real-time by LLM, no predefined templates needed
- 🎭 **Natural Language Input** - Describe stories in your language, AI converts them to animations
- 🔌 **Unified Access Layer** - LiteLLM supports 100+ LLM providers
- 🎨 **Professional Animation** - SVG vector graphics + GSAP animation engine
- 🌐 **Modern Interface** - Responsive Web UI with instant preview
- 🌍 **Internationalization** - Built-in support for English and Chinese
- ⚙️ **Flexible Configuration** - YAML configuration with separated sensitive information

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Clone the repository
git clone https://github.com/your-username/stickman.git
cd stickman

# Copy and edit configuration
cp llm_config.example.yml llm_config.yml

# Edit llm_config.yml and fill in your API key
# openai.api_key: "sk-your-key-here"

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Application

```bash
# Option 1: Use startup script
./start.sh              # macOS/Linux
start.bat               # Windows

# Option 2: Direct start
python3 app.py
```

### 3. Access Application

Open your browser and visit: **http://localhost:5001**

## 💡 Usage Examples

### Simple Scene
```
A person stands and waves hello
```

### Complex Scene
```
Someone runs in from the left, sees a ball, jumps excitedly, then bends down to pick up the ball and celebrates by raising it high
```

### Multi-Character Scene
```
Two people stand on opposite sides, walk towards each other, wave hello, and finally high-five to celebrate
```

### Martial Arts Scene
```
A person performs a martial arts routine with a sword
```

## 🏗️ Project Structure

```
stickman/
├── app.py                      # Flask main application
├── requirements.txt            # Python dependencies
├── config.yml                  # System configuration (can commit)
├── llm_config.yml             # API tokens (do not commit)
│
├── backend/                    # Backend services
│   ├── config_loader.py       # Configuration loader
│   ├── llm_service.py         # LLM service (LiteLLM)
│   ├── prompt_template.py     # Prompt templates
│   └── animation_validator.py # Data validation
│
├── templates/                  # HTML templates
│   └── index.html
│
├── static/                     # Static assets
│   ├── css/style.css
│   └── js/
│       ├── i18n.js            # Internationalization
│       ├── animator.js        # SVG animation engine
│       └── app.js             # Frontend logic
│
└── docs/                       # Documentation
    ├── en/                    # English docs
    └── zh-CN/                 # Chinese docs
```

## ⚙️ Configuration

### config.yml (System Configuration)
```yaml
llm:
  provider: openai              # or anthropic, perfxcloud
  openai:
    model: gpt-4-turbo-preview
    temperature: 0.7
    max_tokens: 4096
```

### llm_config.yml (API Keys)
```yaml
openai:
  api_key: "sk-your-key-here"
```

See: [Configuration Guide](docs/en/CONFIG.md)

## 🔌 Supported LLM Providers

Using LiteLLM unified access layer, supports:

- ✅ OpenAI (GPT-4, GPT-3.5)
- ✅ Anthropic (Claude-3)
- ✅ PerfXCloud (Qwen)
- 🔄 Azure OpenAI
- 🔄 Google (Gemini)
- 🔄 100+ more providers...

## 📊 Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend Framework | Flask 3.0 |
| LLM Access | LiteLLM |
| Data Validation | Pydantic |
| Frontend | Vanilla JavaScript |
| Animation Library | GSAP 3.12 |
| Graphics | SVG |
| Internationalization | Custom i18n |

## 📖 Documentation

- [Quick Start](docs/en/GETTING_STARTED.md) - Get up and running in 5 minutes
- [Configuration Guide](docs/en/CONFIG.md) - Detailed configuration instructions
- [API Documentation](docs/en/API.md) - API reference
- [Development Guide](docs/en/DEVELOPMENT.md) - For contributors
- [Architecture](docs/en/ARCHITECTURE.md) - System design

## 🎯 Performance Metrics

- **Generation Speed**: 3-15 seconds (depending on complexity)
- **Animation Frame Rate**: 60 FPS
- **Supported Characters**: 1-5
- **Scene Count**: 1-10

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-username/stickman.git
cd stickman

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

## 👤 Author

**Shenzhen Wang & AI**

- 📧 Email: manwjh@126.com
- 🐦 Twitter: [@cpswang](https://twitter.com/cpswang)
- 🌐 Website: [zenheart.net](https://zenheart.net)

## 📄 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- [LiteLLM](https://github.com/BerriAI/litellm) - Unified LLM access
- [GSAP](https://greensock.com/gsap/) - Animation engine
- [Flask](https://flask.palletsprojects.com/) - Web framework

---

<div align="center">

**Made with ❤️ by Shenzhen Wang & AI**

📧 manwjh@126.com · 🐦 [@cpswang](https://twitter.com/cpswang) · 🌐 [zenheart.net](https://zenheart.net)

[Get Started](docs/en/GETTING_STARTED.md) · [Report Issue](https://github.com/your-repo/issues) · [中文文档](README.zh-CN.md)

</div>

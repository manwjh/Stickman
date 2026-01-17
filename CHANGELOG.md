# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[中文版](CHANGELOG.zh-CN.md)

---

## [0.1.0] - 2026-01-17

### 🎉 Initial Release

First public release of AI Stick Figure Story Animator!

### ✨ Added

#### Core Features
- **AI-Powered Animation Generation** - Convert natural language stories to stick figure animations using LLM
- **Multiple LLM Provider Support** - Integrated with OpenAI, Anthropic, and PerfXCloud via LiteLLM
- **Interactive Web Interface** - Modern, responsive UI with real-time animation preview
- **SVG Animation Engine** - Smooth 60 FPS animations using GSAP
- **Multi-Character Support** - Generate animations with up to 5 characters
- **Scene Management** - Support for multi-scene animations with smooth transitions

#### Internationalization (i18n)
- **Bilingual UI** - Built-in support for English and Chinese with live language switching
- **Localized Documentation** - Complete documentation in both English and Chinese
- **i18n Framework** - Custom lightweight internationalization system

#### Configuration
- **Dual Configuration System** - Separate system config and API keys for security
- **YAML-based Configuration** - Easy-to-edit configuration files
- **Environment Variable Support** - Override settings via environment variables
- **Multiple Provider Configs** - Pre-configured templates for OpenAI, Anthropic, PerfXCloud

#### Developer Experience
- **Clean Architecture** - Well-organized codebase with clear separation of concerns
- **Type Validation** - Pydantic-based data validation for animation data
- **Comprehensive Documentation** - Getting started, API docs, configuration guide, and more
- **Startup Scripts** - Convenient scripts for macOS/Linux and Windows
- **Error Handling** - Graceful error handling with user-friendly messages

#### Documentation
- **README** - Bilingual README with badges and quick start guide
- **Contributing Guide** - Detailed contribution guidelines in English and Chinese
- **Code of Conduct** - Contributor Covenant code of conduct
- **API Documentation** - Complete REST API reference with examples
- **Configuration Guide** - Comprehensive configuration documentation
- **Getting Started Guide** - Step-by-step setup instructions
- **GitHub Templates** - Issue and PR templates for better collaboration

### 🔧 Technical Stack

- **Backend**: Flask 3.0, LiteLLM, Pydantic
- **Frontend**: Vanilla JavaScript, GSAP 3.12, SVG
- **Configuration**: PyYAML
- **Validation**: Pydantic models
- **Animation**: GSAP timeline-based animation system

### 📦 Supported LLM Providers

- OpenAI (GPT-4, GPT-3.5-turbo)
- Anthropic (Claude-3)
- PerfXCloud (Qwen)
- Compatible with 100+ providers through LiteLLM

### 🌍 Languages

- English (en)
- Chinese Simplified (zh-CN)

### 📝 Known Limitations

- Maximum 5 characters per animation
- Maximum 10 scenes per animation
- Generation time: 3-15 seconds depending on complexity
- No animation persistence (no database)
- No user authentication system

### 🎯 Future Plans

See [ROADMAP.md](docs/ROADMAP.md) for planned features and improvements.

---

## Version History

- [0.1.0] - 2026-01-17 - Initial release

---

**Legend**:
- ✨ Added - New features
- 🔧 Changed - Changes in existing functionality
- 🐛 Fixed - Bug fixes
- 🗑️ Deprecated - Soon-to-be removed features
- ❌ Removed - Removed features
- 🔒 Security - Security improvements
- 📝 Documentation - Documentation changes

[0.1.0]: https://github.com/your-username/stickman/releases/tag/v0.1.0

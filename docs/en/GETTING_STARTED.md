# Getting Started with AI Stick Figure Story Animator

[中文](../zh-CN/GETTING_STARTED.md) | English

This guide will help you get up and running with the AI Stick Figure Story Animator in less than 5 minutes.

## Prerequisites

- **Python 3.9+** installed on your system
- **pip** package manager
- **API Key** from one of the supported LLM providers:
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude-3)
  - PerfXCloud (Qwen)

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/stickman.git
cd stickman
```

### Step 2: Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys

```bash
# Copy example configuration
cp llm_config.example.yml llm_config.yml

# Edit the configuration file
nano llm_config.yml  # or use your preferred editor
```

Add your API key to `llm_config.yml`:

```yaml
openai:
  api_key: "sk-your-actual-api-key-here"
```

### Step 5: Start the Application

```bash
# Option 1: Use the startup script
./start.sh              # macOS/Linux
start.bat               # Windows

# Option 2: Run directly
python app.py
```

### Step 6: Open in Browser

Visit **http://localhost:5001** in your web browser.

## Your First Animation

1. **Switch Language** (optional): Click the language toggle button in the top-right corner
2. **Enter a Story**: Type a story description in the text area, for example:
   ```
   A person walks in from the left, waves hello, then jumps and celebrates
   ```
3. **Generate**: Click the "Generate Animation" button
4. **Watch**: The animation will auto-play once generated
5. **Control**: Use the playback controls to pause, restart, or download

## Example Stories

Try these examples to get started:

### Simple Wave
```
A person stands and waves hello
```

### Running and Jumping
```
Someone runs from left to right, then jumps excitedly to celebrate
```

### Picking Up Object
```
A person walks in, bends down to pick something up, then raises it happily
```

### Two Characters
```
Two people stand on opposite sides, walk towards each other, wave hello, and finally high-five
```

## Configuration

### Changing LLM Provider

Edit `config.yml` to change the LLM provider:

```yaml
llm:
  provider: openai  # or anthropic, perfxcloud
```

### Adjusting Server Settings

Edit `config.yml` to customize server settings:

```yaml
server:
  host: 0.0.0.0
  port: 5001
  debug: true
```

For more configuration options, see the [Configuration Guide](CONFIG.md).

## Troubleshooting

### Issue: "Configuration file not found"

**Solution**: Make sure you've copied `llm_config.example.yml` to `llm_config.yml`:
```bash
cp llm_config.example.yml llm_config.yml
```

### Issue: "API key not configured"

**Solution**: Edit `llm_config.yml` and replace `your_api_key_here` with your actual API key.

### Issue: "Port already in use"

**Solution**: Change the port in `config.yml`:
```yaml
server:
  port: 5002  # Use a different port
```

### Issue: Animation generation is slow

**Causes**:
- Complex stories require more processing time
- Network latency to LLM API
- Model selection (GPT-4 is more powerful but slower)

**Solutions**:
- Try a simpler story first
- Use GPT-3.5-turbo for faster generation
- Check your internet connection

## Next Steps

- Read the [API Documentation](API.md) to integrate with your own applications
- Check out the [Development Guide](DEVELOPMENT.md) to contribute
- Learn about the [Architecture](ARCHITECTURE.md) to understand how it works

## Getting Help

If you encounter any issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Search [existing issues](https://github.com/your-repo/issues)
3. Create a [new issue](https://github.com/your-repo/issues/new) with:
   - Error messages
   - Steps to reproduce
   - Your environment (OS, Python version)

## Related Resources

- [Configuration Guide](CONFIG.md)
- [API Documentation](API.md)
- [Contributing Guide](../../CONTRIBUTING.md)

---

Happy animating! 🎬✨

# 🚀 快速使用指南

## 三步开始使用

### 第一步：安装

```bash
# 运行一键安装脚本
python3 install.py
```

### 第二步：配置API密钥

复制并编辑 `llm_config.yml` 文件：

```bash
cp llm_config.example.yml llm_config.yml
```

填入你的API密钥：

```yaml
openai:
  api_key: "sk-your-actual-key-here"
```

**获取API密钥：**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/

**配置LLM提供商：**

编辑 `config.yml` 文件选择使用的LLM：

```yaml
llm:
  provider: openai  # 或 anthropic
```

### 第三步：启动

```bash
# macOS/Linux
./start.sh

# Windows
start.bat
```

打开浏览器访问：http://localhost:5000

---

## 📝 示例使用

### 1️⃣ 输入故事
在文本框中输入：
```
小明从左边走到右边，然后跳起来庆祝
```

### 2️⃣ 生成动画
点击"✨ 生成动画"按钮，等待3-8秒

### 3️⃣ 观看动画
动画会自动播放，你可以：
- ▶️ 播放/继续
- ⏸️ 暂停
- 🔄 重新开始
- 💾 下载SVG文件

---

## 💡 更多示例

### 简单动作
```
一个人站着，然后挥手打招呼
```

### 复杂动作
```
小明看到一个球，兴奋地跑过去，弯腰捡起球，然后高兴地举起球庆祝
```

### 多角色互动
```
小明站在左边，小红站在右边。小明走向小红并挥手，小红也挥手回应，最后他们击掌庆祝
```

### 连续动作
```
一个人慢慢走进来，停下来环顾四周，然后快速跑向右边，最后跳起来做胜利手势
```

---

## ⚡ 快捷键

- `Ctrl/Cmd + Enter`: 生成动画
- `空格`: 播放/暂停（焦点在动画区域时）

---

## 🔧 常见问题

### Q: 提示"API密钥错误"
**A:** 检查 `llm_config.yml` 文件中的API密钥是否正确填写

### Q: 生成失败
**A:** 可能原因：
1. 网络问题 - 检查网络连接
2. API配额用完 - 检查账户余额
3. 故事描述不清楚 - 尝试更详细的描述

### Q: 动画不流畅
**A:** 尝试：
1. 使用更强大的模型（GPT-4）
2. 添加更多动作细节
3. 减少复杂度

### Q: 如何更改端口
**A:** 编辑 `config.yml` 文件：
```yaml
server:
  port: 8000
```

---

## 📚 更多文档

- [完整README](README.md) - 详细说明
- [API文档](API.md) - 接口说明
- [开发指南](DEVELOPMENT.md) - 二次开发

---

## 💬 获取帮助

- 查看文档：项目根目录的 `.md` 文件
- 运行检查：`python check_setup.py`
- GitHub Issues：报告问题

---

**🎉 开始创作你的火柴人动画故事吧！**

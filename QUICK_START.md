# 🚀 快速开始指南 / Quick Start Guide

让你在 5 分钟内启动 AI 火柴人动画生成器！

## 📋 前置要求 / Prerequisites

- Python 3.9+
- LLM API 密钥（OpenAI / Anthropic / PerfXCloud）

## 1️⃣ 安装和配置 / Installation

```bash
# 克隆项目
git clone <your-repo-url>
cd stickman

# 安装依赖
pip install -r requirements.txt

# 复制配置模板
cp llm_config.example.yml llm_config.yml

# 编辑 llm_config.yml，填入你的 API 密钥
# Edit llm_config.yml and add your API key
```

## 2️⃣ 启动服务 / Start Server

```bash
# macOS/Linux
./start.sh

# Windows
start.bat

# 或手动启动
source set_env.sh
python app.py
```

服务将在 `http://localhost:5001` 启动。
浏览器访问 http://localhost:5001 开始使用！

## 3️⃣ 使用示例 / Usage Examples

### Web 界面使用

1. 打开浏览器访问 http://localhost:5001
2. 在文本框中输入故事描述，例如：
   - "一个人从左边走进来，挥手打招呼"
   - "小明跑过来，跳起来庆祝"
3. 点击"生成动画"按钮
4. 等待 3-15 秒，观看生成的动画

### API 调用示例

#### 基础调用
```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "story": "一个人从左边走进来，挥手打招呼，然后鞠躬"
  }'
```

#### 指定 DOF 级别
```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "story": "小明表演了一套武术动作",
    "dof_level": "12dof",
    "use_cache": true
  }'
```

#### 导出 GIF
```bash
# 先生成动画获取 animation_id
# 然后导出 GIF
curl -X POST http://localhost:5001/api/export/gif \
  -H "Content-Type: application/json" \
  -d '{
    "animation_id": "your-animation-id",
    "fps": 30,
    "duration_scale": 1.0
  }'
```

## 4️⃣ Python SDK 示例 / Python SDK

```python
from backend.services.animation_pipeline import AnimationPipelineV2

# 创建流水线实例
pipeline = AnimationPipelineV2(
    dof_level='12dof',       # 使用 12 自由度骨骼系统
    enable_optimization=True  # 启用动画优化
)

# 生成动画
result = pipeline.generate(
    story="一个人从左边走进来，挥手打招呼，然后鞠躬",
    use_cache=True
)

# 检查结果
if result['success']:
    print(f"✅ 生成成功！")
    print(f"关键帧数：{result['metadata']['keyframes_generated']}")
    print(f"生成时间：{result['metadata']['generation_time_ms']}ms")
    print(f"LLM 调用：{result['metadata']['llm_calls']}次")
    
    # 访问动画数据
    characters = result['data']['characters']
    keyframes = result['data']['keyframes']
    
else:
    print(f"❌ 生成失败：{result.get('error')}")
```

## 📊 响应格式 / Response Format

```json
{
  "success": true,
  "data": {
    "characters": [
      {
        "id": "char1",
        "name": "问候者",
        "color": "#2196F3"
      }
    ],
    "keyframes": [
      {
        "timestamp_ms": 0,
        "description": "准备行走",
        "characters": {
          "char1": {
            "joints": {
              "head": {"x": 400, "y": 240},
              "neck": {"x": 400, "y": 260},
              "waist": {"x": 400, "y": 320}
            }
          }
        }
      }
    ]
  },
  "metadata": {
    "dof_level": "12dof",
    "generation_time_ms": 2500,
    "keyframes_generated": 12,
    "llm_calls": 2,
    "generation_method": "template"
  }
}
```

## 🎯 支持的动作模板 / Action Templates

系统内置以下动作模板，**无需 LLM 调用，生成速度极快**：

- **walk** / 行走：自然的行走动作
- **wave** / 挥手：友好的挥手打招呼
- **bow** / 鞠躬：礼貌的鞠躬动作

复杂动作使用 LLM 批量生成（1-2 次调用）。

## ⚙️ API 端点 / API Endpoints

| 端点 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/api/generate` | POST | 生成动画 | `story`, `dof_level`, `use_cache` |
| `/api/export/gif` | POST | 导出 GIF | `animation_id`, `fps`, `duration_scale` |
| `/api/health` | GET | 健康检查 | - |
| `/api/metrics` | GET | 性能指标 | - |
| `/api/version` | GET | 版本信息 | - |

### 详细参数说明

#### POST /api/generate
- `story` (必需, string): 故事描述
- `dof_level` (可选, string): "6dof" 或 "12dof"，默认 "12dof"
- `use_cache` (可选, boolean): 是否使用缓存，默认 true

#### POST /api/export/gif
- `animation_id` (必需, string): 动画 ID
- `fps` (可选, number): 帧率，默认 30
- `duration_scale` (可选, number): 时长缩放，默认 1.0

## 🐛 常见问题 / FAQ

### Q1: LLM 调用失败？
**A**: 
- 检查 `llm_config.yml` 中的 API 密钥是否正确
- 确认已运行 `source ./set_env.sh`（或使用 `./start.sh`）
- 检查网络连接和 API 提供商状态

### Q2: 生成速度慢？
**A**: 
- 使用模板动作（walk, wave, bow）可实现**秒级生成**
- 启用缓存 `use_cache=True`
- 使用 6DOF 模式（更简单但质量略低）

### Q3: 动画不流畅？
**A**: 
- 确保启用了优化：`enable_optimization=True`
- 使用 12DOF 骨骼系统获得更好的动作表现
- 增加关键帧密度（在 `skeleton_config.yml` 中配置）

### Q4: 如何切换 LLM 提供商？
**A**: 
编辑 `config.yml`：
```yaml
llm:
  provider: openai  # 或 perfxcloud, anthropic
```

## 🎨 配置选项 / Configuration

### 系统配置 (config.yml)
```yaml
llm:
  provider: perfxcloud
  timeout: 30

server:
  host: 0.0.0.0
  port: 5001

animation:
  canvas:
    width: 800
    height: 600
  max_scenes: 10
  max_characters: 5
```

### LLM 配置 (llm_config.yml)
```yaml
openai:
  api_key: "sk-your-key-here"

perfxcloud:
  api_key: "sk-your-key-here"
```

## 📚 更多文档 / Documentation

- 📖 [完整文档](docs/INDEX.md) - 所有文档索引
- 🏗️ [系统架构](docs/ARCHITECTURE.md) - 架构设计说明
- ⚙️ [配置指南](docs/CONFIG.md) - 详细配置说明
- 🔌 [API 参考](docs/API.md) - API 完整文档
- 🛠️ [开发指南](docs/DEVELOPMENT.md) - 二次开发指南
- 🚀 [生产部署](docs/PRODUCTION_DEPLOYMENT.md) - 生产环境部署

---

**💡 提示**: 
- 推荐使用 **12DOF** 模式，提供最佳的性能和质量平衡！
- 首次使用建议从简单场景开始，如"一个人挥手打招呼"
- 启用缓存可大幅提升重复请求的响应速度


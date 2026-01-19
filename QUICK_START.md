# 🚀 快速开始指南

## 前置要求

- Python 3.9+
- LLM API密钥（OpenAI / Anthropic / PerfXCloud）

## 1️⃣ 安装和配置

```bash
# 安装依赖
pip install -r requirements.txt

# 配置API密钥
source ./set_env.sh
# 编辑 set_env.sh 添加你的API密钥
```

## 2️⃣ 启动服务

```bash
./start.sh
```

服务将在 `http://localhost:5001` 启动。

## 3️⃣ 测试API

### 基础测试
```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "story": "一个人从左边走进来，挥手打招呼，然后鞠躬"
  }'
```

### 指定DOF级别
```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "story": "小明表演了一套武术动作",
    "dof_level": "12dof"
  }'
```

## 4️⃣ Python代码示例

```python
from backend.services.animation_pipeline import AnimationPipelineV2

# 创建流水线
pipeline = AnimationPipelineV2(
    dof_level='12dof',
    enable_optimization=True
)

# 生成动画
result = pipeline.generate(
    story="一个人从左边走进来，挥手打招呼，然后鞠躬"
)

if result['success']:
    print(f"✅ 生成成功！")
    print(f"关键帧数：{result['metadata']['keyframes_generated']}")
    print(f"生成时间：{result['metadata']['generation_time_ms']}ms")
    print(f"LLM调用：{result['metadata']['llm_calls']}次")
else:
    print(f"❌ 生成失败：{result.get('error')}")
```

## 📊 响应格式

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

## 🎯 支持的动作模板

系统内置以下动作模板，**0次LLM调用**：

- **walk**: 行走
- **wave**: 挥手
- **bow**: 鞠躬

其他动作使用LLM批量生成（1次调用）。

## ⚙️ API端点

### 生成动画
```
POST /api/generate
```

参数：
- `story` (必需): 故事描述
- `dof_level` (可选): "6dof" 或 "12dof"，默认 "12dof"
- `use_cache` (可选): 是否使用缓存，默认 true

### 健康检查
```
GET /api/health
```

### 性能指标
```
GET /api/metrics
```

### 版本信息
```
GET /api/version
```

## 🐛 常见问题

### Q1: LLM调用失败？
**A**: 检查API密钥配置，运行 `source ./set_env.sh`

### Q2: 生成速度慢？
**A**: 使用模板动作（walk, wave, bow）可大幅提速

### Q3: 动画不流畅？
**A**: 启用优化 `enable_optimization=True`

## 📚 更多文档

- [完整架构](REFACTORING_V2_SUMMARY.md)
- [问题诊断](PROJECT_ISSUES_ANALYSIS.md)
- [API文档](docs/API.md)

---

**提示**: 推荐使用12DOF，提供最佳的性能和质量平衡！🎯


# 🏗️ 系统架构

## 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                      用户层                              │
│                   (Web Browser)                          │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP
                 ↓
┌─────────────────────────────────────────────────────────┐
│                    前端层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  index.html  │  │   app.js     │  │ animator.js  │  │
│  │   (UI界面)   │  │  (业务逻辑)  │  │  (SVG动画)   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────┬────────────────────────────────────────┘
                 │ REST API
                 ↓
┌─────────────────────────────────────────────────────────┐
│                    应用层                                │
│              Flask Web Server                            │
│  ┌──────────────────────────────────────────────────┐   │
│  │  app.py  (路由和请求处理)                        │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────┐
│                   业务逻辑层                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │config_loader │  │ llm_service  │  │  validator   │  │
│  │  (配置管理)  │  │  (LLM调用)   │  │  (数据验证)  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                    ┌──────────────┐                      │
│                    │prompt_template│                     │
│                    │ (提示词模板) │                      │
│                    └──────────────┘                      │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────┐
│                   LLM 接入层                             │
│                    LiteLLM                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐          │
│  │  OpenAI  │  │Anthropic │  │  PerfXCloud  │          │
│  └──────────┘  └──────────┘  └──────────────┘          │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP
                 ↓
┌─────────────────────────────────────────────────────────┐
│                  外部服务层                              │
│          LLM API Providers                               │
└─────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. 配置管理 (config_loader.py)

**职责**:
- 加载 YAML 配置文件
- 转换为环境变量
- 验证配置完整性

**设计模式**: 单例模式

```python
class ConfigLoader:
    def load()          # 加载配置
    def validate()      # 验证配置
    def to_env()        # 转为环境变量
```

### 2. LLM 服务 (llm_service.py)

**职责**:
- 统一 LLM 调用接口
- 支持多提供商切换
- 处理请求和响应

**设计模式**: 单例模式 + 策略模式

```python
class LLMService:
    def __init__()              # 初始化
    def _setup_provider()       # 配置提供商
    def generate_animation()    # 生成动画
```

### 3. Prompt 模板 (prompt_template.py)

**职责**:
- 构建结构化 Prompt
- 定义输出格式
- 提供示例和约束

```python
def get_animation_prompt(story: str) -> str
```

### 4. 数据验证 (animation_validator.py)

**职责**:
- 验证 LLM 输出格式
- 检查坐标范围
- 确保数据完整性

**设计模式**: Pydantic 数据模型

```python
class AnimationData(BaseModel):
    title: str
    characters: List[Character]
    scenes: List[Scene]
```

### 5. 动画引擎 (animator.js)

**职责**:
- 创建 SVG 元素
- 管理 GSAP 时间轴
- 渲染动画

```javascript
class StickFigureAnimator {
    loadAnimation()
    play()
    pause()
    restart()
}
```

## 数据流

### 请求流程

```
1. 用户输入故事
   ↓
2. JavaScript 发送 POST /api/generate
   ↓
3. Flask 路由接收请求
   ↓
4. 读取配置 (config_loader)
   ↓
5. 构建 Prompt (prompt_template)
   ↓
6. 调用 LLM (llm_service → LiteLLM)
   ↓
7. AI 处理并返回 JSON
   ↓
8. 验证数据 (animation_validator)
   ↓
9. 返回给前端
   ↓
10. 渲染动画 (animator.js)
```

### 数据格式

**请求**:
```json
{
  "story": "小明拿着刀表演了一段武术动作"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "title": "武术表演",
    "characters": [...],
    "scenes": [{
      "frames": [...]
    }]
  }
}
```

## 技术选型

### 后端

- **Flask**: 轻量级，易于扩展
- **LiteLLM**: 统一接入，支持多提供商
- **Pydantic**: 类型安全，数据验证
- **PyYAML**: 配置管理

### 前端

- **Vanilla JavaScript**: 无依赖，性能好
- **GSAP**: 专业动画库，60fps
- **SVG**: 矢量图形，清晰不失真

## 设计原则

### 1. 关注点分离

- 配置管理独立
- LLM 调用独立
- 数据验证独立
- 动画渲染独立

### 2. 单一职责

每个模块只负责一个功能

### 3. 开放封闭

对扩展开放（添加新 LLM），对修改封闭

### 4. 依赖倒置

依赖抽象（LiteLLM），不依赖具体实现

## 扩展性

### 添加新 LLM 提供商

1. 在 `config.yml` 添加配置
2. 在 `llm_config.yml` 添加密钥
3. 在 `llm_service.py` 添加 `_setup_xxx()` 方法

### 添加新功能

1. 后端：在 `app.py` 添加路由
2. 前端：在 `app.js` 添加事件处理
3. 动画：在 `animator.js` 扩展功能

## 性能优化

### 已实现

- ✅ 配置预加载
- ✅ LLM 服务单例
- ✅ SVG 元素复用
- ✅ GSAP 硬件加速

### 可优化

- 🔄 响应缓存
- 🔄 并发控制
- 🔄 流式响应
- 🔄 CDN 加速

## 安全性

### 已实现

- ✅ 敏感信息分离
- ✅ 输入验证
- ✅ 数据验证
- ✅ CORS 配置

### 建议

- 🔐 添加用户认证
- 🔐 添加请求限流
- 🔐 API 密钥轮换

## 可靠性

### 错误处理

- LLM 调用失败 → 友好提示
- 数据验证失败 → 降级处理
- 网络超时 → 自动重试

### 日志记录

```python
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT
)
```

## 监控

### 关键指标

- API 响应时间
- LLM 调用成功率
- 动画生成质量
- 用户满意度

## 部署

### 开发环境

```bash
python app.py
```

### 生产环境

```bash
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Docker (待实现)

```dockerfile
FROM python:3.9
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

## 更多文档

- [配置指南](CONFIG.md)
- [API 文档](API.md)
- [开发文档](DEVELOPMENT.md)

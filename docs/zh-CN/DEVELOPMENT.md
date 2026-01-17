# 开发指南

## 项目架构

```
stick_figure/
├── app.py                      # Flask主应用
├── backend/                    # 后端逻辑
│   ├── llm_service.py         # LLM服务层
│   ├── prompt_template.py     # Prompt模板
│   └── animation_validator.py # 数据验证
├── templates/                  # HTML模板
│   └── index.html
├── static/                     # 静态资源
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── animator.js        # SVG动画引擎
│       └── app.js            # 前端主逻辑
└── requirements.txt           # Python依赖
```

## 技术栈

### 后端
- **Flask 3.0**: Web框架
- **OpenAI API**: GPT-4集成
- **Anthropic API**: Claude集成
- **Pydantic**: 数据验证

### 前端
- **Vanilla JavaScript**: 无框架依赖
- **GSAP**: 动画库
- **SVG**: 矢量图形

## 开发环境设置

### 1. 安装开发依赖

```bash
pip install -r requirements.txt
pip install pytest black flake8  # 开发工具
```

### 2. 代码规范

使用Black格式化代码：

```bash
black backend/ app.py
```

代码检查：

```bash
flake8 backend/ app.py
```

### 3. 调试模式

编辑 `.env`:

```env
FLASK_DEBUG=True
FLASK_ENV=development
```

## 核心模块说明

### LLM服务层 (`backend/llm_service.py`)

负责与LLM API交互。

**主要功能**：
- 支持多个LLM提供商（OpenAI/Anthropic）
- 自动处理API调用和错误
- JSON响应解析

**扩展新的LLM提供商**：

```python
# 在 LLMService.__init__ 中添加
elif self.provider == 'new_provider':
    self.client = NewProviderClient(api_key=api_key)
    self.model = os.getenv('NEW_PROVIDER_MODEL')

# 添加生成方法
def _generate_with_new_provider(self, prompt: str):
    # 实现API调用
    pass
```

### Prompt模板 (`backend/prompt_template.py`)

定义发送给LLM的提示词。

**优化Prompt**：
- 修改 `get_animation_prompt()` 函数
- 调整示例和约束条件
- 添加更多动作参考

### 动画验证器 (`backend/animation_validator.py`)

使用Pydantic验证LLM输出。

**添加新的验证规则**：

```python
class StickFigure(BaseModel):
    head: Point
    body: Line
    # 添加新的验证
    @validator('body')
    def validate_body_length(cls, v):
        length = ((v.x2 - v.x1)**2 + (v.y2 - v.y1)**2)**0.5
        if length < 50 or length > 150:
            raise ValueError('Body length out of range')
        return v
```

### 动画引擎 (`static/js/animator.js`)

SVG动画渲染核心。

**主要类方法**：
- `loadAnimation(data)`: 加载动画数据
- `play()`: 播放动画
- `pause()`: 暂停
- `restart()`: 重新开始
- `exportSVG()`: 导出SVG

**扩展动画效果**：

```javascript
// 添加新的缓动函数
this.timeline.to(elements.head, {
    attr: { cy: pose.head.cy },
    duration: frameDuration,
    ease: 'elastic.out(1, 0.3)'  // 弹性效果
}, frameStartTime);
```

## API端点开发

### 添加新端点

在 `app.py` 中：

```python
@app.route('/api/new_endpoint', methods=['POST'])
def new_endpoint():
    try:
        data = request.get_json()
        # 处理逻辑
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
```

## 前端开发

### 添加新功能

1. **HTML** (`templates/index.html`)
```html
<button id="newFeatureBtn">新功能</button>
```

2. **CSS** (`static/css/style.css`)
```css
#newFeatureBtn {
    /* 样式 */
}
```

3. **JavaScript** (`static/js/app.js`)
```javascript
document.getElementById('newFeatureBtn').addEventListener('click', () => {
    // 功能实现
});
```

## 测试

### 手动测试

```bash
# 启动服务器
python app.py

# 在另一个终端测试API
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"story": "测试故事"}'
```

### 单元测试（计划中）

```python
# tests/test_llm_service.py
import pytest
from backend.llm_service import LLMService

def test_generate_animation():
    service = LLMService()
    result = service.generate_animation("简单测试")
    assert 'scenes' in result
```

## 常见开发任务

### 1. 修改火柴人样式

编辑 `static/css/style.css`:

```css
.stick-figure-head {
    stroke-width: 4;  /* 加粗头部线条 */
}
```

### 2. 调整动画速度

编辑 `static/js/animator.js`:

```javascript
// 修改缓动函数
ease: 'power2.inOut'  // 更快
ease: 'power1.inOut'  // 更慢
```

### 3. 添加新的动作模板

虽然我们不使用预定义模板，但可以在Prompt中添加更多示例。

编辑 `backend/prompt_template.py`:

```python
# 添加新的动作类型参考
- **奔跑**: 腿大幅度摆动，身体前倾30度，手臂快速摆动
```

### 4. 支持更多角色

修改 `backend/prompt_template.py` 中的画布宽度建议：

```python
- 画布尺寸：1200px 宽 × 600px 高  # 更宽，支持更多角色
```

## 性能优化

### 1. 缓存LLM响应

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_generate(story: str):
    # 缓存相同故事的结果
    pass
```

### 2. 压缩响应

```python
from flask import Flask
from flask_compress import Compress

app = Flask(__name__)
Compress(app)
```

### 3. 异步处理

```python
from flask import Flask
from threading import Thread

def generate_async(story):
    # 后台生成
    pass

@app.route('/api/generate_async', methods=['POST'])
def generate_async_endpoint():
    thread = Thread(target=generate_async, args=(story,))
    thread.start()
    return jsonify({'status': 'processing'})
```

## 部署

### 生产环境配置

1. **使用Gunicorn**

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Nginx反向代理**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. **环境变量**

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
```

## 贡献指南

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 问题排查

### LLM返回格式错误

检查 `backend/llm_service.py` 中的JSON解析逻辑。

### 动画不显示

1. 检查浏览器控制台错误
2. 验证SVG坐标范围
3. 确认GSAP库加载成功

### API超时

1. 增加超时时间
2. 使用更快的模型
3. 简化Prompt

## 资源链接

- [Flask文档](https://flask.palletsprojects.com/)
- [GSAP文档](https://greensock.com/docs/)
- [SVG规范](https://www.w3.org/TR/SVG2/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Anthropic API](https://docs.anthropic.com/)

# API文档

## 基础信息

- **Base URL**: `http://localhost:5000/api`
- **Content-Type**: `application/json`
- **编码**: UTF-8

## 端点列表

### 1. 生成动画

生成火柴人动画数据。

**请求**

```http
POST /api/generate
Content-Type: application/json

{
  "story": "小明从左边走到右边并挥手"
}
```

**参数**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| story | string | 是 | 故事描述（自然语言） |

**响应**

```json
{
  "success": true,
  "message": "Animation generated successfully",
  "data": {
    "title": "动画标题",
    "description": "动画描述",
    "canvas": {
      "width": 800,
      "height": 600
    },
    "characters": [
      {
        "id": "char_1",
        "name": "小明",
        "color": "#2196F3"
      }
    ],
    "scenes": [
      {
        "id": "scene_1",
        "duration": 2000,
        "description": "场景描述",
        "frames": [
          {
            "timestamp": 0,
            "characters": {
              "char_1": {
                "head": { "cx": 200, "cy": 380, "r": 20 },
                "body": { "x1": 200, "y1": 400, "x2": 200, "y2": 480 },
                "left_arm": { "x1": 200, "y1": 420, "x2": 170, "y2": 470 },
                "right_arm": { "x1": 200, "y1": 420, "x2": 230, "y2": 470 },
                "left_leg": { "x1": 200, "y1": 480, "x2": 180, "y2": 540 },
                "right_leg": { "x1": 200, "y1": 480, "x2": 220, "y2": 540 }
              }
            },
            "text": "旁白文字"
          }
        ]
      }
    ]
  }
}
```

**错误响应**

```json
{
  "success": false,
  "message": "Error message"
}
```

**状态码**

- `200` - 成功
- `400` - 请求参数错误
- `500` - 服务器内部错误

---

### 2. 健康检查

检查服务状态。

**请求**

```http
GET /api/health
```

**响应**

```json
{
  "status": "healthy",
  "provider": "openai"
}
```

---

## 数据结构说明

### AnimationData

完整的动画数据结构。

```typescript
interface AnimationData {
  title: string;              // 动画标题
  description: string;         // 动画描述
  canvas: Canvas;             // 画布配置
  characters: Character[];    // 角色列表
  scenes: Scene[];           // 场景列表
}
```

### Canvas

画布配置。

```typescript
interface Canvas {
  width: number;   // 宽度（像素）
  height: number;  // 高度（像素）
}
```

### Character

角色定义。

```typescript
interface Character {
  id: string;      // 唯一标识符
  name: string;    // 角色名称
  color: string;   // 颜色（十六进制）
}
```

### Scene

动画场景。

```typescript
interface Scene {
  id: string;           // 场景ID
  duration: number;     // 持续时间（毫秒）
  description: string;  // 场景描述
  frames: Frame[];      // 关键帧列表
}
```

### Frame

动画关键帧。

```typescript
interface Frame {
  timestamp: number;                    // 时间戳（毫秒）
  characters: { [id: string]: Pose };  // 角色姿势
  text?: string;                       // 旁白文字（可选）
}
```

### Pose

火柴人姿势。

```typescript
interface Pose {
  head: Circle;      // 头部
  body: Line;        // 身体
  left_arm: Line;    // 左臂
  right_arm: Line;   // 右臂
  left_leg: Line;    // 左腿
  right_leg: Line;   // 右腿
}
```

### Circle

圆形（头部）。

```typescript
interface Circle {
  cx: number;  // 圆心X坐标
  cy: number;  // 圆心Y坐标
  r: number;   // 半径
}
```

### Line

线段（身体/四肢）。

```typescript
interface Line {
  x1: number;  // 起点X坐标
  y1: number;  // 起点Y坐标
  x2: number;  // 终点X坐标
  y2: number;  // 终点Y坐标
}
```

---

## 使用示例

### Python示例

```python
import requests

url = "http://localhost:5000/api/generate"
data = {
    "story": "小明从左边走到右边并挥手"
}

response = requests.post(url, json=data)
result = response.json()

if result['success']:
    animation_data = result['data']
    print(f"生成成功：{animation_data['title']}")
else:
    print(f"生成失败：{result['message']}")
```

### JavaScript示例

```javascript
const generateAnimation = async (story) => {
  const response = await fetch('http://localhost:5000/api/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ story })
  });
  
  const result = await response.json();
  
  if (result.success) {
    console.log('生成成功：', result.data.title);
    return result.data;
  } else {
    console.error('生成失败：', result.message);
    throw new Error(result.message);
  }
};

// 使用
generateAnimation('小明从左边走到右边并挥手')
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

### cURL示例

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"story": "小明从左边走到右边并挥手"}'
```

---

## 最佳实践

### 1. 故事描述建议

✅ **好的描述**
- "小明从左边走到右边，然后跳起来庆祝"
- "两个人面对面站着，互相挥手打招呼，然后击掌"

❌ **不好的描述**
- "做一些动作"（太模糊）
- "瞬间移动到另一边"（不符合物理规律）

### 2. 性能优化

- 故事长度建议：50-200字
- 场景数量：1-5个
- 关键帧数量：每个场景3-10帧

### 3. 错误处理

始终检查 `success` 字段：

```javascript
if (result.success) {
  // 处理成功
} else {
  // 处理错误
  console.error(result.message);
}
```

---

## 限制说明

- 单次请求超时：30秒
- 故事最大长度：500字符
- 并发请求：建议 < 10个/秒

---

## 变更日志

### v1.0.0 (2026-01-17)
- 初始版本发布
- 支持OpenAI和Anthropic
- 完整的动画生成功能

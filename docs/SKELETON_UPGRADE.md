# 🦴 骨骼系统升级指南

## 📋 升级概述

本次升级将火柴人动画系统从**基于坐标的底层系统**升级为**基于骨骼的语义系统**，充分利用LLM的优势。

### 核心改进

| 维度 | 升级前 | 升级后 |
|------|--------|--------|
| **自由度** | 23个坐标参数 | 11个语义角度 + 身体姿态 |
| **LLM工作** | 计算23个坐标 | 描述角度和姿态 |
| **物理约束** | ❌ 无，肢体可断开 | ✅ 自动保持连接 |
| **动作复杂度** | ⭐⭐ 简单 | ⭐⭐⭐⭐⭐ 丰富 |
| **物品支持** | ❌ 不支持 | ✅ 12种道具 + 交互 |

---

## 🏗️ 架构变化

### 新增模块

1. **`backend/skeleton.py`** - 骨骼系统核心
   - 分层关节结构（头→颈→胸→腰）
   - 语义姿态描述（SemanticPose）
   - 标准人体比例

2. **`backend/kinematics.py`** - 正向运动学引擎
   - 角度→坐标自动转换
   - 保证骨骼长度恒定
   - 平滑姿态插值

3. **`backend/props.py`** - 物品系统
   - 12种预定义道具（剑、球、盾牌等）
   - 关节附着（grab/release/throw）
   - 变换继承

4. **`backend/animation_validator_enhanced.py`** - 增强验证器
   - 支持双格式（骨骼 + 旧版）
   - 自动格式检测
   - 语义姿态验证

5. **`backend/prompt_template_skeleton.py`** - 骨骼专用Prompt
   - 面向角度的描述方式
   - 物品使用示例
   - 常见姿态参考

6. **`static/js/skeleton_animator.js`** - 骨骼渲染器
   - 分层骨骼渲染
   - 物品附着可视化
   - 向后兼容旧格式

---

## 🎯 LLM视角的改变

### 之前（坐标模式）

LLM需要手动计算所有坐标：

```json
{
  "head": {"cx": 400, "cy": 380, "r": 20},
  "body": {"x1": 400, "y1": 400, "x2": 400, "y2": 480},
  "left_arm": {"x1": 400, "y1": 420, "x2": 370, "y2": 470},
  // ... 还要计算右臂、双腿的坐标
}
```

**问题：**
- 难以保证肢体连接
- 容易出现不自然姿态
- 无法理解动作语义

### 现在（骨骼模式）

LLM用直观的角度描述姿态：

```json
{
  "semantic_poses": {
    "char_1": {
      "body_lean": 15,              // 身体前倾15°
      "left_shoulder_angle": -30,   // 左臂向上摆30°
      "left_elbow_bend": 20,        // 肘部弯曲20°
      "right_shoulder_angle": 45,   // 右臂挥拳
      "right_elbow_bend": 10,       // 几乎伸直
      "left_hip_angle": 30,         // 左腿前踏
      "left_knee_bend": 40,
      "right_hip_angle": -10,       // 右腿支撑
      "right_knee_bend": 15,
      "root_x": 350,
      "root_y": 385
    }
  }
}
```

**优势：**
- ✅ 描述符合人类思维（"前倾"、"挥拳"）
- ✅ 系统自动计算坐标并保证物理合理性
- ✅ 更容易生成复杂动作
- ✅ 支持物品交互

---

## 🎮 新增物品系统

### 可用道具

| 类型 | 描述 | 典型用途 |
|------|------|---------|
| `sword` | 中世纪剑 | 战斗动画 |
| `katana` | 日本武士刀 | 武术动画 |
| `shield` | 风筝盾 | 防御姿态 |
| `ball` | 圆球 | 运动动画 |
| `basketball` | 篮球 | 投篮动画 |
| `box` | 箱子 | 搬运动作 |
| `stick` | 木棍 | 格斗/行走 |
| `axe` | 战斧 | 砍伐动作 |
| `flag` | 旗帜 | 举旗庆祝 |
| `umbrella` | 雨伞 | 日常场景 |
| `briefcase` | 公文包 | 商务场景 |
| `cup` | 杯子 | 喝水动作 |

### 物品交互动作

- **grab** - 抓取物品（附着到手部）
- **release** - 释放物品
- **throw** - 投掷物品（带轨迹）
- **place** - 放置物品到指定位置
- **swing** - 挥舞物品（武器动作）

### 使用示例

```json
{
  "props": [
    {"id": "sword_1", "type": "sword", "x": 300, "y": 500}
  ],
  "frames": [
    {
      "timestamp": 0,
      "semantic_poses": {
        "char_1": {
          "right_shoulder_angle": 80,
          "right_elbow_bend": 60,
          // ...
        }
      },
      "prop_states": [
        {
          "prop_id": "sword_1",
          "attached_to_character": "char_1",
          "attached_to_joint": "right_hand"
        }
      ]
    }
  ],
  "prop_interactions": [
    {
      "character_id": "char_1",
      "prop_id": "sword_1",
      "action": "grab",
      "joint_name": "right_hand",
      "timestamp": 0
    }
  ]
}
```

---

## 📐 语义姿态参数说明

### 身体姿态

- `body_lean`: -45 ~ 45° （负=后仰，正=前倾）
- `body_twist`: -90 ~ 90° （躯干旋转）
- `root_x`: 0-800 （水平位置）
- `root_y`: 200-550 （垂直位置，越小越高）

### 手臂角度

- `left/right_shoulder_angle`: -180 ~ 180°
  - 0° = 水平右伸
  - 90° = 向下
  - -90° = 向上
  - 180° = 水平左伸
- `left/right_elbow_bend`: 0 ~ 180° （0=伸直，180=完全弯曲）

### 腿部角度

- `left/right_hip_angle`: -90 ~ 135°
  - 0° = 站直
  - 正值 = 腿向前
  - 负值 = 腿向后
- `left/right_knee_bend`: 0 ~ 150° （0=伸直，150=深蹲）

---

## 🚀 使用方法

### 启动系统

系统**自动兼容**新旧格式，无需修改启动命令：

```bash
python app.py
```

### LLM生成新格式

默认使用骨骼系统：

```python
llm_service = get_llm_service()
animation_data = llm_service.generate_animation("两个武士决斗")
# 自动生成骨骼格式，包含语义姿态和物品
```

### 强制使用旧格式

如果需要旧格式：

```python
animation_data = llm_service.generate_animation("故事", use_skeleton=False)
```

---

## 🎬 常见姿态示例

### 站立（中立姿态）

```python
body_lean=0, body_twist=0,
left_shoulder_angle=-30, left_elbow_bend=10,
right_shoulder_angle=30, right_elbow_bend=10,
left_hip_angle=0, left_knee_bend=5,
right_hip_angle=0, right_knee_bend=5,
root_x=400, root_y=380
```

### 行走（左腿迈步）

```python
body_lean=5,
left_shoulder_angle=30, left_elbow_bend=20,
right_shoulder_angle=-30, right_elbow_bend=20,
left_hip_angle=-30, left_knee_bend=30,
right_hip_angle=20, right_knee_bend=10,
root_y=385
```

### 跳跃

```python
body_lean=-10,
left_shoulder_angle=-120, left_elbow_bend=30,
right_shoulder_angle=-120, right_elbow_bend=30,
left_hip_angle=-45, left_knee_bend=30,
right_hip_angle=-45, right_knee_bend=30,
root_y=280  # 腾空
```

### 深蹲

```python
body_lean=30,
left_shoulder_angle=-20, left_elbow_bend=30,
right_shoulder_angle=20, right_elbow_bend=30,
left_hip_angle=90, left_knee_bend=120,
right_hip_angle=90, right_knee_bend=120,
root_y=450  # 接近地面
```

### 出拳（右手）

```python
body_lean=15, body_twist=-20,
left_shoulder_angle=-40, left_elbow_bend=60,
right_shoulder_angle=0, right_elbow_bend=10,  # 伸直出拳
left_hip_angle=10, left_knee_bend=20,
right_hip_angle=5, right_knee_bend=15
```

---

## 🔄 向后兼容性

系统**完全兼容**旧格式动画：

- ✅ 旧格式数据可正常播放
- ✅ 自动检测格式类型
- ✅ 混合使用不受影响
- ✅ 渲染器统一处理

---

## 🎓 给LLM的建议

1. **使用角度思考，而非坐标**
   - 描述"前倾15度"，而非"y=385"
   - 描述"抬臂90度"，而非计算端点坐标

2. **利用物品增强表现力**
   - 战斗场景 → 添加 sword/shield
   - 运动场景 → 添加 ball/basketball
   - 日常场景 → 添加 cup/briefcase

3. **平滑过渡很重要**
   - 每个主要动作4-8个关键帧
   - 时间间隔合理（快动作300-600ms，慢动作1500-2500ms）

4. **物理合理性**
   - 行走时手臂腿部对称摆动
   - 前倾时调整重心
   - 跳跃时root_y变化显著

---

## 🐛 故障排除

### Q: 动画显示异常？

检查浏览器控制台，确认加载了 `skeleton_animator.js`

### Q: 旧动画无法播放？

系统自动兼容，如有问题检查：
1. 数据格式是否完整
2. 控制台是否有错误

### Q: LLM生成的坐标超出范围？

新系统有内置验证：
- Pydantic模型自动限制参数范围
- 角度超限会报错
- 坐标自动裁剪到画布内

---

## 📊 性能对比

| 指标 | 旧系统 | 新系统 |
|------|--------|--------|
| LLM生成难度 | ⭐⭐⭐⭐ | ⭐⭐ |
| 动作复杂度 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 物理合理性 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 表现力 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 开发复杂度 | ⭐⭐ | ⭐⭐⭐⭐ |

---

## 🎉 总结

骨骼系统升级将火柴人动画提升到了全新水平：

✅ **LLM更容易生成**：从坐标计算解放，专注于动作设计  
✅ **动作更加丰富**：骨骼系统支持更复杂的姿态  
✅ **物理自动保证**：关节连接、长度恒定自动维护  
✅ **物品系统加持**：12种道具极大增强表现力  
✅ **向后兼容**：旧动画继续可用  

**现在，您可以让LLM生成更加生动、复杂、富有表现力的火柴人动画了！** 🎬✨

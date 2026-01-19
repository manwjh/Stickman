# 🔧 五级流水线技术流程详解

> 详细说明每个技术节点的工作原理、数据流转和LLM调用机制

## ❓ 常见问题 FAQ

### Q1: Level 3的"上下文"是带上全部关键帧吗？

**不是！** 上下文使用**滑动窗口**机制：

| 项目 | 说明 |
|------|------|
| 窗口大小 | 3帧（可配置） |
| 实际提供给LLM | **仅上一帧**的关键关节坐标 |
| 关节数量 | 7个关键关节（非全部16个） |
| Token消耗 | ~200 tokens/帧 |

**为什么不提供所有历史帧？**
1. **Token效率**：每帧完整坐标约400+ tokens，13帧=5000+ tokens
2. **质量更好**：只关注相邻帧过渡，LLM更专注
3. **足够平滑**：帧到帧的平滑已经足够保证连续性

**实际Prompt示例**：
```
下一个动作：角色向前迈步

⚠️ 重要：必须从以下姿势平滑过渡！
上一帧姿势：
  - head: (400.0, 150.0)
  - neck: (400.0, 180.0)
  - waist: (400.0, 260.0)
  - left_hand: (340.0, 300.0)
  - right_hand: (460.0, 300.0)
  - left_foot: (360.0, 380.0)
  - right_foot: (440.0, 380.0)

当前位置：(400.0, 260.0)
移动速度：(5.0, 0.0) px/frame
朝向：right

要求：
1. 确保动作流畅过渡，避免突兀跳变
2. 保持角色的移动趋势（除非明确改变方向）
3. 骨骼长度必须与上一帧保持一致
```

### Q2: 滑动窗口保留3帧，但只用1帧？

是的！窗口保留3帧是为了：
- **计算速度/趋势**：需要比较前2-3帧
- **检测跳变**：验证时需要历史数据
- **未来扩展**：可以实验性提供更多上下文

但**当前策略**是只提供上一帧给LLM。

---

## 📐 整体架构图

```
用户输入故事（自然语言）
        ↓
┌──────────────────────────────────────┐
│  Level 1: Story Planner              │
│  ├─ LLM调用 #1                       │
│  ├─ 输入: 原始故事文本               │
│  ├─ 输出: ScenePlan对象              │
│  └─ 关键: 结构化数据提取             │
└──────────────────────────────────────┘
        ↓ ScenePlan
┌──────────────────────────────────────┐
│  Level 2: Choreographer              │
│  ├─ LLM调用 #2                       │
│  ├─ 输入: ScenePlan + 动作列表       │
│  ├─ 输出: KeyframeDescription[]      │
│  └─ 关键: 时间轴规划                │
└──────────────────────────────────────┘
        ↓ KeyframeDescription[]
┌──────────────────────────────────────┐
│  Level 3: Animator LLM               │
│  ├─ LLM调用 #3-N（逐帧生成）         │
│  ├─ 输入: 单个关键帧描述             │
│  │    + 前N帧关节坐标（滑动窗口）    │
│  │    + 角色状态（位置/速度/朝向）   │
│  ├─ 输出: 关节坐标 (JSON)            │
│  └─ 关键: 上下文记忆系统             │
│      - 窗口大小: 3帧                 │
│      - 仅保留关键关节位置            │
└──────────────────────────────────────┘
        ↓ Keyframes with Coordinates
┌──────────────────────────────────────┐
│  Level 4: Constraint Validator       │
│  ├─ 无LLM调用（纯算法验证）          │
│  ├─ 输入: 关节坐标                   │
│  ├─ 输出: 验证结果 + 反馈            │
│  └─ 关键: 反馈循环（回到Level 3）   │
└──────────────────────────────────────┘
        ↓ Validated Keyframes
┌──────────────────────────────────────┐
│  Level 5: Post Processor             │
│  ├─ 无LLM调用（纯算法处理）          │
│  ├─ 输入: 验证后的关键帧             │
│  ├─ 输出: 优化后的最终动画           │
│  └─ 关键: 插值和平滑                 │
└──────────────────────────────────────┘
        ↓
最终动画数据（JSON）
```

---

## 🎯 Level 1: Story Planner - 技术流程

### 1.1 输入处理

**输入格式**:
```python
story: str  # 用户的自然语言故事
# 例如: "小明站立，然后向右挥手问好，最后恢复站立姿势"
```

**预处理步骤**:
```python
# 1. 安全清理
story = sanitize_input(story)  # 去除危险字符

# 2. 长度验证
if len(story) < 5:
    raise ValueError("故事太短")
if len(story) > 10000:
    raise ValueError("故事太长")

# 3. 去除首尾空白
story = story.strip()
```

### 1.2 构建LLM Prompt

**系统提示词**（固定）:
```python
SYSTEM_PROMPT = """
你是一位专业的故事分析师和动画导演。

任务：
1. 识别角色（从故事中找出角色，分配ID和颜色）
2. 识别道具（武器、工具等）
3. 分解动作（将故事拆分为具体的动作序列）
4. 估算时长（为每个动作估算合理的毫秒数）
5. 设定场景（位置、氛围等）

返回JSON格式：
{
  "story_summary": "故事概要",
  "characters": [
    {"id": "char1", "name": "...", "role": "...", "color": "#..."}
  ],
  "props": [
    {"id": "prop1", "type": "...", "name": "..."}
  ],
  "actions": [
    {
      "action_id": "action1",
      "description": "详细的动作描述",
      "duration_ms": 1000,
      "character_ids": ["char1"],
      "tags": ["stand", "wave"],
      "intensity": "normal"
    }
  ],
  "setting": {...}
}
"""
```

**用户提示词**（动态）:
```python
USER_PROMPT = f"""
请分析以下故事并生成场景计划：

故事：
{story}

要求：
- 至少生成3-5个动作
- 每个动作都要详细描述
- 时长合理分配
"""
```

### 1.3 LLM调用

**调用参数**:
```python
import litellm

response = litellm.completion(
    model="openai/Qwen3-Next-80B-Instruct",  # 模型
    api_key=os.getenv('PERFXCLOUD_API_KEY'),  # API密钥
    api_base="https://deepseek.perfxlab.cn/v1",  # API端点
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT}
    ],
    temperature=0.7,  # 创造性（0-1）
    max_tokens=2048,  # 最大输出token
    response_format={"type": "json_object"}  # 强制JSON输出
)
```

**关键参数说明**:
- `temperature=0.7`: 平衡创造性和一致性
- `max_tokens=2048`: 足够返回完整的场景规划
- `response_format`: 确保返回有效的JSON

### 1.4 响应处理

**原始响应**:
```python
content = response.choices[0].message.content
# 类型: str
# 内容: JSON字符串
```

**JSON解析**:
```python
import json

# 处理可能的markdown包裹（Anthropic等）
if "```json" in content:
    content = content.split("```json")[1].split("```")[0].strip()

# 解析JSON
result = json.loads(content)
```

**数据验证与转换**:
```python
# 转换为ScenePlan对象
scene_plan = ScenePlan(
    story_summary=result.get("story_summary", ""),
    characters=[
        Character(
            id=c["id"],
            name=c["name"],
            role=c.get("role", "character"),
            color=c.get("color", "#2196F3")
        )
        for c in result.get("characters", [])
    ],
    props=[
        Prop(
            id=p["id"],
            type=p["type"],
            name=p["name"]
        )
        for p in result.get("props", [])
    ],
    actions=[
        Action(
            action_id=a["action_id"],
            description=a["description"],
            duration_ms=a["duration_ms"],
            character_ids=a.get("character_ids", ["char1"]),
            tags=a.get("tags", []),
            intensity=a.get("intensity", "normal")
        )
        for a in result.get("actions", [])
    ],
    setting=result.get("setting", {})
)
```

### 1.5 输出格式

**ScenePlan对象结构**:
```python
@dataclass
class ScenePlan:
    story_summary: str
    characters: List[Character]  # 角色列表
    props: List[Prop]            # 道具列表
    actions: List[Action]        # 动作序列
    setting: Dict[str, Any]      # 场景设置
    total_duration_ms: int       # 总时长（自动计算）
```

**传递给下一级**:
```python
# Level 1 → Level 2
return scene_plan  # ScenePlan对象
```

---

## 🎭 Level 2: Choreographer - 技术流程

### 2.1 输入处理

**接收数据**:
```python
scene_plan: ScenePlan  # 来自Level 1
```

**数据提取**:
```python
# 提取关键信息
characters = scene_plan.characters
actions = scene_plan.actions
props = scene_plan.props
setting = scene_plan.setting
```

### 2.2 构建LLM Prompt

**系统提示词**:
```python
SYSTEM_PROMPT = """
你是一位专业的动作编排师（Choreographer）。

任务：为每个动作生成2-3个关键帧

每个关键帧需要包含：
1. timestamp_ms: 精确的时间戳
2. description: 详细的姿势描述（包括头部、躯干、手臂、腿部）
3. character_ids: 涉及的角色
4. transition: 过渡类型（smooth/sudden）

返回JSON格式：
{
  "keyframes": [
    {
      "timestamp_ms": 0,
      "action_id": "action1",
      "description": "详细的身体姿态描述",
      "character_ids": ["char1"],
      "transition": "smooth"
    }
  ]
}
"""
```

**用户提示词**（构建动作列表）:
```python
# 构建prompt
prompt_parts = [
    "请为以下场景计划编排关键帧：",
    "",
    f"**故事概要**: {scene_plan.story_summary}",
    "",
    "**角色**:"
]

for char in scene_plan.characters:
    prompt_parts.append(f"  - {char.id} ({char.name}): {char.role}")

prompt_parts.append("")
prompt_parts.append("**动作序列**:")

for action in scene_plan.actions:
    prompt_parts.append(f"")
    prompt_parts.append(f"动作 {action.action_id}:")
    prompt_parts.append(f"  - 描述: {action.description}")
    prompt_parts.append(f"  - 时长: {action.duration_ms}ms")
    prompt_parts.append(f"  - 角色: {', '.join(action.character_ids)}")
    prompt_parts.append(f"  - 强度: {action.intensity}")

prompt_parts.append("")
prompt_parts.append("请为每个动作生成2-3个关键帧，确保动作流畅连贯。")

USER_PROMPT = "\n".join(prompt_parts)
```

### 2.3 LLM调用

```python
response = litellm.completion(
    model="openai/Qwen3-Next-80B-Instruct",
    api_key=os.getenv('PERFXCLOUD_API_KEY'),
    api_base="https://deepseek.perfxlab.cn/v1",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT}
    ],
    temperature=0.7,
    max_tokens=2048,
    response_format={"type": "json_object"}
)
```

### 2.4 响应处理

```python
content = response.choices[0].message.content
result = json.loads(content)
keyframe_descriptions = result.get("keyframes", [])
```

### 2.5 输出格式

**KeyframeDescription结构**:
```python
[
    {
        "timestamp_ms": 0,
        "action_id": "action1",
        "description": "详细姿势描述",
        "character_ids": ["char1"],
        "transition": "smooth"
    },
    # ... 更多关键帧
]
```

**传递给下一级**:
```python
# Level 2 → Level 3
return keyframe_descriptions  # List[Dict]
```

---

## 🎨 Level 3: Animator LLM - 技术流程（核心）

### 3.1 上下文记忆系统初始化

```python
class ContextMemory:
    def __init__(self, window_size=3):
        self.frame_history = deque(maxlen=window_size)  # 滑动窗口
        self.character_states = {}  # 角色状态追踪
```

**记忆内容**:
```python
{
    "char_id": "char1",
    "joints": {关节坐标},
    "timestamp": 帧序号
}
```

### 3.2 骨骼系统配置

**根据DOF级别选择骨骼系统**:
```python
if dof_level == '6dof':
    skeleton = Skeleton6DOF()
elif dof_level == '12dof':
    skeleton = Skeleton12DOF()  # 本次使用
```

**获取骨骼系统的Prompt模板**:
```python
skeleton_prompt = skeleton.get_system_prompt()
# 包含：
# - 关节列表
# - 标准比例
# - 约束规则
# - JSON格式要求
```

### 3.3 逐帧生成循环

```python
for i, kf_desc in enumerate(keyframe_descriptions):
    # 关键决策点：是否使用上下文
    use_context = (i > 0)  # 第一帧不用上下文
    
    if use_context:
        # 构建带上下文的prompt
        prompt = context_memory.get_context_prompt(
            next_action=kf_desc["description"],
            char_id="char1"
        )
    else:
        # 简单prompt
        prompt = f"请为以下姿势生成关节坐标：\n\n{kf_desc['description']}"
```

### 3.4 上下文Prompt构建（关键技术点）

**❓ 重要说明：上下文不是全部关键帧！**

上下文记忆系统使用**滑动窗口**机制：
- 窗口大小：3帧（可配置）
- 内容：仅保留**前N帧**的关节坐标
- 策略：**只提供上一帧**给LLM，不是所有历史帧
- 原因：
  1. 减少Token消耗
  2. 避免混淆LLM（过多历史信息反而降低质量）
  3. 相邻帧之间的平滑过渡已经足够

```python
def get_context_prompt(self, next_action: str, char_id: str) -> str:
    # 获取上一帧（不是所有帧！）
    last_frame = self.get_last_frame(char_id)
    state = self.character_states.get(char_id, {})
    
    # 构建上下文信息
    context_parts = [
        f"下一个动作：{next_action}",
        "",
        "⚠️ 重要：必须从以下姿势平滑过渡！",
        "上一帧姿势："  # 只有上一帧！
    ]
    
    # 显示关键关节的坐标（简化版，非全部16关节）
    key_joints = ["head", "neck", "waist", "left_hand", "right_hand", 
                  "left_foot", "right_foot"]
    last_joints = last_frame["joints"]
    
    for joint_name in key_joints:
        if joint_name in last_joints:
            j = last_joints[joint_name]
            context_parts.append(f"  - {joint_name}: ({j['x']:.1f}, {j['y']:.1f})")
    
    # 添加运动状态（从滑动窗口计算）
    if state.get("center"):
        center = state["center"]
        velocity = state["velocity"]
        context_parts.append("")
        context_parts.append(f"当前位置：({center['x']:.1f}, {center['y']:.1f})")
        context_parts.append(f"移动速度：({velocity['x']:.1f}, {velocity['y']:.1f}) px/frame")
        context_parts.append(f"朝向：{state.get('facing', 'unknown')}")
    
    # 添加约束要求
    context_parts.append("")
    context_parts.append("要求：")
    context_parts.append("1. 确保动作流畅过渡，避免突兀跳变")
    context_parts.append("2. 保持角色的移动趋势（除非明确改变方向）")
    context_parts.append("3. 骨骼长度必须与上一帧保持一致")
    
    return "\n".join(context_parts)
```

### 3.5 LLM调用（每帧）

```python
response = litellm.completion(
    model="openai/Qwen3-Next-80B-Instruct",
    api_key=os.getenv('PERFXCLOUD_API_KEY'),
    api_base="https://deepseek.perfxlab.cn/v1",
    messages=[
        {
            "role": "system",
            "content": skeleton.get_system_prompt()  # 12DOF系统prompt
        },
        {
            "role": "user",
            "content": prompt  # 带上下文或不带
        }
    ],
    temperature=0.7,
    max_tokens=4096,  # 更大，因为包含所有关节坐标
    response_format={"type": "json_object"}
)
```

### 3.6 响应解析

```python
content = response.choices[0].message.content
result = json.loads(content)

# LLM返回格式
{
  "characters": [...],
  "keyframes": [
    {
      "timestamp_ms": 0,
      "description": "...",
      "characters": {
        "char1": {
          "dof": 12,
          "joints": {
            "head": {"x": 400, "y": 240},
            "neck": {"x": 400, "y": 260},
            // ... 其他11个关节
          }
        }
      }
    }
  ]
}

# 提取第一个关键帧（因为我们逐帧请求）
keyframe = result["keyframes"][0]
keyframe["timestamp_ms"] = kf_desc["timestamp_ms"]  # 使用choreographer的时间戳
```

### 3.7 更新上下文记忆

```python
# 提取生成的关节数据
for char_id in character_ids:
    if char_id in keyframe["characters"]:
        char_data = keyframe["characters"][char_id]
        
        # 提取关节
        if "joints" in char_data:
            joints = char_data["joints"]
            
            # 添加到记忆
            context_memory.add_frame(joints, char_id)
            
            # 更新角色状态
            # - 计算中心位置
            # - 计算速度向量
            # - 判断朝向
```

### 3.8 输出格式

**单帧输出**:
```python
{
    "timestamp_ms": 0,
    "description": "站立姿势",
    "characters": {
        "char1": {
            "dof": 12,
            "joints": {
                "head": {"x": 400, "y": 240},
                "neck": {"x": 400, "y": 260},
                "waist": {"x": 400, "y": 320},
                "left_shoulder": {"x": 380, "y": 265},
                "left_hand": {"x": 350, "y": 310},
                "right_shoulder": {"x": 420, "y": 265},
                "right_hand": {"x": 450, "y": 310},
                "left_hip": {"x": 385, "y": 320},
                "left_foot": {"x": 385, "y": 370},
                "right_hip": {"x": 415, "y": 320},
                "right_foot": {"x": 415, "y": 370}
            }
        }
    }
}
```

**累积所有帧后传递给下一级**:
```python
# Level 3 → Level 4
animation_data = {
    "characters": character_list,
    "keyframes": generated_keyframes,  # 所有生成的帧
    "dof_level": "12dof"
}
```

---

## 🔍 Level 4: Constraint Validator - 技术流程

### 4.1 验证算法（无LLM）

**关键决策点：对每一帧进行验证**

```python
for keyframe in animation_data["keyframes"]:
    is_valid, errors = validator.validate_keyframe(keyframe)
    
    if not is_valid:
        # 触发反馈循环
        feedback = validator.generate_feedback(errors)
        # 返回Level 3重新生成这一帧
```

### 4.2 骨骼长度验证

```python
def _check_bone_lengths(self, joints: Dict):
    violations = []
    
    # 定义骨骼连接和期望长度
    BONE_CHECKS = {
        "neck_to_head": ("neck", "head", 20),
        "neck_to_waist": ("neck", "waist", 60),
        "left_arm": ("left_shoulder", "left_hand", 50),
        "right_arm": ("right_shoulder", "right_hand", 50),
        "left_leg": ("left_hip", "left_foot", 50),
        "right_leg": ("right_hip", "right_foot", 50),
    }
    
    for bone_name, (j1_name, j2_name, expected) in BONE_CHECKS.items():
        # 计算实际长度
        actual = math.sqrt(
            (joints[j1_name]["x"] - joints[j2_name]["x"])**2 +
            (joints[j1_name]["y"] - joints[j2_name]["y"])**2
        )
        
        # 获取容差
        tolerance = TOLERANCE_MAP.get(bone_name, 0.5)
        min_allowed = expected * (1 - tolerance)
        max_allowed = expected * (1 + tolerance)
        
        # 检查是否在范围内
        if actual < min_allowed or actual > max_allowed:
            deviation = abs(actual - expected) / expected
            violations.append({
                "type": "bone_length_violation",
                "bone": bone_name,
                "expected": expected,
                "actual": actual,
                "deviation_percent": deviation * 100
            })
    
    return violations
```

### 4.3 反馈生成

```python
def generate_feedback(self, errors: List[str]) -> str:
    feedback_parts = ["检测到以下问题，请修正：", ""]
    
    # 分类错误
    length_errors = [e for e in errors if "长度异常" in e]
    
    if length_errors:
        feedback_parts.append("**骨骼长度问题**:")
        for err in length_errors[:5]:
            feedback_parts.append(f"  - {err}")
        feedback_parts.append("")
    
    feedback_parts.append("请仔细检查骨骼长度，确保符合标准比例。")
    
    return "\n".join(feedback_parts)
```

### 4.4 反馈循环机制

```python
# 在animation_pipeline.py中
for attempt in range(max_retries):
    # 生成关键帧
    keyframe = animator.generate_keyframe(
        description=description,
        use_context=(i > 0)
    )
    
    # 验证
    is_valid, errors = validator.validate_keyframe(keyframe)
    
    if is_valid:
        # 验证通过，继续
        break
    else:
        if attempt < max_retries - 1:
            # 生成反馈
            feedback = validator.generate_feedback(errors)
            
            # 修改description，加入反馈
            description = f"{description}\n\n修正要求：\n{feedback}"
            
            # 下次循环会重新调用LLM
        else:
            # 最后一次尝试失败，使用降级策略
            logger.warning("达到最大重试次数，使用降级数据")
```

### 4.5 输出格式

```python
# Level 4 → Level 5
{
    "is_valid": True,
    "valid_keyframes": 13,
    "invalid_keyframes": 0,
    "errors": []
}

# 原始animation_data继续传递
```

---

## ✨ Level 5: Post Processor - 技术流程

### 5.1 插值算法

```python
def _interpolate_keyframes(self, keyframes):
    result = [keyframes[0]]  # 第一帧
    
    for i in range(len(keyframes) - 1):
        current_kf = keyframes[i]
        next_kf = keyframes[i + 1]
        
        # 计算时间差
        time_diff = next_kf["timestamp_ms"] - current_kf["timestamp_ms"]
        steps = self.interpolation_frames  # 例如：2
        
        # 生成中间帧
        for step in range(1, steps + 1):
            t = step / (steps + 1)  # 插值因子：0.33, 0.67
            
            # 线性插值
            interp_kf = self._lerp_keyframe(current_kf, next_kf, t)
            result.append(interp_kf)
        
        result.append(next_kf)  # 目标帧
    
    return result
```

**LERP（线性插值）**:
```python
def _lerp_keyframe(self, kf1, kf2, t):
    # 插值时间戳
    new_timestamp = kf1["timestamp_ms"] + (kf2["timestamp_ms"] - kf1["timestamp_ms"]) * t
    
    # 插值每个角色的关节
    new_kf = {
        "timestamp_ms": int(new_timestamp),
        "characters": {}
    }
    
    for char_id in kf1["characters"].keys():
        if char_id in kf2["characters"]:
            new_kf["characters"][char_id] = self._lerp_joints(
                kf1["characters"][char_id],
                kf2["characters"][char_id],
                t
            )
    
    return new_kf

def _lerp_joints(self, joints1, joints2, t):
    result = {}
    
    for joint_name in joints1.keys():
        if joint_name in joints2:
            j1 = joints1[joint_name]
            j2 = joints2[joint_name]
            
            # 线性插值：new = start + (end - start) * t
            result[joint_name] = {
                "x": j1["x"] + (j2["x"] - j1["x"]) * t,
                "y": j1["y"] + (j2["y"] - j1["y"]) * t
            }
    
    return result
```

### 5.2 平滑算法

```python
def _smooth_keyframes(self, keyframes):
    result = [keyframes[0]]  # 保留第一帧
    
    for i in range(1, len(keyframes) - 1):
        prev_kf = keyframes[i - 1]
        curr_kf = keyframes[i]
        next_kf = keyframes[i + 1]
        
        # 移动加权平均
        smoothed_kf = {
            "timestamp_ms": curr_kf["timestamp_ms"],
            "characters": {}
        }
        
        for char_id in curr_kf["characters"].keys():
            smoothed_kf["characters"][char_id] = self._smooth_joints(
                prev_kf["characters"][char_id],
                curr_kf["characters"][char_id],
                next_kf["characters"][char_id],
                self.smoothing_factor  # 0.3
            )
        
        result.append(smoothed_kf)
    
    result.append(keyframes[-1])  # 保留最后一帧
    return result

def _smooth_joints(self, prev_joints, curr_joints, next_joints, factor):
    result = {}
    
    for joint_name in curr_joints.keys():
        prev_j = prev_joints[joint_name]
        curr_j = curr_joints[joint_name]
        next_j = next_joints[joint_name]
        
        # 加权平均：(prev*0.3 + curr*0.4 + next*0.3) / 1.0
        result[joint_name] = {
            "x": (prev_j["x"]*factor + curr_j["x"]*(1-factor) + next_j["x"]*factor) / (1+2*factor),
            "y": (prev_j["y"]*factor + curr_j["y"]*(1-factor) + next_j["y"]*factor) / (1+2*factor)
        }
    
    return result
```

### 5.3 输出格式

```python
# Level 5 → 最终输出
{
    "characters": [...],
    "keyframes": optimized_keyframes  # 插值+平滑后
}
```

---

## 📊 关键技术决策点总结

### 决策点1: 何时使用上下文

```python
if frame_index == 0:
    use_context = False  # 第一帧：无上下文
else:
    use_context = True   # 后续帧：使用上下文
```

### 决策点2: 何时触发反馈循环

```python
if validation_failed and attempt < max_retries:
    # 生成反馈，重新调用LLM
    feedback = generate_feedback(errors)
    retry_with_feedback(feedback)
else:
    # 验证通过或达到最大重试次数
    accept_result()
```

### 决策点3: 插值密度

```python
# 根据时间差动态调整
time_diff = next_frame.timestamp - current_frame.timestamp

if time_diff > 1000:  # 超过1秒
    interpolation_steps = 3  # 更多插值
elif time_diff > 500:
    interpolation_steps = 2  # 中等插值
else:
    interpolation_steps = 1  # 少量插值
```

### 决策点4: 容差调整

```python
# 根据DOF级别和部位调整
if dof_level == '6dof':
    TOLERANCE = 0.3  # 严格
elif dof_level == '12dof':
    TOLERANCE = {
        'torso': 0.3,   # 躯干严格
        'arms': 0.5,    # 手臂中等
        'legs': 0.6     # 腿部宽松
    }
```

---

## 🔄 数据流转完整追踪

```python
# 输入
user_story = "小明站立，然后挥手"

# Level 1
scene_plan = story_planner.plan_story(user_story)
# ScenePlan对象

# Level 2
keyframe_descriptions = choreographer.choreograph(scene_plan)
# List[Dict]: [{timestamp_ms, description, ...}]

# Level 3
for kf_desc in keyframe_descriptions:
    keyframe = animator.generate_keyframe(
        kf_desc["description"],
        use_context=True
    )
    # Dict: {timestamp_ms, characters: {char1: {joints: {...}}}}
    
    # Level 4
    is_valid, errors = validator.validate_keyframe(keyframe)
    if not is_valid:
        feedback = validator.generate_feedback(errors)
        # 回到Level 3重试

animation_data = {
    "keyframes": all_keyframes,
    "characters": characters
}

# Level 5
final_animation = post_processor.optimize(animation_data)
# 插值+平滑后的最终数据

# 输出
return final_animation
```

---

## 🎯 LLM调用时机汇总

| Level | LLM调用次数 | 调用时机 | 输入 | 输出 |
|-------|-------------|----------|------|------|
| **Level 1** | 1次 | 开始时 | 原始故事 | ScenePlan |
| **Level 2** | 1次 | 收到ScenePlan后 | ScenePlan | KeyframeDescriptions |
| **Level 3** | N次 | 每个关键帧 | 姿势描述+上下文 | 关节坐标 |
| **Level 4** | 0次 | - | 关节坐标 | 验证结果 |
| **Level 5** | 0次 | - | 验证后的帧 | 优化后的帧 |

**总LLM调用次数**: 2 + N（N=关键帧数，本例为13）= **15次**

**总耗时**: ~56秒  
**平均每次LLM调用**: ~3.7秒

---

## 📋 配置参数汇总

```yaml
# LLM配置
llm:
  provider: perfxcloud
  model: Qwen3-Next-80B-Instruct
  temperature: 0.7
  max_tokens: 4096

# 上下文记忆
context_memory:
  window_size: 3  # 保留前3帧

# 验证器
validator:
  max_retries: 2
  tolerance:
    torso: 0.3
    arms: 0.5
    legs: 0.6

# 后处理
post_processor:
  interpolation_level: 2
  smoothing_factor: 0.3
  enable_physics: false
```

---

**文档版本**: v1.0  
**最后更新**: 2026-01-17  
**适用系统**: v0.5.0 (Refactored)

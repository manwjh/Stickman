# 🎮 骨骼系统快速上手

## 🚀 30秒体验

启动服务器后，输入以下故事：

```
两个武士持剑对峙，然后冲向对方，在中间交锋，最后一个获胜举剑庆祝
```

系统将自动生成：
- ✅ 2个角色，各持一把剑
- ✅ 对峙姿态（持剑戒备）
- ✅ 奔跑动作（身体前倾，腿部摆动）
- ✅ 挥剑动作（手臂旋转，身体扭转）
- ✅ 庆祝姿态（举剑高呼）

---

## 📝 示例1：单人武术表演

### 故事输入

```
一个人走到场地中央，从地上捡起一把武士刀，摆出起手式，
然后连续挥刀三次，最后收刀致敬
```

### LLM生成的JSON（简化版）

```json
{
  "title": "武士刀表演",
  "characters": [
    {"id": "char_1", "name": "武士", "color": "#E53935"}
  ],
  "props": [
    {"id": "katana_1", "type": "katana", "x": 400, "y": 500, "rotation": 90}
  ],
  "scenes": [
    {
      "id": "scene_1",
      "duration": 8000,
      "frames": [
        {
          "timestamp": 0,
          "text": "走到中央",
          "semantic_poses": {
            "char_1": {
              "body_lean": 5,
              "left_shoulder_angle": -30, "left_elbow_bend": 20,
              "right_shoulder_angle": 30, "right_elbow_bend": 20,
              "left_hip_angle": -30, "left_knee_bend": 30,
              "right_hip_angle": 20, "right_knee_bend": 10,
              "root_x": 200, "root_y": 380
            }
          }
        },
        {
          "timestamp": 1500,
          "text": "到达中央",
          "semantic_poses": {
            "char_1": {
              "body_lean": 0,
              "left_shoulder_angle": -20, "left_elbow_bend": 10,
              "right_shoulder_angle": 20, "right_elbow_bend": 10,
              "left_hip_angle": 0, "left_knee_bend": 5,
              "right_hip_angle": 0, "right_knee_bend": 5,
              "root_x": 400, "root_y": 380
            }
          }
        },
        {
          "timestamp": 2200,
          "text": "弯腰捡刀",
          "semantic_poses": {
            "char_1": {
              "body_lean": 40,
              "left_shoulder_angle": 10, "left_elbow_bend": 30,
              "right_shoulder_angle": 60, "right_elbow_bend": 80,
              "left_hip_angle": 50, "left_knee_bend": 60,
              "right_hip_angle": 30, "right_knee_bend": 40,
              "root_x": 400, "root_y": 420
            }
          },
          "prop_states": [
            {
              "prop_id": "katana_1",
              "attached_to_character": "char_1",
              "attached_to_joint": "right_hand",
              "rotation": 45
            }
          ]
        },
        {
          "timestamp": 3000,
          "text": "起手式",
          "semantic_poses": {
            "char_1": {
              "body_lean": 0,
              "left_shoulder_angle": -90, "left_elbow_bend": 100,
              "right_shoulder_angle": -100, "right_elbow_bend": 90,
              "left_hip_angle": 15, "left_knee_bend": 20,
              "right_hip_angle": -10, "right_knee_bend": 15,
              "root_x": 400, "root_y": 380
            }
          }
        },
        {
          "timestamp": 4000,
          "text": "第一刀",
          "semantic_poses": {
            "char_1": {
              "body_lean": 15, "body_twist": -30,
              "right_shoulder_angle": -45, "right_elbow_bend": 20,
              "left_shoulder_angle": -60, "left_elbow_bend": 90,
              "left_hip_angle": 20, "left_knee_bend": 25,
              "right_hip_angle": 10, "right_knee_bend": 20,
              "root_x": 380, "root_y": 385
            }
          }
        },
        {
          "timestamp": 4800,
          "text": "第二刀",
          "semantic_poses": {
            "char_1": {
              "body_lean": 20, "body_twist": 35,
              "right_shoulder_angle": 45, "right_elbow_bend": 30,
              "left_shoulder_angle": -70, "left_elbow_bend": 80,
              "left_hip_angle": -15, "left_knee_bend": 30,
              "right_hip_angle": 25, "right_knee_bend": 30,
              "root_x": 420, "root_y": 390
            }
          }
        },
        {
          "timestamp": 5600,
          "text": "第三刀",
          "semantic_poses": {
            "char_1": {
              "body_lean": 10, "body_twist": -25,
              "right_shoulder_angle": -120, "right_elbow_bend": 40,
              "left_shoulder_angle": -80, "left_elbow_bend": 100,
              "left_hip_angle": 10, "left_knee_bend": 20,
              "right_hip_angle": -5, "right_knee_bend": 15,
              "root_x": 400, "root_y": 370
            }
          }
        },
        {
          "timestamp": 7000,
          "text": "收刀致敬",
          "semantic_poses": {
            "char_1": {
              "body_lean": 25,
              "right_shoulder_angle": 80, "right_elbow_bend": 90,
              "left_shoulder_angle": 30, "left_elbow_bend": 20,
              "left_hip_angle": 5, "left_knee_bend": 15,
              "right_hip_angle": 5, "right_knee_bend": 15,
              "root_x": 400, "root_y": 400
            }
          }
        }
      ],
      "prop_interactions": [
        {
          "character_id": "char_1",
          "prop_id": "katana_1",
          "action": "grab",
          "joint_name": "right_hand",
          "timestamp": 2200,
          "duration": 500
        }
      ]
    }
  ]
}
```

---

## 🏀 示例2：篮球投篮

### 故事输入

```
一个人持球，向前助跑两步，然后起跳投篮，球飞向空中
```

### 关键帧设计

```json
{
  "props": [
    {"id": "ball_1", "type": "basketball", "x": 250, "y": 450}
  ],
  "frames": [
    {
      "timestamp": 0,
      "text": "持球准备",
      "semantic_poses": {
        "char_1": {
          "body_lean": 0,
          "left_shoulder_angle": -70, "left_elbow_bend": 90,
          "right_shoulder_angle": -70, "right_elbow_bend": 90,
          "root_x": 250, "root_y": 380
        }
      },
      "prop_states": [{
        "prop_id": "ball_1",
        "attached_to_character": "char_1",
        "attached_to_joint": "right_hand"
      }]
    },
    {
      "timestamp": 300,
      "text": "第一步",
      "semantic_poses": {
        "char_1": {
          "body_lean": 8,
          "left_shoulder_angle": -60, "left_elbow_bend": 85,
          "right_shoulder_angle": -60, "right_elbow_bend": 85,
          "left_hip_angle": -35, "left_knee_bend": 35,
          "right_hip_angle": 25, "right_knee_bend": 15,
          "root_x": 310, "root_y": 385
        }
      }
    },
    {
      "timestamp": 600,
      "text": "第二步",
      "semantic_poses": {
        "char_1": {
          "body_lean": 12,
          "left_shoulder_angle": -65, "left_elbow_bend": 80,
          "right_shoulder_angle": -65, "right_elbow_bend": 80,
          "left_hip_angle": 25, "left_knee_bend": 20,
          "right_hip_angle": -35, "right_knee_bend": 40,
          "root_x": 370, "root_y": 385
        }
      }
    },
    {
      "timestamp": 900,
      "text": "起跳",
      "semantic_poses": {
        "char_1": {
          "body_lean": -5,
          "left_shoulder_angle": -110, "left_elbow_bend": 50,
          "right_shoulder_angle": -110, "right_elbow_bend": 50,
          "left_hip_angle": -30, "left_knee_bend": 25,
          "right_hip_angle": -30, "right_knee_bend": 25,
          "root_x": 400, "root_y": 320
        }
      }
    },
    {
      "timestamp": 1200,
      "text": "出手",
      "semantic_poses": {
        "char_1": {
          "body_lean": -10,
          "left_shoulder_angle": -140, "left_elbow_bend": 20,
          "right_shoulder_angle": -140, "right_elbow_bend": 10,
          "left_hip_angle": -25, "left_knee_bend": 20,
          "right_hip_angle": -25, "right_knee_bend": 20,
          "root_x": 400, "root_y": 300
        }
      },
      "prop_states": [{
        "prop_id": "ball_1",
        "x": 450, "y": 150,
        "attached_to_character": null
      }]
    }
  ],
  "prop_interactions": [
    {
      "character_id": "char_1",
      "prop_id": "ball_1",
      "action": "grab",
      "joint_name": "right_hand",
      "timestamp": 0
    },
    {
      "character_id": "char_1",
      "prop_id": "ball_1",
      "action": "throw",
      "target_x": 450,
      "target_y": 150,
      "velocity": 400,
      "timestamp": 1200
    }
  ]
}
```

---

## ⚔️ 示例3：双人对决

### 故事输入

```
两个战士各持盾牌和剑，从两侧冲向对方，在中间碰撞，互相格挡
```

### 关键帧（char_1 视角）

```json
{
  "characters": [
    {"id": "char_1", "name": "红方", "color": "#E53935"},
    {"id": "char_2", "name": "蓝方", "color": "#1976D2"}
  ],
  "props": [
    {"id": "sword_1", "type": "sword", "x": 200, "y": 450},
    {"id": "shield_1", "type": "shield", "x": 180, "y": 450},
    {"id": "sword_2", "type": "sword", "x": 600, "y": 450},
    {"id": "shield_2", "type": "shield", "x": 620, "y": 450}
  ],
  "frames": [
    {
      "timestamp": 0,
      "text": "对峙",
      "semantic_poses": {
        "char_1": {
          "body_lean": 10,
          "left_shoulder_angle": -30, "left_elbow_bend": 70,
          "right_shoulder_angle": -60, "right_elbow_bend": 60,
          "left_hip_angle": 15, "left_knee_bend": 20,
          "right_hip_angle": -10, "right_knee_bend": 15,
          "root_x": 200, "root_y": 380
        },
        "char_2": {
          "body_lean": 10,
          "left_shoulder_angle": 60, "left_elbow_bend": 60,
          "right_shoulder_angle": 30, "right_elbow_bend": 70,
          "left_hip_angle": -15, "left_knee_bend": 20,
          "right_hip_angle": 10, "right_knee_bend": 15,
          "root_x": 600, "root_y": 380
        }
      },
      "prop_states": [
        {"prop_id": "sword_1", "attached_to_character": "char_1", "attached_to_joint": "right_hand"},
        {"prop_id": "shield_1", "attached_to_character": "char_1", "attached_to_joint": "left_hand"},
        {"prop_id": "sword_2", "attached_to_character": "char_2", "attached_to_joint": "left_hand"},
        {"prop_id": "shield_2", "attached_to_character": "char_2", "attached_to_joint": "right_hand"}
      ]
    },
    {
      "timestamp": 800,
      "text": "冲刺",
      "semantic_poses": {
        "char_1": {
          "body_lean": 25,
          "left_shoulder_angle": -20, "left_elbow_bend": 60,
          "right_shoulder_angle": -70, "right_elbow_bend": 50,
          "left_hip_angle": -40, "left_knee_bend": 45,
          "right_hip_angle": 30, "right_knee_bend": 20,
          "root_x": 320, "root_y": 385
        },
        "char_2": {
          "body_lean": 25,
          "left_shoulder_angle": 70, "left_elbow_bend": 50,
          "right_shoulder_angle": 20, "right_elbow_bend": 60,
          "left_hip_angle": 30, "left_knee_bend": 20,
          "right_hip_angle": -40, "right_knee_bend": 45,
          "root_x": 480, "root_y": 385
        }
      }
    },
    {
      "timestamp": 1400,
      "text": "碰撞！",
      "semantic_poses": {
        "char_1": {
          "body_lean": 20, "body_twist": -15,
          "left_shoulder_angle": -40, "left_elbow_bend": 80,
          "right_shoulder_angle": -30, "right_elbow_bend": 30,
          "left_hip_angle": 20, "left_knee_bend": 30,
          "right_hip_angle": 15, "right_knee_bend": 25,
          "root_x": 370, "root_y": 385
        },
        "char_2": {
          "body_lean": 20, "body_twist": 15,
          "left_shoulder_angle": 30, "left_elbow_bend": 30,
          "right_shoulder_angle": 40, "right_elbow_bend": 80,
          "left_hip_angle": 15, "left_knee_bend": 25,
          "right_hip_angle": 20, "right_knee_bend": 30,
          "root_x": 430, "root_y": 385
        }
      }
    }
  ]
}
```

---

## 💡 设计技巧

### 1. 身体前倾表达速度

```python
# 慢走
body_lean=2, root_y=380

# 快跑
body_lean=20, root_y=385  # 前倾+轻微起伏

# 冲刺
body_lean=35, root_y=390  # 大幅前倾
```

### 2. 手臂协调性

```python
# 行走：手臂与腿对称摆动
left_hip_angle=-30  →  right_shoulder_angle=30  # 左腿前→右臂前
right_hip_angle=20  →  left_shoulder_angle=-20  # 右腿后→左臂后
```

### 3. 重心控制

```python
# 单腿站立：身体偏向支撑腿
root_x=395  # 向右偏5像素（右腿支撑）
left_hip_angle=-80, left_knee_bend=100  # 左腿抬起

# 深蹲：重心下沉
root_y=450
left_hip_angle=90, left_knee_bend=120
right_hip_angle=90, right_knee_bend=120
```

### 4. 物品让动作更清晰

```python
# 模糊的"攻击动作"
right_shoulder_angle=-45, right_elbow_bend=20

# 清晰的"挥剑"（加上剑道具）
+ props: [{"type": "sword", "attached_to_joint": "right_hand"}]
→ 观众立刻理解这是在挥剑
```

---

## 🎯 调试技巧

### 查看生成的JSON

打开浏览器控制台（F12），生成动画时会显示：

```
Animation format: skeleton
```

### 检查姿态合理性

如果动作看起来奇怪：

1. **检查角度范围**
   - shoulder_angle: -180 ~ 180
   - elbow_bend: 0 ~ 180
   - hip_angle: -90 ~ 135
   - knee_bend: 0 ~ 150

2. **检查root_y**
   - 站立：380
   - 跳跃：250-320
   - 蹲下：420-470

3. **检查身体协调性**
   - 前倾时腿部应弯曲支撑
   - 挥臂时身体应有相应扭转

---

## 📚 进一步学习

- **完整文档**: `docs/SKELETON_UPGRADE.md`
- **API参考**: `docs/en/API.md`
- **代码示例**: `backend/skeleton.py` 中的 `POSE_REFERENCES`

---

**现在开始创作您的火柴人动画吧！** 🎬✨

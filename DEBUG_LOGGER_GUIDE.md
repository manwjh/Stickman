# 调试数据保存功能使用指南

## 功能说明

Pipeline各阶段的中间数据会自动保存到 `debug_logs/` 目录下，方便排查问题。

## 配置

在 `config.yml` 中配置：

```yaml
debug:
  save_process_data: true  # 启用/禁用调试数据保存
  process_data_dir: "debug_logs"  # 保存目录
  keep_last_n_sessions: 10  # 保留最近N个会话（0=全部保留）
```

## 保存的数据文件

每次生成动画会创建一个会话目录：`debug_logs/YYYYMMDD_HHMMSS_mmm/`

### 主要文件

1. **00_session_metadata.json** - 会话元信息
   - 会话ID、时间戳
   - 用户输入的故事
   - DOF级别

2. **01_story_plan.json** - Level 1: Story Planning
   - 角色列表
   - 动作序列
   - 场景规划

3. **02_choreography.json** - Level 2: Choreography
   - 关键帧描述列表
   - 时间轴信息
   - 角色分配

4. **03_animation_raw.json** - Level 3: Animation Generation
   - 原始关键帧坐标数据
   - 各角色姿势
   - 关节位置（x, y）
   - **自动生成 `keyframe_svgs/` 目录，包含每个关键帧的SVG文件**

5. **04_validation_report.json** - Level 4: Validation
   - 验证结果（通过/失败）
   - 错误详情
   - 约束检查报告

6. **05_post_processed.json** - Level 5: Post-processing
   - 优化后的动画数据
   - 插值后的帧数
   - 平滑处理结果

7. **06_final_output.json** - 最终输出
   - 标准化的16关节数据
   - 元数据统计

8. **99_error.json** - 错误日志（如果出错）
   - 错误类型
   - 错误消息
   - 发生阶段

### 关键帧SVG可视化

生成动画数据后，会在 `keyframe_svgs/` 子目录下自动生成每个关键帧的SVG文件：

- `keyframe_000.svg` - 第0帧的可视化
- `keyframe_001.svg` - 第1帧的可视化
- `keyframe_002.svg` - 第2帧的可视化
- ...

**特点**：
- 完整渲染火柴人骨骼结构（支持6DOF/12DOF）
- 包含旁白文字
- 包含地面线和画布背景
- 可直接在浏览器中打开查看
- 方便对比每一帧的姿势变化

### 重试记录

如果关键帧生成失败并重试，会在 `retries/` 子目录下保存：

- `retry_kf000_attempt1.json` - 第0帧第1次重试
- `retry_kf000_attempt2.json` - 第0帧第2次重试
- ...

## 使用示例

### 1. 查看最近一次生成的数据

```bash
cd debug_logs
ls -lt | head -2  # 查看最新目录
cd 20260118_153000_123  # 进入会话目录
```

### 2. 检查故事规划

```bash
cat 01_story_plan.json | python -m json.tool
```

### 3. 查看关键帧生成结果

```bash
# 查看JSON数据
cat 03_animation_raw.json | python -m json.tool | less

# 在浏览器中查看SVG可视化
open keyframe_svgs/keyframe_000.svg  # macOS
# 或
xdg-open keyframe_svgs/keyframe_000.svg  # Linux
# 或直接拖入浏览器
```

### 4. 检查验证报告

```bash
cat 04_validation_report.json | python -m json.tool
```

### 5. 对比优化前后的数据

```bash
# 原始数据
jq '.keyframe_count' 03_animation_raw.json

# 优化后
jq '.frame_count' 05_post_processed.json
```

## 常见排查场景

### 场景1：动画效果不符合预期

1. 查看 `01_story_plan.json` - 确认故事理解是否正确
2. 查看 `02_choreography.json` - 检查关键帧描述是否合理
3. **打开 `keyframe_svgs/` 目录中的SVG文件 - 直观查看每一帧的姿势**
4. 查看 `03_animation_raw.json` - 检查坐标数据

### 场景2：验证失败

1. 查看 `04_validation_report.json` - 查看具体的验证错误
2. 检查 `retries/` 目录 - 查看重试历史
3. 对比失败的帧与成功的帧

### 场景3：性能问题

1. 查看 `00_session_metadata.json` - 记录开始时间
2. 查看 `06_final_output.json` - 记录结束时间和统计信息
3. 计算各阶段耗时

### 场景4：LLM输出异常

1. 查看各级输出文件的原始数据
2. 检查JSON格式是否正确
3. 查看错误日志 `99_error.json`

## API响应中的调试信息

生成成功后，API响应的 `metadata` 中会包含：

```json
{
  "success": true,
  "data": {...},
  "metadata": {
    "debug_session_id": "20260118_153000_123",
    ...
  }
}
```

使用 `debug_session_id` 可以快速定位对应的调试文件目录。

## 注意事项

1. **磁盘空间**：每个会话约占用 100KB-1MB（包含SVG文件后约2-5MB），定期清理旧数据
2. **性能影响**：写入文件有轻微性能开销（约10-50ms）
3. **敏感信息**：调试文件中包含用户输入的故事内容
4. **Git忽略**：`debug_logs/` 目录已在 `.gitignore` 中忽略
5. **SVG文件**：每个关键帧生成约2-5KB的SVG文件，可在任何现代浏览器中直接打开

## 禁用调试日志

如果不需要调试数据，在 `config.yml` 中设置：

```yaml
debug:
  save_process_data: false
```

## 清理旧数据

```bash
# 清理7天前的数据
find debug_logs -type d -mtime +7 -exec rm -rf {} +

# 只保留最近10个会话
ls -t debug_logs | tail -n +11 | xargs -I {} rm -rf debug_logs/{}
```

## 数据结构示例

### 03_animation_raw.json 结构

```json
{
  "level": 3,
  "stage": "Animation Generation (Raw)",
  "timestamp": "2026-01-18T15:33:08.035000",
  "keyframe_count": 15,
  "animation_data": {
    "characters": [
      {
        "id": "char1",
        "name": "武术大师",
        "color": "#2196F3"
      }
    ],
    "keyframes": [
      {
        "timestamp_ms": 0,
        "description": "起势 - 双脚并拢站立",
        "character_ids": ["char1"],
        "poses": {
          "char1": {
            "head": {"x": 400, "y": 100},
            "torso": {"x": 400, "y": 200},
            "left_shoulder": {"x": 360, "y": 200},
            ...
          }
        }
      },
      ...
    ],
    "dof_level": "12dof"
  }
}
```

## 技术细节

- 实现位置：`backend/utils/debug_logger.py`
- 集成位置：`backend/services/animation_pipeline.py`
- 文件格式：UTF-8 编码的 JSON，使用2空格缩进
- 命名规则：按执行顺序编号（00-06），错误日志为99

---

**提示**：如果遇到问题无法解决，可以将整个会话目录打包发送给技术支持分析。

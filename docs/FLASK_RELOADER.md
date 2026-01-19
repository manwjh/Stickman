# Flask Reloader 优化说明

## 问题背景

在 Flask debug 模式下，应用会初始化**两次**：

```
第一次初始化 (监控进程)
  ↓
启动 Reloader
  ↓
第二次初始化 (工作进程) ← 实际处理请求的进程
```

这导致：
- ❌ LLM Client 初始化两次
- ❌ Pipeline 初始化两次（耗时、浪费资源）
- ❌ 启动时间加倍

## 解决方案

使用 `WERKZEUG_RUN_MAIN` 环境变量判断当前进程类型：

```python
# 只在工作进程或生产环境中初始化
should_initialize = os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or \
                   os.environ.get('WERKZEUG_RUN_MAIN') is None

if should_initialize:
    # 初始化 pipelines...
else:
    # 跳过初始化（reloader 监控进程）
```

## 环境变量说明

| 环境 | WERKZEUG_RUN_MAIN | 说明 | 是否初始化 |
|------|-------------------|------|-----------|
| **生产模式** | `None` (未设置) | 只有一个进程，直接运行 | ✅ 是 |
| **开发模式 - Reloader进程** | `""` (空字符串) | 监控文件变化 | ❌ 否 |
| **开发模式 - Worker进程** | `"true"` | 实际处理请求 | ✅ 是 |

## 效果对比

### 修复前：
```
2026-01-18 15:24:50,046 - Initializing 5-level pipeline system...
2026-01-18 15:24:50,047 - ✅ Pipelines initialized
...
* Restarting with stat
2026-01-18 15:24:53,979 - Initializing 5-level pipeline system...  ← 重复！
2026-01-18 15:24:53,979 - ✅ Pipelines initialized
```

### 修复后：
```
⏭️  Skipping initialization in reloader monitor process
...
* Restarting with stat
2026-01-18 15:30:00,123 - Initializing 5-level pipeline system...
2026-01-18 15:30:00,124 - ✅ Pipelines initialized  ← 只初始化一次！
```

## 优势

1. **开发环境优雅**：避免不必要的重复初始化
2. **生产环境兼容**：逻辑自动适配，无需修改
3. **启动更快**：节省一半初始化时间
4. **资源节省**：避免创建重复的 LLM Client 和 Pipeline 实例

## 参考资料

- [Flask Documentation - Reloader](https://flask.palletsprojects.com/en/2.3.x/cli/#watch-files-with-the-reloader)
- [Werkzeug Reloader Source Code](https://github.com/pallets/werkzeug/blob/main/src/werkzeug/_reloader.py)

---

**Author**: Shenzhen Wang & AI  
**Date**: 2026-01-18

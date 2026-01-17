# 🔒 安全指南

## ✅ 安全检查完成

已完成全面的安全检查和配置，确保所有敏感信息不会泄露到 GitHub。

---

## 🛡️ 已处理的安全问题

### 1. API 密钥清理
**发现问题**：
- ❌ `llm_config.yml` - 包含真实的 PerfXCloud API 密钥
- ❌ `docs/reports/CALL_FLOW.md` - 文档中包含真实密钥
- ❌ `docs/reports/PERFXCLOUD_VERIFICATION.md` - 文档中包含真实密钥

**处理结果**：
- ✅ 所有真实密钥已替换为占位符
- ✅ `llm_config.yml` 已在 `.gitignore` 中排除
- ✅ 文档中使用示例占位符

### 2. Git 安全配置
**`.gitignore` 已配置以下规则**：

#### 敏感信息（最重要）
```
llm_config.yml    # 包含真实 API 密钥
.env, .env.*      # 环境变量文件
*.key, *.pem      # 密钥和证书文件
*.p12, *.pfx      # 证书文件
secrets/          # 密钥目录
credentials/      # 凭证目录
```

#### 日志文件（可能包含敏感信息）
```
*.log, logs/      # 所有日志文件
```

#### 数据库文件
```
*.db, *.sqlite, *.sqlite3
```

#### 其他
- Python 虚拟环境：`venv/`, `env/`, `.venv`
- 缓存文件：`__pycache__/`, `*.pyc`
- IDE 配置：`.vscode/`, `.idea/`
- 临时文件：`*.tmp`, `*.bak`

---

## 📋 验证结果

### Git 状态
```
✅ 仓库地址：https://github.com/manwjh/Stickman
✅ 分支：main
✅ llm_config.yml 已被正确排除
✅ 32 个文件已成功上传
✅ 0 个敏感文件泄露
```

### 上传的文件清单
- ✅ 源代码文件（`.py`, `.js`, `.css`, `.html`）
- ✅ 配置示例文件（`llm_config.example.yml`, `config.yml`）
- ✅ 文档文件（`docs/`, `README.md`）
- ✅ 项目配置（`requirements.txt`, `.gitignore`）
- ❌ `llm_config.yml`（敏感文件，已排除）

---

## 🔐 使用说明

### 对于项目维护者（您）

1. **本地配置**
   - 保持本地的 `llm_config.yml` 文件不变
   - 该文件包含您的真实 API 密钥
   - 绝不将此文件提交到 Git

2. **更新代码**
   ```bash
   # 正常 git 操作，敏感文件会自动被排除
   git add .
   git commit -m "你的提交信息"
   git push
   ```

3. **添加新的 API 密钥**
   - 仅在本地 `llm_config.yml` 中添加
   - 同时更新 `llm_config.example.yml` 的结构（使用占位符）

### 对于其他开发者

1. **克隆项目**
   ```bash
   git clone https://github.com/manwjh/Stickman.git
   cd Stickman
   ```

2. **配置 API 密钥**
   ```bash
   # 复制示例配置
   cp llm_config.example.yml llm_config.yml
   
   # 编辑并填入您的 API 密钥
   nano llm_config.yml
   ```

3. **安装依赖**
   ```bash
   python install.py
   # 或
   ./install.py
   ```

4. **运行项目**
   ```bash
   python app.py
   # 或
   ./start.sh
   ```

---

## ⚠️ 重要提醒

### 绝对不要做的事
- ❌ 不要将 `llm_config.yml` 提交到 Git
- ❌ 不要在代码注释中写入真实密钥
- ❌ 不要在日志中输出完整的 API 密钥
- ❌ 不要在截图/文档中展示真实密钥
- ❌ 不要通过聊天工具发送完整密钥

### 推荐做法
- ✅ 使用环境变量存储敏感信息
- ✅ 使用配置文件模板（`.example`）
- ✅ 在文档中使用占位符（`your-api-key-here`）
- ✅ 定期轮换 API 密钥
- ✅ 为不同环境使用不同的密钥

---

## 🔍 定期检查

运行以下命令检查是否有敏感信息泄露：

```bash
# 检查是否有 API 密钥模式
grep -r "sk-[a-zA-Z0-9]\{20,\}" --exclude-dir=.git --exclude-dir=venv .

# 检查 git 跟踪的文件
git ls-files | grep -E "(secret|token|key|password|credential)"

# 检查 llm_config.yml 是否被排除
git status --ignored | grep llm_config.yml
```

---

## 📞 安全事件响应

如果不小心提交了敏感信息：

1. **立即撤销密钥**
   - 登录相应的服务提供商
   - 立即删除或重新生成 API 密钥

2. **清理 Git 历史**
   ```bash
   # 从所有提交中删除文件
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch llm_config.yml" \
     --prune-empty --tag-name-filter cat -- --all
   
   # 强制推送（谨慎操作）
   git push origin --force --all
   ```

3. **通知团队**
   - 通知所有相关人员
   - 更新所有使用该密钥的配置

---

## ✨ 安全配置总结

| 项目 | 状态 | 说明 |
|------|------|------|
| API 密钥保护 | ✅ 已完成 | 已从所有公开文件中清除 |
| .gitignore 配置 | ✅ 已完成 | 完善的排除规则 |
| 配置文件示例 | ✅ 已完成 | 提供 `llm_config.example.yml` |
| 文档安全性 | ✅ 已完成 | 所有文档使用占位符 |
| Git 仓库验证 | ✅ 已完成 | 无敏感信息泄露 |

---

**项目已成功上传到 GitHub：https://github.com/manwjh/Stickman**

所有敏感信息已被妥善保护！🎉

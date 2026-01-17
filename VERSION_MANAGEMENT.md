# Version Management / 版本管理

## Current Version / 当前版本

**v0.1.0** (2026-01-17)

## Versioning System / 版本系统

This project follows [Semantic Versioning 2.0.0](https://semver.org/) / 本项目遵循[语义化版本 2.0.0](https://semver.org/lang/zh-CN/)

### Format / 格式

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Incompatible API changes / 不兼容的 API 更改
- **MINOR**: Backward-compatible new features / 向后兼容的新功能
- **PATCH**: Backward-compatible bug fixes / 向后兼容的 Bug 修复

### Examples / 示例

- `0.1.0` → `0.1.1` - Bug fix / Bug 修复
- `0.1.0` → `0.2.0` - New feature / 新功能
- `0.1.0` → `1.0.0` - Breaking change / 破坏性更改

## Version Files / 版本文件

### VERSION
Contains the current version number / 包含当前版本号

```
v0.1.0
```

### CHANGELOG.md / CHANGELOG.zh-CN.md
Complete change history / 完整的更改历史

- [CHANGELOG.md](CHANGELOG.md) - English
- [CHANGELOG.zh-CN.md](CHANGELOG.zh-CN.md) - 中文

## Checking Version / 查看版本

### Command Line / 命令行

```bash
# Read VERSION file
cat VERSION

# Or run the app and check startup output
python app.py
```

### API Endpoint / API 端点

```bash
# Get version via API
curl http://localhost:5001/api/version
```

Response / 响应:
```json
{
  "version": "0.1.0",
  "name": "AI Stick Figure Story Animator",
  "author": "Shenzhen Wang & AI",
  "license": "MIT"
}
```

### Web Interface / Web 界面

Version is displayed in the footer / 版本号显示在页面底部

## Release Process / 发布流程

### 1. Update Version / 更新版本

Edit `VERSION` file / 编辑 `VERSION` 文件:
```bash
echo "v0.2.0" > VERSION
```

### 2. Update CHANGELOG / 更新变更日志

Add changes to `CHANGELOG.md` and `CHANGELOG.zh-CN.md`:

```markdown
## [0.2.0] - 2026-XX-XX

### ✨ Added
- New feature description

### 🐛 Fixed
- Bug fix description
```

### 3. Update Code Version / 更新代码版本

Update `__version__` in `app.py`:
```python
__version__ = "0.2.0"
```

### 4. Commit Changes / 提交更改

```bash
git add VERSION CHANGELOG.md CHANGELOG.zh-CN.md app.py
git commit -m "chore: bump version to v0.2.0"
```

### 5. Create Git Tag / 创建 Git 标签

```bash
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

### 6. Create GitHub Release / 创建 GitHub Release

Go to GitHub repository → Releases → Create new release
前往 GitHub 仓库 → Releases → 创建新发布

- Tag: `v0.2.0`
- Title: `v0.2.0 - Release Title`
- Description: Copy from CHANGELOG / 从 CHANGELOG 复制

## Version History / 版本历史

| Version | Date | Description |
|---------|------|-------------|
| [0.1.0](https://github.com/your-repo/releases/tag/v0.1.0) | 2026-01-17 | Initial release / 首次发布 |

## Automation / 自动化

For future improvement, consider using:
未来可以考虑使用：

- **bump2version** - Automated version bumping / 自动版本号递增
- **semantic-release** - Automated changelog and releases / 自动化变更日志和发布
- **GitHub Actions** - CI/CD for releases / 发布的 CI/CD

## Questions? / 有问题？

- See [CHANGELOG.md](CHANGELOG.md) for detailed change history
- Check [GitHub Releases](https://github.com/your-repo/releases) for downloads
- Create an [issue](https://github.com/your-repo/issues) if you find problems

---

**Current Version**: v0.1.0  
**Last Updated**: 2026-01-17

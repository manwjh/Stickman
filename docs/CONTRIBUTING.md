# Contributing to AI Stick Figure Story Animator

[中文](CONTRIBUTING.zh-CN.md) | English

Thank you for your interest in contributing to this project! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [issue list](https://github.com/your-repo/issues) to avoid duplicates.

When reporting a bug, please include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Clear title and description**
- **Use case** - why is this enhancement useful?
- **Proposed solution** if you have one
- **Alternative solutions** you've considered

### Contributing Code

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding guidelines
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Git

### Setup Steps

```bash
# 1. Fork and clone the repository
git clone https://github.com/your-username/stickman.git
cd stickman

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy configuration file
cp llm_config.example.yml llm_config.yml

# 5. Edit llm_config.yml and add your API key

# 6. Run the application
python app.py
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=backend tests/
```

## Coding Guidelines

### Python Code

- **Follow PEP 8** style guide
- **Use type hints** where applicable
- **Write docstrings** for all functions and classes
- **Keep functions small** and focused on a single task
- **Use meaningful variable names** in English

Example:

```python
def generate_animation(story: str) -> Dict[str, Any]:
    """
    Generate animation from story description
    
    Args:
        story: Natural language story description
        
    Returns:
        Dict containing animation data with scenes and frames
        
    Raises:
        ValueError: If story is empty or invalid
    """
    # Implementation here
    pass
```

### JavaScript Code

- **Use ES6+ features** where appropriate
- **Add JSDoc comments** for functions
- **Use meaningful variable names** in English
- **Follow consistent indentation** (4 spaces)

Example:

```javascript
/**
 * Generate animation from story
 * @param {string} story - User's story description
 * @returns {Promise<Object>} Animation data
 */
async function generateAnimation(story) {
    // Implementation here
}
```

### Code Comments

- **All code comments must be in English**
- **Explain "why", not "what"** - the code shows what it does
- **Keep comments up-to-date** with code changes
- **Use inline comments sparingly** - prefer clear code

### Internationalization

- **All user-facing text** must be internationalized
- **Add translations** to `static/js/i18n.js` for both English and Chinese
- **Use i18n keys** instead of hardcoded strings in templates and JavaScript

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Build process or auxiliary tool changes

### Examples

```
feat(animation): add support for multi-character scenes

- Implement character coordination
- Add collision detection
- Update prompt template

Closes #123
```

```
fix(llm): handle timeout errors gracefully

Previously, timeout errors would crash the application.
Now they are caught and a user-friendly error is displayed.
```

## Pull Request Process

1. **Update documentation** if you changed functionality
2. **Add tests** for new features
3. **Ensure all tests pass** before submitting
4. **Update CHANGELOG.md** with your changes
5. **Link related issues** in the PR description

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages follow guidelines
- [ ] No merge conflicts
- [ ] Code has been self-reviewed

### Review Process

- Maintainers will review your PR within 3-5 business days
- Address any feedback or requested changes
- Once approved, a maintainer will merge your PR

## Questions?

Feel free to:

- Open an issue with the `question` label
- Email: manwjh@126.com
- Twitter: [@cpswang](https://twitter.com/cpswang)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AI Stick Figure Story Animator! 🎬✨

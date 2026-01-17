#!/usr/bin/env python3
"""
测试脚本 - 验证项目配置和依赖
"""
import sys
import os

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python版本过低，需要 3.9+")
        print(f"   当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """检查依赖包"""
    required = ['flask', 'openai', 'anthropic', 'pydantic', 'flask_cors', 'dotenv']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing.append(package)
    
    return len(missing) == 0

def check_env_file():
    """检查环境变量文件"""
    if not os.path.exists('.env'):
        print("❌ .env 文件不存在")
        print("   请运行: cp .env.example .env")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        
    if 'your_' in content or 'your-' in content:
        print("⚠️  .env 文件存在但可能未配置API密钥")
        return False
    
    print("✅ .env 文件已配置")
    return True

def check_project_structure():
    """检查项目结构"""
    required_files = [
        'app.py',
        'requirements.txt',
        'backend/__init__.py',
        'backend/llm_service.py',
        'backend/prompt_template.py',
        'backend/animation_validator.py',
        'templates/index.html',
        'static/css/style.css',
        'static/js/animator.js',
        'static/js/app.js',
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 缺失")
            all_exist = False
    
    return all_exist

def main():
    """主函数"""
    print("=" * 60)
    print("🔍 项目环境检查")
    print("=" * 60)
    print()
    
    print("1️⃣  检查Python版本...")
    python_ok = check_python_version()
    print()
    
    print("2️⃣  检查项目结构...")
    structure_ok = check_project_structure()
    print()
    
    print("3️⃣  检查依赖包...")
    deps_ok = check_dependencies()
    print()
    
    print("4️⃣  检查环境配置...")
    env_ok = check_env_file()
    print()
    
    print("=" * 60)
    if python_ok and structure_ok and deps_ok and env_ok:
        print("✅ 所有检查通过！项目已就绪")
        print()
        print("运行以下命令启动服务器:")
        print("  python app.py")
    else:
        print("❌ 部分检查失败，请修复上述问题")
        if not deps_ok:
            print()
            print("安装依赖:")
            print("  pip install -r requirements.txt")
        if not env_ok:
            print()
            print("配置环境:")
            print("  cp .env.example .env")
            print("  # 然后编辑 .env 文件添加API密钥")
    print("=" * 60)

if __name__ == '__main__':
    main()

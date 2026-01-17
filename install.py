#!/usr/bin/env python3
"""
一键安装和启动脚本
"""
import os
import sys
import subprocess
import platform

def run_command(cmd, description):
    """运行命令并显示进度"""
    print(f"📦 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"   ✅ 完成")
        return True
    else:
        print(f"   ❌ 失败: {result.stderr}")
        return False

def main():
    print("=" * 60)
    print("🎬 AI火柴人故事动画生成器 - 一键安装")
    print("=" * 60)
    print()
    
    # 检查Python版本
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("   需要 Python 3.9+")
        return
    
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    print()
    
    # 检查虚拟环境
    if not os.path.exists('venv'):
        print("1️⃣  创建虚拟环境...")
        if not run_command(f"{sys.executable} -m venv venv", "创建虚拟环境"):
            return
    else:
        print("✅ 虚拟环境已存在")
    
    print()
    
    # 确定pip路径
    is_windows = platform.system() == 'Windows'
    if is_windows:
        pip_path = os.path.join('venv', 'Scripts', 'pip')
        python_path = os.path.join('venv', 'Scripts', 'python')
    else:
        pip_path = os.path.join('venv', 'bin', 'pip')
        python_path = os.path.join('venv', 'bin', 'python')
    
    # 安装依赖
    print("2️⃣  安装依赖包...")
    if not run_command(f"{pip_path} install -r requirements.txt", "安装依赖"):
        return
    
    print()
    
    # 检查llm_config.yml文件
    if not os.path.exists('llm_config.yml'):
        print("3️⃣  配置LLM...")
        if os.path.exists('llm_config.example.yml'):
            import shutil
            shutil.copy('llm_config.example.yml', 'llm_config.yml')
            print("   ✅ 已创建 llm_config.yml 文件")
            print()
            print("⚠️  重要: 请编辑 llm_config.yml 文件并添加你的API密钥!")
            print("   - OpenAI API密钥: https://platform.openai.com/api-keys")
            print("   - 或 Anthropic API密钥: https://console.anthropic.com/")
            print()
            print("然后运行以下命令启动服务器:")
            if is_windows:
                print("   start.bat")
            else:
                print("   ./start.sh")
            return
    else:
        print("✅ llm_config.yml 文件已存在")
    
    print()
    print("=" * 60)
    print("✅ 安装完成!")
    print("=" * 60)
    print()
    print("启动服务器:")
    if is_windows:
        print("   start.bat")
    else:
        print("   ./start.sh")
    print()
    print("或直接运行:")
    print(f"   {python_path} app.py")
    print()

if __name__ == '__main__':
    main()

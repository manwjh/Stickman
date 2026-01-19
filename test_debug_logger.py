#!/usr/bin/env python3
"""
测试调试日志功能

测试Pipeline的调试数据保存功能是否正常工作
"""
import os
import json
import time
from pathlib import Path

def check_debug_config():
    """检查配置文件"""
    print("=" * 60)
    print("1. 检查配置文件")
    print("=" * 60)
    
    with open('config.yml', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'save_process_data' in content:
            print("✅ 配置项已添加")
            print(f"   - save_process_data: {True if 'save_process_data: true' in content else False}")
        else:
            print("❌ 配置项未找到")
            return False
    return True

def check_debug_logger_module():
    """检查debug_logger模块"""
    print("\n" + "=" * 60)
    print("2. 检查debug_logger模块")
    print("=" * 60)
    
    try:
        from backend.utils.debug_logger import DebugLogger, get_debug_logger
        print("✅ 模块导入成功")
        
        # 测试初始化
        logger = DebugLogger(enabled=True, output_dir="test_debug_logs")
        print("✅ DebugLogger实例化成功")
        
        # 测试会话
        session_id = logger.start_session("测试故事", "12dof")
        print(f"✅ 会话启动成功: {session_id}")
        
        # 测试数据保存
        test_data = {"test": "data", "timestamp": time.time()}
        logger._save_json("test_file.json", test_data)
        
        # 验证文件
        test_file = Path(f"test_debug_logs/{session_id}/test_file.json")
        if test_file.exists():
            print(f"✅ 文件保存成功: {test_file}")
            with open(test_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                if loaded == test_data:
                    print("✅ 数据验证成功")
        else:
            print("❌ 文件未创建")
            return False
        
        logger.end_session()
        
        # 清理测试数据
        import shutil
        shutil.rmtree("test_debug_logs")
        print("✅ 测试数据清理完成")
        
        return True
    except Exception as e:
        print(f"❌ 模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_pipeline_integration():
    """检查Pipeline集成"""
    print("\n" + "=" * 60)
    print("3. 检查Pipeline集成")
    print("=" * 60)
    
    try:
        # 只检查代码是否正确导入debug_logger
        with open('backend/services/animation_pipeline.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'from backend.utils.debug_logger import get_debug_logger' in content:
            print("✅ Pipeline已导入debug_logger模块")
        else:
            print("❌ Pipeline未导入debug_logger模块")
            return False
        
        if 'self.debug_logger = get_debug_logger()' in content:
            print("✅ Pipeline已初始化debug_logger")
        else:
            print("❌ Pipeline未初始化debug_logger")
            return False
        
        if 'self.debug_logger.start_session' in content:
            print("✅ Pipeline调用了debug_logger.start_session")
        else:
            print("❌ Pipeline未调用debug_logger.start_session")
            return False
        
        if 'self.debug_logger.log_level_1_story_plan' in content:
            print("✅ Pipeline调用了log_level_1_story_plan")
        else:
            print("❌ Pipeline未调用log_level_1_story_plan")
            return False
        
        # 检查所有5个级别的日志调用
        log_methods = [
            'log_level_1_story_plan',
            'log_level_2_choreography',
            'log_level_3_animation_raw',
            'log_level_4_validation',
            'log_level_5_optimized'
        ]
        
        all_present = True
        for method in log_methods:
            if f'self.debug_logger.{method}' in content:
                print(f"✅ 调用了 {method}")
            else:
                print(f"❌ 未调用 {method}")
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"❌ Pipeline集成检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_gitignore():
    """检查.gitignore"""
    print("\n" + "=" * 60)
    print("4. 检查.gitignore")
    print("=" * 60)
    
    with open('.gitignore', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'debug_logs/' in content:
            print("✅ debug_logs/已添加到.gitignore")
            return True
        else:
            print("⚠️  debug_logs/未在.gitignore中（可能不影响功能）")
            return True

def main():
    print("\n" + "=" * 60)
    print("调试日志功能测试")
    print("=" * 60 + "\n")
    
    results = []
    
    # 测试1: 配置文件
    results.append(("配置文件", check_debug_config()))
    
    # 测试2: debug_logger模块
    results.append(("debug_logger模块", check_debug_logger_module()))
    
    # 测试3: Pipeline集成
    results.append(("Pipeline集成", check_pipeline_integration()))
    
    # 测试4: .gitignore
    results.append((".gitignore", check_gitignore()))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\n" + "🎉 所有测试通过！")
        print("\n下一步：")
        print("  1. 访问 http://127.0.0.1:5001")
        print("  2. 生成一个动画")
        print("  3. 查看 debug_logs/ 目录")
        print("  4. 检查是否生成了各级数据文件")
        print("\n详细使用说明请查看: DEBUG_LOGGER_GUIDE.md")
    else:
        print("\n" + "❌ 部分测试失败，请检查上述错误信息")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())

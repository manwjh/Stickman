#!/usr/bin/env python3
"""
动画生成重构验证测试

测试改进后的动画生成流程：
1. LLM响应解析能力
2. 错误处理和重试机制
3. Fallback策略
4. 响应缓存功能

Usage:
    python test_refactored_animation.py
"""
import sys
import os
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.services.llm_response_parser import LLMResponseParser, ResponseCache
from backend.services.animation_pipeline import AnimationPipeline


def test_response_parser():
    """测试响应解析器"""
    print("\n" + "="*80)
    print("测试 1: LLM响应解析器")
    print("="*80)
    
    parser = LLMResponseParser(dof_level='12dof')
    
    # 测试用例1: 标准格式
    test_case_1 = """
    {
        "keyframes": [{
            "timestamp_ms": 0,
            "characters": {
                "char1": {
                    "joints": {
                        "head": {"x": 400, "y": 240},
                        "neck": {"x": 400, "y": 260}
                    }
                }
            }
        }]
    }
    """
    
    print("\n[测试用例 1] 标准格式")
    data, error = parser.parse_response(test_case_1, 'openai')
    if error:
        print(f"  ❌ 失败: {error}")
        return False
    else:
        print(f"  ✅ 成功解析")
        print(f"  数据: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
    
    # 测试用例2: 带Markdown包裹
    test_case_2 = """
    ```json
    {
        "keyframes": [{
            "timestamp_ms": 0,
            "characters": {
                "char1": {
                    "dof": 12,
                    "joints": {
                        "head": {"x": 400, "y": 240}
                    }
                }
            }
        }]
    }
    ```
    """
    
    print("\n[测试用例 2] Markdown包裹格式")
    data, error = parser.parse_response(test_case_2, 'anthropic')
    if error:
        print(f"  ❌ 失败: {error}")
        return False
    else:
        print(f"  ✅ 成功解析（已去除Markdown）")
    
    # 测试用例3: 直接关节数据（无包裹）
    test_case_3 = """
    {
        "keyframes": [{
            "timestamp_ms": 0,
            "characters": {
                "char1": {
                    "head": {"x": 400, "y": 240},
                    "neck": {"x": 400, "y": 260},
                    "waist": {"x": 400, "y": 300}
                }
            }
        }]
    }
    """
    
    print("\n[测试用例 3] 直接关节数据（无joints包裹）")
    data, error = parser.parse_response(test_case_3, 'openai')
    if error:
        print(f"  ❌ 失败: {error}")
        return False
    else:
        print(f"  ✅ 成功解析（自动修正格式）")
        # 验证是否已包裹
        char_data = data['characters']['char1']
        if 'joints' in char_data:
            print(f"  ✅ 已自动添加joints包裹层")
        else:
            print(f"  ❌ 未正确添加包裹层")
            return False
    
    # 测试用例4: 错误格式
    test_case_4 = """
    {
        "keyframes": [{
            "timestamp_ms": 0,
            "characters": {
                "char1": {
                    "wrong_field": "data"
                }
            }
        }]
    }
    """
    
    print("\n[测试用例 4] 错误格式（应该报错）")
    data, error = parser.parse_response(test_case_4, 'openai')
    if error:
        print(f"  ✅ 正确识别错误: {error[:100]}...")
    else:
        print(f"  ❌ 应该报错但没有报错")
        return False
    
    print("\n✅ 响应解析器测试通过")
    return True


def test_response_cache():
    """测试响应缓存"""
    print("\n" + "="*80)
    print("测试 2: 响应缓存")
    print("="*80)
    
    cache = ResponseCache(max_size=5)
    
    # 添加一些记录
    print("\n添加测试记录...")
    cache.add(0, "response_0", {"data": "ok"}, None, "prompt_0")
    cache.add(1, "response_1", None, "Parse error", "prompt_1")
    cache.add(2, "response_2", {"data": "ok"}, None, "prompt_2")
    cache.add(3, "response_3", None, "Validation error", "prompt_3")
    
    # 测试获取最近记录
    recent = cache.get_recent(3)
    print(f"\n最近3条记录: {len(recent)}条")
    if len(recent) != 3:
        print(f"  ❌ 期望3条，实际{len(recent)}条")
        return False
    print(f"  ✅ 正确")
    
    # 测试获取失败记录
    failed = cache.get_failed()
    print(f"\n失败记录: {len(failed)}条")
    if len(failed) != 2:
        print(f"  ❌ 期望2条失败记录，实际{len(failed)}条")
        return False
    print(f"  ✅ 正确")
    
    for f in failed:
        print(f"  - Keyframe {f['keyframe_index']}: {f['error']}")
    
    # 测试清空
    cache.clear()
    if len(cache.cache) != 0:
        print(f"  ❌ 清空后应该为0，实际{len(cache.cache)}")
        return False
    print(f"\n清空缓存: ✅")
    
    print("\n✅ 响应缓存测试通过")
    return True


def test_animation_generation():
    """测试完整的动画生成流程"""
    print("\n" + "="*80)
    print("测试 3: 完整动画生成流程")
    print("="*80)
    
    # 简单的测试故事
    story = "一个人走进来，挥手打招呼"
    
    print(f"\n故事: {story}")
    print("初始化Pipeline...")
    
    try:
        pipeline = AnimationPipeline(dof_level='12dof', enable_optimization=False)
        
        print("开始生成动画...\n")
        result = pipeline.generate(story, max_retries=2, enable_feedback_loop=True)
        
        if result["success"]:
            metadata = result["metadata"]
            print(f"\n✅ 生成成功!")
            print(f"  - 生成时间: {metadata['generation_time_ms']:.0f}ms")
            print(f"  - 关键帧数: {metadata['keyframes_generated']}")
            print(f"  - 验证通过: {metadata['validation_passed']}")
            print(f"  - 调试会话: {metadata['debug_session_id']}")
            
            # 检查是否有fallback
            keyframes = result["data"]["keyframes"]
            fallback_count = sum(1 for kf in keyframes if "fallback" in kf.get("description", "").lower())
            
            print(f"\n  - Fallback帧数: {fallback_count}/{len(keyframes)}")
            
            if fallback_count > len(keyframes) * 0.3:
                print(f"  ⚠️  Fallback比例较高({fallback_count/len(keyframes)*100:.1f}%)")
            else:
                print(f"  ✅ Fallback比例正常")
            
            # 查看失败的响应
            failed_responses = pipeline.animator.get_failed_responses()
            if failed_responses:
                print(f"\n  失败的LLM调用:")
                for resp in failed_responses:
                    print(f"    - Keyframe {resp['keyframe_index']}: {resp['error'][:80]}...")
            
            return True
        else:
            print(f"\n❌ 生成失败: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"\n❌ 异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "="*80)
    print("🔧 动画生成重构验证测试")
    print("="*80)
    
    results = []
    
    # 运行测试
    results.append(("响应解析器", test_response_parser()))
    results.append(("响应缓存", test_response_cache()))
    results.append(("动画生成流程", test_animation_generation()))
    
    # 汇总结果
    print("\n" + "="*80)
    print("📊 测试结果汇总")
    print("="*80)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n总计: {passed}/{total} 通过 ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！重构验证成功！")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查日志")
        return 1


if __name__ == "__main__":
    exit(main())

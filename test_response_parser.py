#!/usr/bin/env python3
"""
响应解析器单元测试（不依赖LLM）

专门测试LLMResponseParser的各种边界情况
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.services.llm_response_parser import LLMResponseParser


def test_12dof_formats():
    """测试12DOF的各种格式"""
    print("\n" + "="*80)
    print("测试 12DOF 响应格式处理")
    print("="*80)
    
    parser = LLMResponseParser(dof_level='12dof')
    
    test_cases = [
        {
            "name": "标准格式（带joints包裹）",
            "content": json.dumps({
                "keyframes": [{
                    "timestamp_ms": 0,
                    "characters": {
                        "char1": {
                            "joints": {
                                "head": {"x": 400, "y": 240},
                                "neck": {"x": 400, "y": 260},
                                "waist": {"x": 400, "y": 300}
                            }
                        }
                    }
                }]
            }),
            "should_pass": True
        },
        {
            "name": "带dof元数据的格式",
            "content": json.dumps({
                "keyframes": [{
                    "timestamp_ms": 0,
                    "characters": {
                        "char1": {
                            "dof": 12,
                            "joints": {
                                "head": {"x": 400, "y": 240},
                                "neck": {"x": 400, "y": 260}
                            }
                        }
                    }
                }]
            }),
            "should_pass": True
        },
        {
            "name": "直接关节数据（无joints包裹）",
            "content": json.dumps({
                "keyframes": [{
                    "timestamp_ms": 0,
                    "characters": {
                        "char1": {
                            "head": {"x": 400, "y": 240},
                            "neck": {"x": 400, "y": 260},
                            "waist": {"x": 400, "y": 300},
                            "left_shoulder": {"x": 380, "y": 270}
                        }
                    }
                }]
            }),
            "should_pass": True,
            "note": "应自动添加joints包裹"
        },
        {
            "name": "Markdown包裹的JSON",
            "content": "```json\n" + json.dumps({
                "keyframes": [{
                    "timestamp_ms": 0,
                    "characters": {
                        "char1": {
                            "joints": {"head": {"x": 400, "y": 240}}
                        }
                    }
                }]
            }) + "\n```",
            "should_pass": True,
            "note": "应去除Markdown包裹"
        },
        {
            "name": "缺少characters字段",
            "content": json.dumps({
                "keyframes": [{
                    "timestamp_ms": 0
                }]
            }),
            "should_pass": False
        },
        {
            "name": "错误的数据类型",
            "content": json.dumps({
                "keyframes": [{
                    "timestamp_ms": 0,
                    "characters": {
                        "char1": "wrong_type"
                    }
                }]
            }),
            "should_pass": False
        },
        {
            "name": "空的keyframes数组",
            "content": json.dumps({
                "keyframes": []
            }),
            "should_pass": False
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n[测试 {i}] {test['name']}")
        if 'note' in test:
            print(f"  说明: {test['note']}")
        
        data, error = parser.parse_response(test['content'], 'openai')
        
        if test['should_pass']:
            if error:
                print(f"  ❌ 失败: 期望成功但报错 - {error[:100]}")
                failed += 1
            else:
                print(f"  ✅ 通过")
                # 验证是否正确规范化
                if 'char1' in data.get('characters', {}):
                    char_data = data['characters']['char1']
                    if 'joints' in char_data:
                        print(f"      包含joints字段 ✓")
                    else:
                        print(f"      ⚠️ 缺少joints字段")
                passed += 1
        else:
            if error:
                print(f"  ✅ 通过: 正确识别错误 - {error[:80]}...")
                passed += 1
            else:
                print(f"  ❌ 失败: 期望报错但成功")
                failed += 1
    
    print(f"\n结果: {passed}/{len(test_cases)} 通过")
    return failed == 0


def test_6dof_formats():
    """测试6DOF的格式"""
    print("\n" + "="*80)
    print("测试 6DOF 响应格式处理")
    print("="*80)
    
    parser = LLMResponseParser(dof_level='6dof')
    
    test_cases = [
        {
            "name": "标准6DOF格式",
            "content": json.dumps({
                "keyframes": [{
                    "timestamp_ms": 0,
                    "characters": {
                        "char1": {
                            "pose": {
                                "head_x": 400,
                                "head_y": 240,
                                "body_angle": 0,
                                "left_arm_angle": 30,
                                "right_arm_angle": -30,
                                "left_leg_angle": 10,
                                "right_leg_angle": -10
                            }
                        }
                    }
                }]
            }),
            "should_pass": True
        },
        {
            "name": "直接姿态数据（无pose包裹）",
            "content": json.dumps({
                "keyframes": [{
                    "timestamp_ms": 0,
                    "characters": {
                        "char1": {
                            "head_x": 400,
                            "head_y": 240,
                            "body_angle": 0
                        }
                    }
                }]
            }),
            "should_pass": True,
            "note": "应自动添加pose包裹"
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n[测试 {i}] {test['name']}")
        if 'note' in test:
            print(f"  说明: {test['note']}")
        
        data, error = parser.parse_response(test['content'], 'openai')
        
        if test['should_pass']:
            if error:
                print(f"  ❌ 失败: {error[:100]}")
                failed += 1
            else:
                print(f"  ✅ 通过")
                if 'char1' in data.get('characters', {}):
                    char_data = data['characters']['char1']
                    if 'pose' in char_data:
                        print(f"      包含pose字段 ✓")
                passed += 1
        else:
            if error:
                print(f"  ✅ 通过: {error[:80]}...")
                passed += 1
            else:
                print(f"  ❌ 失败: 应报错")
                failed += 1
    
    print(f"\n结果: {passed}/{len(test_cases)} 通过")
    return failed == 0


def test_diagnostic_report():
    """测试诊断报告生成"""
    print("\n" + "="*80)
    print("测试 诊断报告生成")
    print("="*80)
    
    parser = LLMResponseParser(dof_level='12dof')
    
    raw_content = """{"invalid": "json" "missing_comma": true}"""
    error = "JSON解析失败: Expecting ',' delimiter"
    context = {
        "keyframe_index": 3,
        "description": "角色挥手打招呼"
    }
    
    report = parser.create_diagnostic_report(raw_content, error, context)
    
    print("\n生成的诊断报告:")
    print(report)
    
    # 验证报告内容
    checks = [
        ("包含DOF级别", "12dof" in report),
        ("包含错误信息", error in report),
        ("包含原始响应", "invalid" in report),
        ("包含上下文", "keyframe_index" in report)
    ]
    
    passed = sum(1 for _, check in checks if check)
    
    print(f"\n验证:")
    for name, check in checks:
        status = "✅" if check else "❌"
        print(f"  {status} {name}")
    
    print(f"\n结果: {passed}/{len(checks)} 项通过")
    return passed == len(checks)


def main():
    """主测试函数"""
    print("\n" + "="*80)
    print("🔬 LLM响应解析器单元测试")
    print("="*80)
    
    tests = [
        ("12DOF格式处理", test_12dof_formats),
        ("6DOF格式处理", test_6dof_formats),
        ("诊断报告生成", test_diagnostic_report)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ 测试异常: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 汇总
    print("\n" + "="*80)
    print("📊 测试结果汇总")
    print("="*80)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {name}")
    
    total = len(results)
    passed_count = sum(1 for _, p in results if p)
    
    print(f"\n总计: {passed_count}/{total} 通过 ({passed_count/total*100:.0f}%)")
    
    if passed_count == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print("\n⚠️  部分测试失败")
        return 1


if __name__ == "__main__":
    exit(main())

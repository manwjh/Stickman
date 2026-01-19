#!/usr/bin/env python3
"""
测试插值修复
验证关节位置的平滑过渡
"""
import json

def test_interpolation():
    """测试插值是否正确工作"""
    
    # 模拟两个关键帧
    kf1 = {
        "timestamp_ms": 0,
        "characters": {
            "char1": {
                "dof": 12,
                "joints": {
                    "head": {"x": 420, "y": 235},
                    "waist": {"x": 415, "y": 310}
                }
            }
        }
    }
    
    kf2 = {
        "timestamp_ms": 600,
        "characters": {
            "char1": {
                "dof": 12,
                "joints": {
                    "head": {"x": 340, "y": 240},
                    "waist": {"x": 338, "y": 315}
                }
            }
        }
    }
    
    # 模拟插值（t=0.33）
    t = 0.33
    
    # 提取joints
    char1_kf1 = kf1["characters"]["char1"]["joints"]
    char1_kf2 = kf2["characters"]["char1"]["joints"]
    
    # 计算预期的插值
    expected_head_x = 420 + (340 - 420) * t  # 420 + (-80) * 0.33 = 393.6
    expected_head_y = 235 + (240 - 235) * t  # 235 + 5 * 0.33 = 236.65
    expected_waist_x = 415 + (338 - 415) * t  # 415 + (-77) * 0.33 = 389.59
    expected_waist_y = 310 + (315 - 310) * t  # 310 + 5 * 0.33 = 311.65
    
    print("预期插值结果 (t=0.33):")
    print(f"  head.x: {expected_head_x:.2f} (从 420 到 340)")
    print(f"  head.y: {expected_head_y:.2f} (从 235 到 240)")
    print(f"  waist.x: {expected_waist_x:.2f} (从 415 到 338)")
    print(f"  waist.y: {expected_waist_y:.2f} (从 310 到 315)")
    print()
    
    # 检查最新的debug log
    try:
        with open('debug_logs/20260118_161633_102/06_final_output.json', 'r') as f:
            data = json.load(f)
        
        # 获取第二帧（200ms，第一个插值帧）
        if len(data['final_animation']['keyframes']) > 1:
            kf_200 = data['final_animation']['keyframes'][1]
            actual_head = kf_200['characters']['char1']['joints']['head']
            actual_waist = kf_200['characters']['char1']['joints']['waist']
            
            print("实际插值结果 (200ms):")
            print(f"  head.x: {actual_head['x']:.2f}")
            print(f"  head.y: {actual_head['y']:.2f}")
            print(f"  waist.x: {actual_waist['x']:.2f}")
            print(f"  waist.y: {actual_waist['y']:.2f}")
            print()
            
            # 检查是否合理
            head_x_ok = 340 <= actual_head['x'] <= 420
            head_y_ok = 235 <= actual_head['y'] <= 240
            waist_x_ok = 338 <= actual_waist['x'] <= 415
            waist_y_ok = 310 <= actual_waist['y'] <= 315
            
            if head_x_ok and head_y_ok and waist_x_ok and waist_y_ok:
                print("✅ 插值结果在合理范围内")
            else:
                print("❌ 插值结果异常!")
                if not head_x_ok:
                    print(f"   head.x={actual_head['x']} 不在 [340, 420] 范围内")
                if not head_y_ok:
                    print(f"   head.y={actual_head['y']} 不在 [235, 240] 范围内")
                if not waist_x_ok:
                    print(f"   waist.x={actual_waist['x']} 不在 [338, 415] 范围内")
                if not waist_y_ok:
                    print(f"   waist.y={actual_waist['y']} 不在 [310, 315] 范围内")
    
    except Exception as e:
        print(f"无法读取debug log: {e}")

if __name__ == '__main__':
    test_interpolation()

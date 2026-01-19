#!/usr/bin/env python3
"""
快速验证插值修复
检查最新debug log的插值效果
"""
import json
import sys
from pathlib import Path

def check_latest_debug_log():
    """检查最新的debug log"""
    debug_dir = Path('debug_logs')
    
    # 找到最新的debug目录
    if not debug_dir.exists():
        print("❌ debug_logs目录不存在")
        return False
    
    subdirs = [d for d in debug_dir.iterdir() if d.is_dir()]
    if not subdirs:
        print("❌ 没有找到debug log")
        return False
    
    latest = max(subdirs, key=lambda d: d.name)
    print(f"📁 检查最新log: {latest.name}")
    print("=" * 70)
    
    # 读取final output
    final_output = latest / '06_final_output.json'
    if not final_output.exists():
        print("❌ 找不到06_final_output.json")
        return False
    
    with open(final_output, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    kfs = data['final_animation']['keyframes']
    
    # 检查关节数量
    first_char = kfs[0]['characters']['char1']
    joints = first_char.get('joints', first_char)
    joint_count = len(joints)
    
    print(f"✅ 总帧数: {len(kfs)}")
    print(f"✅ 关节数量: {joint_count}")
    print(f"✅ 关节列表: {', '.join(sorted(joints.keys()))}")
    print()
    
    # 检查前几帧的插值平滑度
    print("检查插值平滑度:")
    print("-" * 70)
    
    issues = []
    for i in range(min(5, len(kfs) - 1)):
        kf1 = kfs[i]
        kf2 = kfs[i + 1]
        
        char1 = kf1['characters']['char1']
        char2 = kf2['characters']['char1']
        
        joints1 = char1.get('joints', char1)
        joints2 = char2.get('joints', char2)
        
        if 'head' in joints1 and 'head' in joints2:
            head1 = joints1['head']
            head2 = joints2['head']
            
            dx = head2['x'] - head1['x']
            dy = head2['y'] - head1['y']
            
            # 检查是否有异常跳变（单帧变化超过100像素）
            if abs(dx) > 100 or abs(dy) > 100:
                issues.append(f"  ⚠️  帧{i}→{i+1}: Δx={dx:+.1f}, Δy={dy:+.1f} (异常跳变!)")
            else:
                print(f"  ✅ 帧{i}→{i+1}: Δx={dx:+6.1f}, Δy={dy:+6.1f}")
    
    print()
    
    if issues:
        print("发现问题:")
        for issue in issues:
            print(issue)
        return False
    
    # 读取原始数据检查是否保持原始DOF
    raw_data = latest / '03_animation_raw.json'
    if raw_data.exists():
        with open(raw_data, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        
        raw_kf = raw['animation_data']['keyframes'][0]
        raw_char = raw_kf['characters']['char1']
        
        if 'dof' in raw_char:
            dof = raw_char['dof']
            expected_joints = 5 if dof == 6 else 11
            
            if joint_count == expected_joints:
                print(f"✅ DOF级别正确: {dof}dof ({joint_count}个关节)")
            else:
                print(f"⚠️  关节数量异常: 期望{expected_joints}个，实际{joint_count}个")
                return False
    
    print()
    print("=" * 70)
    print("✅ 插值修复验证通过！")
    print("=" * 70)
    return True

if __name__ == '__main__':
    success = check_latest_debug_log()
    sys.exit(0 if success else 1)

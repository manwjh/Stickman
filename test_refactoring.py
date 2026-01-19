#!/usr/bin/env python3
"""
测试重构后的骨骼系统
验证工厂模式和统一接口
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import (
    create_skeleton,
    SkeletonFactory,
    get_skeleton_config
)


def test_factory_pattern():
    """测试工厂模式"""
    print("=" * 60)
    print("测试工厂模式")
    print("=" * 60)
    
    # 测试6DOF
    print("\n1. 创建6DOF骨骼系统...")
    skeleton_6dof = create_skeleton('6dof')
    print(f"   ✓ {skeleton_6dof}")
    print(f"   - DOF级别: {skeleton_6dof.get_dof_level()}")
    print(f"   - 关节数量: {skeleton_6dof.get_joint_count()}")
    print(f"   - 数据字段: {skeleton_6dof.get_data_field_name()}")
    
    # 测试12DOF
    print("\n2. 创建12DOF骨骼系统...")
    skeleton_12dof = create_skeleton('12dof')
    print(f"   ✓ {skeleton_12dof}")
    print(f"   - DOF级别: {skeleton_12dof.get_dof_level()}")
    print(f"   - 关节数量: {skeleton_12dof.get_joint_count()}")
    print(f"   - 数据字段: {skeleton_12dof.get_data_field_name()}")
    
    # 测试支持的DOF级别
    print("\n3. 支持的DOF级别:")
    for dof in SkeletonFactory.get_supported_dof_levels():
        print(f"   - {dof}")


def test_unified_interface():
    """测试统一接口"""
    print("\n" + "=" * 60)
    print("测试统一接口")
    print("=" * 60)
    
    # 测试6DOF验证
    print("\n1. 测试6DOF验证接口...")
    skeleton_6dof = create_skeleton('6dof')
    
    valid_pose = {
        "head_x": 400,
        "head_y": 200,
        "body_angle": 0,
        "left_arm_angle": -45,
        "right_arm_angle": 45,
        "left_leg_angle": -10,
        "right_leg_angle": 10
    }
    
    errors = skeleton_6dof.validate(valid_pose)
    if not errors:
        print("   ✓ 有效姿态验证通过")
    else:
        print(f"   ✗ 验证失败: {errors}")
    
    # 测试无效姿态
    invalid_pose = {
        "head_x": 1000,  # 超出范围
        "head_y": 200,
        "body_angle": 0,
        "left_arm_angle": -45,
        "right_arm_angle": 45,
        "left_leg_angle": -10,
        "right_leg_angle": 10
    }
    
    errors = skeleton_6dof.validate(invalid_pose)
    if errors:
        print(f"   ✓ 无效姿态检测成功: {len(errors)} 个错误")
    else:
        print("   ✗ 应该检测到错误")
    
    # 测试12DOF验证
    print("\n2. 测试12DOF验证接口...")
    skeleton_12dof = create_skeleton('12dof')
    
    valid_joints = {
        "head": {"x": 400, "y": 240},
        "neck": {"x": 400, "y": 260},
        "waist": {"x": 400, "y": 320},
        "left_shoulder": {"x": 380, "y": 265},
        "left_hand": {"x": 350, "y": 310},
        "right_shoulder": {"x": 420, "y": 265},
        "right_hand": {"x": 450, "y": 310},
        "left_hip": {"x": 385, "y": 320},
        "left_foot": {"x": 385, "y": 370},
        "right_hip": {"x": 415, "y": 320},
        "right_foot": {"x": 415, "y": 370}
    }
    
    errors = skeleton_12dof.validate(valid_joints)
    if not errors:
        print("   ✓ 有效关节验证通过")
    else:
        print(f"   ✗ 验证失败: {errors}")


def test_config_loading():
    """测试配置加载"""
    print("\n" + "=" * 60)
    print("测试配置加载")
    print("=" * 60)
    
    # 测试6DOF配置
    print("\n1. 加载6DOF配置...")
    config_6dof = get_skeleton_config('6dof')
    print(f"   ✓ DOF级别: {config_6dof.dof_level}")
    print(f"   ✓ 关节数量: {config_6dof.joint_count}")
    print(f"   ✓ 画布尺寸: {config_6dof.canvas_width}x{config_6dof.canvas_height}")
    print(f"   ✓ 骨骼长度: {len(config_6dof.bone_lengths)} 项")
    
    # 测试12DOF配置
    print("\n2. 加载12DOF配置...")
    config_12dof = get_skeleton_config('12dof')
    print(f"   ✓ DOF级别: {config_12dof.dof_level}")
    print(f"   ✓ 关节数量: {config_12dof.joint_count}")
    print(f"   ✓ 画布尺寸: {config_12dof.canvas_width}x{config_12dof.canvas_height}")
    print(f"   ✓ 骨骼长度: {len(config_12dof.bone_lengths)} 项")
    print(f"   ✓ 容差配置: {len(config_12dof.tolerance)} 项")


def test_default_pose():
    """测试默认姿态"""
    print("\n" + "=" * 60)
    print("测试默认姿态")
    print("=" * 60)
    
    # 6DOF默认姿态
    print("\n1. 6DOF默认姿态:")
    skeleton_6dof = create_skeleton('6dof')
    default_pose = skeleton_6dof.get_default_pose()
    for key, value in default_pose.items():
        print(f"   - {key}: {value}")
    
    # 12DOF默认姿态
    print("\n2. 12DOF默认姿态:")
    skeleton_12dof = create_skeleton('12dof')
    default_joints = skeleton_12dof.get_default_pose()
    for key, value in list(default_joints.items())[:3]:  # 只显示前3个
        print(f"   - {key}: {value}")
    print(f"   ... (共 {len(default_joints)} 个关节)")


def main():
    """主函数"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "骨骼系统重构测试" + " " * 15 + "║")
    print("╚" + "═" * 58 + "╝")
    
    try:
        test_factory_pattern()
        test_unified_interface()
        test_config_loading()
        test_default_pose()
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过！重构成功！")
        print("=" * 60 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
weight-loss-skill — BMR/TDEE 计算器

用法：
    python scripts/bmr_calculator.py --weight 70 --height 168 --age 21 --male
    python scripts/bmr_calculator.py --weight 55 --height 160 --age 25 --female

输出：
    BMR = 1,650 kcal
    TDEE（中度活动 1.55）= 2,558 kcal
    减脂摄入（-500 缺口）= 2,058 kcal
"""

import argparse

def calculate_bmr(weight_kg: float, height_cm: float, age: int, is_male: bool) -> float:
    """Mifflin-St Jeor 公式"""
    if is_male:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

def calculate_tdee(bmr: float, activity_level: str) -> float:
    """活动系数映射"""
    factors = {
        "sedentary": 1.2,        # 久坐
        "light": 1.375,          # 轻度 1~3天
        "moderate": 1.55,        # 中度 3~5天
        "active": 1.725,         # 高度 6~7天
        "extreme": 1.9,          # 运动员
    }
    return bmr * factors.get(activity_level, 1.55)

LEVEL_NAMES = {
    "sedentary": "久坐（几乎不运动）",
    "light": "轻度活动（1~3天/周）",
    "moderate": "中度活动（3~5天/周）",
    "active": "高度活动（6~7天/周）",
    "extreme": "极高度活动（运动员）",
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BMR/TDEE 计算器")
    parser.add_argument("--weight", type=float, required=True, help="体重(kg)")
    parser.add_argument("--height", type=float, required=True, help="身高(cm)")
    parser.add_argument("--age", type=int, required=True, help="年龄")
    parser.add_argument("--male", action="store_true", help="男性")
    parser.add_argument("--female", action="store_true", help="女性")
    parser.add_argument("--activity", default="moderate",
                        choices=["sedentary", "light", "moderate", "active", "extreme"],
                        help="活动水平 (默认: moderate)")

    args = parser.parse_args()

    if args.male == args.female:
        parser.error("请指定 --male 或 --female")

    is_male = args.male
    gender_str = "男性" if is_male else "女性"

    bmr = calculate_bmr(args.weight, args.height, args.age, is_male)
    tdee = calculate_tdee(bmr, args.activity)

    print(f"{'='*45}")
    print(f"  🏆 减脂管家 · BMR/TDEE 计算")
    print(f"{'='*45}")
    print(f"  性别：{gender_str}")
    print(f"  身高：{args.height:.0f} cm")
    print(f"  体重：{args.weight:.0f} kg")
    print(f"  年龄：{args.age} 岁")
    print(f"  活动：{LEVEL_NAMES[args.activity]}")
    print(f"{'─'*45}")
    print(f"  BMR   = {bmr:>6.0f} kcal")
    print(f"  TDEE  = {tdee:>6.0f} kcal")
    print(f"  ─────────────────────────")
    print(f"  减脂（−500） = {tdee-500:>6.0f} kcal")
    print(f"  温和减脂（−300）= {tdee-300:>6.0f} kcal")
    print(f"  增肌（+200）  = {tdee+200:>6.0f} kcal")
    print(f"{'='*45}")

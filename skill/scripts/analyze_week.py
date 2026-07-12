#!/usr/bin/env python3
"""
weight-loss-skill — 一周饮食分析器

解析一周饮食文本 → 输出 6 维评分 + 结构分析

用法：
    python scripts/analyze_week.py --input week_data.txt --weight 70 --height 168 --age 21 --male

输入格式（week_data.txt）：
    周一
    早餐: 小米粥 水煮蛋 凉拌黄瓜
    午餐: 土豆烧牛肉 清炒上海青 米饭
    晚餐: 番茄鸡蛋面 蒜蓉西兰花
    周二
    早餐: 豆浆 肉包子 煮玉米
    ...
"""

import argparse
import sys
import re
from collections import defaultdict

# ═══════════════════════════════════════════
# 菜品标签系统
# ═══════════════════════════════════════════

LIGHT_COOK = {"清蒸", "白灼", "清炒", "凉拌", "汤羹", "煮", "上汤", "蒸"}
HEAVY_COOK = {"红烧", "油炸", "干煸", "麻辣", "糖醋", "回锅", "油焖", "爆炒"}
PROTEIN_KEYWORDS = {
    "鱼": "🐟鱼虾", "虾": "🐟鱼虾", "鲈鱼": "🐟鱼虾", "鳕鱼": "🐟鱼虾", "基围虾": "🐟鱼虾",
    "鸡": "🐔鸡鸭", "鸭": "🐔鸡鸭", "鸡胸": "🐔鸡鸭", "鸡腿": "🐔鸡鸭", "白切鸡": "🐔鸡鸭",
    "鸡蛋": "🥚蛋豆", "蛋": "🥚蛋豆", "豆腐": "🥚蛋豆", "豆浆": "🥚蛋豆",
    "牛肉": "🥩牛肉", "牛": "🥩牛肉",
    "猪肉": "🐷猪肉", "排骨": "🐷猪肉", "里脊": "🐷猪肉",
}
GRAIN_KEYWORDS = {"杂粮", "糙米", "藜麦", "玉米", "紫薯", "红薯", "燕麦", "全麦"}
FINE_GRAIN = {"米饭", "馒头", "面条", "包子", "饺子", "米粉", "米线"}

VEGETABLES = {
    "黄瓜", "西兰花", "油菜", "上海青", "生菜", "娃娃菜", "菠菜", "秋葵",
    "芦笋", "藕片", "豆苗", "空心菜", "菜心", "冬瓜", "番茄", "木耳",
    "海带", "萝卜", "南瓜", "丝瓜", "豆芽", "茄子", "辣椒(蔬菜)",
}

def parse_dish(dish: str) -> dict:
    """解析一道菜，返回标签"""
    result = {
        "name": dish.strip(),
        "cook_method": None,
        "has_protein": False,
        "protein_type": None,
        "is_grain": False,
        "is_fine_grain": False,
        "is_heavy": False,
        "is_light": False,
        "is_vegetable": False,
        "vegetable_name": None,
    }
    for kw in LIGHT_COOK:
        if kw in dish:
            result["cook_method"] = kw
            result["is_light"] = True
            break
    for kw in HEAVY_COOK:
        if kw in dish:
            result["cook_method"] = kw
            result["is_heavy"] = True
            result["is_light"] = False
            break
    for kw, ptype in PROTEIN_KEYWORDS.items():
        if kw in dish:
            result["has_protein"] = True
            result["protein_type"] = ptype
            break
    for kw in GRAIN_KEYWORDS:
        if kw in dish:
            result["is_grain"] = True
            break
    for kw in FINE_GRAIN:
        if kw in dish:
            result["is_fine_grain"] = True
            break
    for veg in VEGETABLES:
        if veg in dish and "饭" not in dish and "面" not in dish and "粉" not in dish:
            result["is_vegetable"] = True
            result["vegetable_name"] = veg
            break
    return result

def analyze_week(text: str, bmr: float, tdee: float):
    """主分析函数"""
    # 解析数据
    days = re.split(r"(周一|周二|周三|周四|周五|周六|周日)", text)
    meals = []
    day_count = 0
    all_veggies = defaultdict(set)

    for i, day_name in enumerate(days):
        if day_name in ("周一","周二","周三","周四","周五","周六","周日"):
            day_count += 1
            block = days[i+1] if i+1 < len(days) else ""
            meal_sections = re.split(r"(早餐|中餐|午餐|晚餐)[：:]", block)

            for j, meal_type in enumerate(meal_sections):
                if meal_type in ("早餐","中餐","午餐","晚餐"):
                    content = meal_sections[j+1] if j+1 < len(meal_sections) else ""
                    dishes = re.split(r"[+、,，/]", content)
                    for d in dishes:
                        d = d.strip()
                        if len(d) < 2:
                            continue
                        info = parse_dish(d)
                        info["day"] = day_name
                        info["meal"] = meal_type
                        meals.append(info)
                        if info["is_vegetable"] and info["vegetable_name"]:
                            all_veggies[day_name].add(info["vegetable_name"])

    total_meals = len([m for m in meals if m["name"]])
    # 蛋白评分
    protein_meals = sum(1 for m in meals if m["has_protein"])
    protein_score = min(10, max(0, (protein_meals / max(21, total_meals)) * 10))

    # 蔬菜评分
    veg_daily = [len(v) for v in all_veggies.values()]
    avg_veg = sum(veg_daily) / max(1, len(veg_daily)) if veg_daily else 0
    if avg_veg >= 3.0: veg_score = 10
    elif avg_veg >= 2.5: veg_score = 8
    elif avg_veg >= 2.0: veg_score = 6
    elif avg_veg >= 1.5: veg_score = 4
    else: veg_score = 2

    # 碳水评分
    grain_days = 0
    for day_name in ["周一","周二","周三","周四","周五","周六","周日"]:
        day_grains = [m for m in meals if m["day"] == day_name and m["is_grain"]]
        if day_grains:
            grain_days += 1
    carb_score = min(10, max(0, grain_days * 1.5))

    # 清淡度评分
    heavy_meals = sum(1 for m in meals if m["is_heavy"])
    if heavy_meals <= 1: light_score = 10
    elif heavy_meals <= 3: light_score = 8
    elif heavy_meals <= 5: light_score = 5
    elif heavy_meals <= 7: light_score = 3
    else: light_score = 1

    # 综合评分
    total_score = round((protein_score + veg_score + carb_score + light_score) / 4, 1)

    # 输出
    print(f"{'='*50}")
    print(f"  📊 一周饮食分析报告")
    print(f"{'='*50}")
    print(f"  📅 记录天数：{day_count} 天")
    print(f"  🍽️  总菜品数：{total_meals}")
    print(f"{'─'*50}")
    print(f"  🥩 蛋白评分：{protein_score:.0f}/10（含蛋白 {protein_meals}/{total_meals} 道）")
    print(f"  🥦 蔬菜评分：{veg_score:.0f}/10（日均 {avg_veg:.1f} 种）")
    print(f"  🍚 碳水评分：{carb_score:.0f}/10（粗粮 {grain_days}/{day_count} 天）")
    print(f"  🧂 清淡评分：{light_score:.0f}/10（重油 {heavy_meals} 道）")
    print(f"{'─'*50}")
    print(f"  📊 综合评分：{total_score}/10")
    print(f"  🔥 BMR：{bmr:.0f} kcal  |  TDEE：{tdee:.0f} kcal")
    print(f"  🥗 建议摄入：{tdee-500:.0f} kcal（−500 缺口）")
    print(f"{'='*50}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="一周饮食分析器")
    parser.add_argument("--input", required=True, help="饮食数据文件路径")
    parser.add_argument("--weight", type=float, default=70, help="体重(kg)")
    parser.add_argument("--height", type=float, default=168, help="身高(cm)")
    parser.add_argument("--age", type=int, default=21, help="年龄")
    parser.add_argument("--male", action="store_true", help="男性")
    parser.add_argument("--female", action="store_true", help="女性")

    args = parser.parse_args()

    if args.male == args.female:
        parser.error("请指定 --male 或 --female")

    # 计算 BMR
    if args.male:
        bmr = 10 * args.weight + 6.25 * args.height - 5 * args.age + 5
    else:
        bmr = 10 * args.weight + 6.25 * args.height - 5 * args.age - 161

    tdee = bmr * 1.55  # 默认中度活动

    # 读取数据
    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    analyze_week(text, bmr, tdee)

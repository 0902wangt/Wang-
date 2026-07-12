# 🏆 weight-loss-skill — 全能减脂管家

> **AI 驱动的个人减脂管理系统** · 开箱即用 Hermes Agent Skill

## 📌 选题背景

传统的减脂工具（计算器、打卡 App）只能做纯数字记录，无法理解"你吃了什么"、"食堂有什么菜"、"预算够不够"这些真实场景问题。  
本 Skill 让 AI 扮演**私人营养师**角色，在真实条件（学校食堂/外卖/有限预算）下帮你做更好的饮食+运动决策。

**核心价值：** 没有 AI，这个功能根本做不到——AI 必须理解模糊的菜品描述、识别烹饪方式、根据历史数据推理口味偏好、联动运动计划动态调摄入。

---

## ✨ 功能简介

| 功能 | 说明 |
|:----|:------|
| 🧸 **智能建档** | Mifflin-St Jeor 公式自动算 BMR/TDEE/建议摄入 |
| 🍱 **每日推荐** | 根据档案+历史+运动计划推荐三餐（含食堂价格） |
| 🔍 **进食评估** | 文字/拍照 → AI 评估蛋白/蔬菜/油腻度 |
| 🏋️ **运动追踪** | 记录消耗 → 联动调摄入（高强度+200/恢复日不加） |
| 📊 **周分析** | 6维硬性评分雷达 + 食堂替代方案 |
| 🧬 **口味画像** | 量化算法判定饮食风格（粤式/川湘/北方/均衡） |
| 📋 **下周推荐** | 基于上周问题+口味+未试新菜，每天推荐一餐 |
| 💰 **预算不够** | 极致省钱模式 ¥25~30/天 |
| 🎨 **骚包HTML** | 暗紫星空粉渐变 4Tab 全面健康报告 |
| 🚨 **错误处理** | 自动拦截 9999kcal 等异常数据 |

---

## 📂 仓库结构

```
weight-loss-skill/
├── skill/                          # Skill 核心文件
│   ├── SKILL.md                    # 技能定义（YAML前端+完整提示词）
│   ├── scripts/                    # Python 工具脚本
│   │   ├── bmr_calculator.py       # BMR/TDEE 命令行计算器
│   │   ├── analyze_week.py         # 一周饮食文本解析+6维评分
│   │   └── requirements.txt        # Python 依赖
│   └── references/                 # 配置参考 & 最佳实践
│       ├── saobao-style-guide.md   # HTML 骚包风格 CSS 完整模板
│       ├── usage-guide.md          # 快速上手指南
│       └── quick-reference.md      # 公式/阈值/触发词速查卡
├── data/                           # 测试数据集
│   ├── sample_week1.md             # 样本周1（清淡健康周）
│   ├── sample_week2.md             # 样本周2（油腻问题周）
│   └── sample_exercise.md          # 样本运动数据
├── tests/                          # 测试记录
│   └── test_record.md              # 测试环境+步骤+结果
├── iteration/                      # 迭代升级说明
│   └── iteration_log.md            # 5步迭代法记录（2轮）
└── README.md                       # 本文件
```

---

## 🚀 使用方式

### 前提

- Hermes Agent（运行环境）
- Python 3.9+（如需运行脚本）

### 安装

```bash
# 克隆仓库
git clone https://github.com/0902wangt/Wang-.git

# 将 skill/ 目录链接到 Hermes Skills 目录
# Windows:
mklink /D %USERPROFILE%\AppData\Local\hermes\skills\daily-life\weight-loss-skill %CD%\skill

# 或直接复制
cp -r skill /c/Users/0902wangt/AppData/Local/hermes/skills/daily-life/weight-loss-skill
```

### 快速开始

```
1️⃣ 建档：
   减脂管家，帮我建档，175cm，75kg，目标70kg，男，25岁

2️⃣ 每日使用：
   今天吃什么           → AI 推荐三餐
   我吃了：青椒炒牛肉+米饭  → AI 评估营养

3️⃣ 周总结：
   这周我吃了：（7天数据） → 6维雷达+食堂替代方案
   生成全面健康档案       → 4Tab 骚包 HTML 报告
```

### 脚本使用

```bash
cd skill/scripts
pip install -r requirements.txt

# 算 BMR/TDEE
python bmr_calculator.py --weight 70 --height 168 --age 21 --male

# 分析一周饮食
python analyze_week.py --input ../../data/sample_week1.md --weight 70 --height 168 --age 21 --male
```

---

## 📝 迭代记录

共完成 **2 轮迭代**，详见 [`iteration/iteration_log.md`](iteration/iteration_log.md)：

| 迭代 | 痛点 | 改进 |
|:----|:-----|:-----|
| #1 | BMR/TDEE 拍脑袋，数值偏低~500kcal | 引入 Mifflin-St Jeor 标准公式 |
| #2 | 评分/口味画像无量化标准，不同AI结果不同 | 硬性评分表+菜品标签系统 |

---

## 📜 依赖

- Hermes Agent（运行环境）
- Python 3.9+（可选，仅脚本需要）
- openpyxl / pandas（可选，仅 analyze_week.py 需要）

---

## 📄 License

MIT

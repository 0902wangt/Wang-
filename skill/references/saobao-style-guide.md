# 🌟 骚包风格 HTML CSS 模板

## 引用方式

在 HTML `<head>` 中直接复制以下 CSS。这是完整的暗紫星空骚包风模板。

## 完整 CSS

```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap');

* { margin:0; padding:0; box-sizing:border-box; }

body {
  font-family:'Noto Sans SC',sans-serif;
  min-height:100vh; padding:24px 16px 40px; overflow-x:hidden;
  background:linear-gradient(135deg,#1a0033 0%,#2d004d 20%,#4a0066 40%,#660080 55%,#4a0066 70%,#2d004d 85%,#1a0033 100%);
}

/* 闪烁星点 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none;
  background:radial-gradient(2px 2px at 20%30%,#fff,transparent),
             radial-gradient(2px 2px at 40%70%,#f9a8d4,transparent),
             radial-gradient(3px 3px at 60%20%,#fff,transparent),
             radial-gradient(2px 2px at 80%50%,#c084fc,transparent),
             radial-gradient(2px 2px at 10%80%,#fff,transparent),
             radial-gradient(3px 3px at 50%40%,#f9a8d4,transparent);
  animation:twinkle 4s ease-in-out infinite alternate;
}
@keyframes twinkle{0%{opacity:.4}100%{opacity:.9}}
```

## 核心配色

| 用途 | 色值 |
|:----|:----:|
| 背景开始 | `#1a0033` |
| 背景中间 | `#4a0066` |
| 背景结束 | `#660080` |
| 粉色主色 | `#f9a8d4` |
| 紫色辅色 | `#c084fc` / `#e879f9` |
| 青色强调 | `#22d3ee` |
| 绿色成功 | `#6ee7b7` |
| 橙色警告 | `#fb923c` / `#fdba74` |
| 蓝色信息 | `#93c5fd` |
| 红色异常 | `#f87171` |
| 卡片背景 | `rgba(45,0,77,.6)` |
| 文字主色 | `#e9d5ff` |
| 文字辅色 | `#a78bfa` / `#c084fc` |

## 组件规范

### 毛玻璃卡片
```css
.section {
  background: rgba(45,0,77,.6);
  backdrop-filter: blur(14px);
  border-radius: 24px;
  padding: 28px 32px;
  border: 1px solid rgba(249,168,212,.12);
  box-shadow: 0 8px 32px rgba(0,0,0,.25);
}
```

### 霓虹渐变标题
```css
.gradient-text {
  background: linear-gradient(135deg,#f9a8d4,#e879f9,#c084fc,#f9a8d4);
  background-size: 300%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: wave 4s ease infinite;
}
@keyframes wave{0%{background-position:0%50%}50%{background-position:100%50%}100%{background-position:0%50%}}
```

### 浮动装饰
```css
.floating-deco{position:fixed;pointer-events:none;font-size:28px;animation:floaty 6s ease-in-out infinite;z-index:0;}
@keyframes floaty{0%,100%{transform:translateY(0)rotate(0deg);opacity:.5}50%{transform:translateY(-16px)rotate(6deg);opacity:.85}}
```

### 进度条（评分用）
```css
.bar-track{flex:1;height:26px;background:rgba(0,0,0,.25);border-radius:14px;overflow:hidden;box-shadow:inset 0 2px 4px rgba(0,0,0,.3);}
.bar-fill{height:100%;border-radius:14px;transition:width 1.5s cubic-bezier(.34,1.56,.64,1);}
.bar-fill.green{background:linear-gradient(90deg,#6ee7b7,#34d399)}
.bar-fill.orange{background:linear-gradient(90deg,#fdba74,#fb923c)}
.bar-fill.pink{background:linear-gradient(90deg,#f9a8d4,#e879f9)}
.bar-fill.red{background:linear-gradient(90deg,#f87171,#ef4444)}
```

### Tab 切换
```css
.tabs{display:flex;gap:4px;justify-content:center;padding:0 12px;}
.tab-btn{flex:1;max-width:160px;padding:14px 10px 12px;background:rgba(45,0,77,.35);border-radius:16px 16px 0 0;border:1px solid rgba(249,168,212,.1);border-bottom:none;color:#a78bfa;font-size:16px;font-weight:600;cursor:pointer;font-family:inherit;}
.tab-btn.active{background:rgba(60,0,100,.75);color:#f9a8d4;border-color:rgba(249,168,212,.25);}
.tab-content{display:none}
.tab-content.active{display:block}
```

### 响应式断点
```css
@media(max-width:700px){
  .section{padding:20px 16px}
  .metrics,.summary-grid{grid-template-columns:1fr 1fr;gap:8px}
  .meals,.ex-grid,.rec-body,.profile-grid{grid-template-columns:1fr}
  .header-name{font-size:26px}
  .tab-btn{font-size:13px;max-width:none}
}
```

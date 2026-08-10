---
name: ui-mockup-shots
description: 'Render each phone screen in an integrated UI mockup deck (多个手机框排在一个 HTML 里) to its own PNG so the screens can be visually checked. Use after editing any mockup HTML, or when the user asks to 截图 / 看看渲染效果 / 检查 UI 稿 / verify a mockup renders correctly.'
---

# 整合 UI 稿逐屏截图

**用途：** 把整合稿（一页排了 N 个手机框）拆成一屏一张 PNG，然后**用 Read 工具逐张看图核验**。

配套 `ui-ux-design-flow` skill 的第四步使用；单独用也可以。

## 为什么必须截图

整合稿改完只做静态检查（div 配平、symbol 引用是否存在）**查不出这几类问题**，它们全都要靠肉眼看图：

- SVG 路径写错 —— 标签合法但画出来不是那个图标（比如"医院"图标画成了房子而不是十字）
- `<use>` 引用画到了可视区外 —— 外层 `<svg>` 和 `<symbol>` 都声明 `viewBox` 时，影子 svg 定位在用户坐标 (0,0)，如果外层 viewBox 的原点不是 (0,0) 就完全不重叠，元素静默消失
- 屏与屏之间结构不一致 —— 同一个真实页面的不同视图，一屏有页头另一屏没有
- 说明性内容混进了手机框 —— 违反「页面里只能有真实用户看得到的东西」
- 布局溢出 / 被 tabbar 遮挡 / 空白屏

## 用法

```bash
# 自动定位 shots.py：项目级安装和全局安装都能找到（在项目根目录下执行）
S=$(ls .claude/skills/ui-mockup-shots/shots.py ~/.claude/skills/ui-mockup-shots/shots.py 2>/dev/null | head -1)

python3 "$S" <稿件.html>                 # 全量
python3 "$S" <稿件.html> A7 P4           # 只截指定屏
python3 "$S" <稿件.html> --list          # 只列屏号
python3 "$S" <稿件.html> --sheet         # 额外拼总览图（需 Pillow）
python3 "$S" <稿件.html> -o /tmp/shots   # 指定输出目录
```

脚本只按传入的 HTML 路径推导输出位置，**不依赖自身所在目录**，所以任何项目、任何位置的稿件都能截。

默认输出到稿件同级的 `.shots/`。**出图后必须用 Read 工具把 PNG 读进来逐张看** —— 只跑脚本不看图等于没做。

屏多的时候：先 `--sheet` 看总览定位可疑屏，再单独放大看那几屏。总览图只能判断大结构，图标画错这类细节必须看单屏原图。

## 稿件需要满足的约定

脚本靠这几个约定识别每一屏，你的整合稿要对得上，否则截不出来：

| 约定 | 默认值 | 说明 |
| --- | --- | --- |
| 真实页面容器 | `.phone-shell` | 模拟真实 App 页面的手机框 |
| 规格图容器 | `.spec-shell` | 虚线卡 + ◇ 标记，只有这种框里允许出现说明性标注 |
| 屏号来源 | `<span class="frame-tag">` 的第一段（`·` 之前） | 用于 `--list` 和按屏号筛选 |

用了别的 class 名就改 `shots.py` 里对应的常量，或把稿件改成这套约定。

## 已知边界

- **字体**：稿件若从 Google Fonts 拉字体，沙箱里网络通常不通，会回退到系统字体。布局崩没崩、图标对不对能看出来；**字重/字距/换行位置的精修必须在真浏览器里确认**。
- 依赖 `/Applications/Google Chrome.app`（macOS）；`--sheet` 额外依赖 Pillow。

## 实现上踩过的坑

取屏内容**不要用非贪婪正则** `<div class="phone-shell">.*?</div></div>`：屏内任何一处相邻的 `</div></div>` 都会让它提前截断，症状是截出来一片空白（而且很容易误判成稿件本身坏了）。脚本里用的是按 `<div` / `</div>` 嵌套深度配对的 `slice_div()`。

## 相关约定

- 页面框里零解释 —— 手机框内只能有真实用户看得见的东西，批注一律放框外
- 画之前先对着真实代码验证逻辑，别把需求文档文字直译成像素 —— 完整规则见 `ui-ux-design-flow` skill

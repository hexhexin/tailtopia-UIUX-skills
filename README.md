# tailtopia-UIUX-skills

我自用的 Claude Code UI/UX Skills，外加它依赖的三个第三方 skill，克隆下来即可跑通整套流程。

## 我写的（`skills/`）

| Skill | 作用 |
| --- | --- |
| [`ui-ux-design-flow`](skills/ui-ux-design-flow/) | UI/UX 设计稿的标准工作流：完整度 → 代码对齐 → 美观 → 核对确认 → 拆页。要求先列全页面/状态清单（含空态、失败态），再对着真实代码补齐，最后才调样式。**这是入口，其余都被它调用。** |
| [`tailtopia-ui-shots`](skills/tailtopia-ui-shots/) | 把「一页排了 N 个手机框」的整合 UI 稿逐屏截成 PNG，用来肉眼核验图标画错、元素消失、布局溢出这类只有看图才发现的问题。依赖本机 Chrome。 |

## 第三方依赖（`vendor-skills/`）

`ui-ux-design-flow` 的第三步**明确要求调用**下面三个，缺了工作流就是断的，所以一并收录。
它们不是我写的，许可证与出处见 [NOTICE.md](NOTICE.md)。

| Skill | 在流程里干什么 | 许可证 |
| --- | --- | --- |
| [`ui-ux-pro-max`](vendor-skills/ui-ux-pro-max/) | 第三步一开始**每次都调**：移动端信息层次、间距体系、交互态、空/错态范式、配色字体、对比度检查 | MIT |
| [`make-interfaces-feel-better`](vendor-skills/make-interfaces-feel-better/) | 第三步末尾 + 第四步细节打磨：同心圆角、光学对齐、阴影优于描边、点击热区、tabular-nums | MIT |
| [`frontend-design`](vendor-skills/frontend-design/) | 需要创新/对外分享页时调：版式个性、字体配对、hero 结构、如何不显得像模板 | Apache-2.0 |

## 怎么安装

```bash
git clone git@github.com:hexhexin/tailtopia-UIUX-skills.git
cd tailtopia-UIUX-skills

# 全部装到全局（所有项目生效）
cp -R skills/* vendor-skills/* ~/.claude/skills/

# 或只装到某个项目（只在该项目生效）
cp -R skills/* vendor-skills/* /path/to/your-project/.claude/skills/
```

重启 Claude Code 后 `/ui-ux-design-flow` 就能用了，它会自动调起另外四个。

已经装过其中某个第三方 skill 的话，跳过对应目录即可，不要覆盖你自己那份。

## 使用前须知

这两个 skill 是**按我自己的工作区习惯写的**，直接拿去用需要改几处：

- `ui-ux-design-flow` 里的代码路径、颜色/文案取值位置、以及踩坑实录都来自一个 Flutter 私有仓库（`petgo-platform`）。这些是「去哪儿查真实代码实现」的指路牌，换成你自己项目的对应位置即可，**五步工作流和那些硬规则本身是通用的**。
- `tailtopia-ui-shots` 的 `shots.py` 依赖 `/Applications/Google Chrome.app`，`--sheet` 拼图额外需要 Pillow。它只认 `.phone-shell` / `.spec-shell` 两种容器，屏号取自 `<span class="frame-tag">`——如果你的 mockup 用别的 class，需要改脚本。

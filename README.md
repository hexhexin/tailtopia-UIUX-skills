# claude-skills

我自用的 Claude Code Skills。

## 包含的 skill

| Skill | 作用 |
| --- | --- |
| [`ui-ux-design-flow`](skills/ui-ux-design-flow/) | UI/UX 设计稿的标准工作流：完整度 → 代码对齐 → 美观 → 核对确认 → 拆页。要求先列全页面/状态清单（含空态、失败态），再对着真实代码补齐，最后才调样式。 |
| [`tailtopia-ui-shots`](skills/tailtopia-ui-shots/) | 把「一页排了 N 个手机框」的整合 UI 稿逐屏截成 PNG，用来肉眼核验图标画错、元素消失、布局溢出这类只有看图才发现的问题。依赖本机 Chrome。 |

## 怎么安装

克隆下来，把需要的 skill 目录复制（或软链）到 Claude Code 的 skills 目录：

```bash
git clone git@github.com:hexhexin/tailtopia-UIUX-skills.git
cd tailtopia-UIUX-skills

# 装到某个项目里（只在该项目生效）
cp -R skills/ui-ux-design-flow /path/to/your-project/.claude/skills/

# 或装到全局（所有项目生效）
cp -R skills/ui-ux-design-flow ~/.claude/skills/
```

重启 Claude Code 后，`/ui-ux-design-flow` 就能用了。

## 使用前须知

这两个 skill 是**按我自己的工作区习惯写的**，直接拿去用需要改几处：

- `ui-ux-design-flow` 里引用了一个私有仓库（`petgo-platform`）和一批本机记忆 slug（`feedback_tailtopia_*`）。这些是「去哪儿查真实代码实现」的指路牌，换成你自己项目的仓库地址即可，工作流本身是通用的。
- `tailtopia-ui-shots` 的 `shots.py` 依赖 `/Applications/Google Chrome.app`，`--sheet` 拼图额外需要 Pillow。它只认 `.phone-shell` / `.spec-shell` 两种容器，屏号取自 `<span class="frame-tag">`——如果你的 mockup 用别的 class，需要改脚本。

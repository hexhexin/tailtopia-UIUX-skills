# tailtopia-UIUX-skills

我自用的 Claude Code UI/UX Skills，外加它依赖的三个第三方 skill，克隆下来即可跑通整套流程。

## 我写的（`skills/`）

| Skill | 作用 |
| --- | --- |
| [`ui-ux-design-flow`](skills/ui-ux-design-flow/) | UI/UX 设计稿的标准工作流：完整度 → 代码对齐 → 美观 → 核对确认 → 拆页。要求先列全页面/状态清单（含空态、失败态），再对着真实代码补齐，最后才调样式。**这是入口，其余都被它调用。** |
| [`ui-mockup-shots`](skills/ui-mockup-shots/) | 把「一页排了 N 个手机框」的整合 UI 稿逐屏截成 PNG，用来肉眼核验图标画错、元素消失、布局溢出这类只有看图才发现的问题。依赖本机 Chrome。 |

## 第三方依赖（`vendor-skills/`）

`ui-ux-design-flow` 的第三步**明确要求调用**下面三个，缺了工作流就是断的，所以一并收录。
它们不是我写的，许可证与出处见 [NOTICE.md](NOTICE.md)。

| Skill | 在流程里干什么 | 许可证 |
| --- | --- | --- |
| [`ui-ux-pro-max`](vendor-skills/ui-ux-pro-max/) | 第三步一开始**每次都调**：移动端信息层次、间距体系、交互态、空/错态范式、配色字体、对比度检查 | MIT |
| [`make-interfaces-feel-better`](vendor-skills/make-interfaces-feel-better/) | 第三步末尾 + 第四步细节打磨：同心圆角、光学对齐、阴影管景深/描边管结构、点击热区、tabular-nums、图标线重 | MIT |
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

### 多个项目共用一份（软链装法）

`cp` 装法每个项目一份实体，改一处别处不动，很快就漂移。多项目共用时改成软链，本仓库就是唯一副本，`git pull` 一次全部生效：

```bash
# 在每个项目的 .claude/skills/ 下执行，REPO 换成本仓库的实际路径
REPO=/path/to/tailtopia-UIUX-skills
for s in ui-ux-design-flow ui-mockup-shots; do ln -s "$REPO/skills/$s" "$s"; done
for s in ui-ux-pro-max make-interfaces-feel-better frontend-design; do ln -s "$REPO/vendor-skills/$s" "$s"; done
```

代价是路径被绑死：仓库改名或移走，所有项目的这几个 skill 会**静默失效**（Claude Code 不报错，只是技能列表里少几项）。用相对路径软链的话，还要求仓库和项目的相对位置不变。

目标项目本身是 git 仓库时，把 `.claude/` 写进 `.git/info/exclude`（本机生效、不产生仓库 diff），不要改团队共享的 `.gitignore`。

## 更新第三方依赖

```bash
./scripts/sync-vendor.sh
```

脚本会拉三个上游的 main HEAD 覆盖 `vendor-skills/`（含删除上游已移除的文件）、补回上游放在仓库根目录的 LICENSE，并打印新的 commit 号——**记得同步改 [NOTICE.md](NOTICE.md) 里的 commit 表格**，否则出处记录会和实际内容对不上。

## 第一次使用：填一份项目配置

`ui-ux-design-flow` 的流程是通用的，但「去哪儿查代码、文案、配色，产出放哪」每个项目不同。
这些值不写死在 skill 里，而是放在**你自己项目根目录**的：

```
.claude/ui-ux-design-flow.config.md
```

**你不用手写。** 装好后直接让 Claude 开始做设计稿，skill 的第 0 步发现配置不存在，
会把 [`skills/ui-ux-design-flow/config.example.md`](skills/ui-ux-design-flow/config.example.md)
里的问题一次性问你，答完自动生成配置文件。要提前看有哪些问题，打开那个模板即可。

问的大致是：项目名与技术栈、代码仓库在哪 / 本地路径 / 分支约定、页面代码目录、
文案和配色文件、设计稿与决策日志放哪、需求文档在哪。

答不上来的项填 `未配置`，skill 用到时会单独问你，不会自己瞎猜。

配置文件是本机私有的，不要提交到公开仓库。多个项目各有各的配置，互不影响。

## 使用前须知

- `ui-mockup-shots` 的 `shots.py` 依赖 `/Applications/Google Chrome.app`（macOS），`--sheet` 拼图额外需要 Pillow。
- 它靠 `.phone-shell` / `.spec-shell` 两种容器和 `<span class="frame-tag">` 识别每一屏——如果你的 mockup 用别的 class，改 `shots.py` 里的常量或把稿件改成这套约定。
- 两个 skill 里的「踩坑实录」保留了匿名化的真实案例（比如某项目的颜色常量名和实际色值不符）。这些是**教训**不是配置，照着理解思路即可，你自己项目的坑记进配置文件第 5 节。

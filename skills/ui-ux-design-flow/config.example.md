# ui-ux-design-flow 项目配置模板

复制到 **你的项目根目录** 下的 `.claude/ui-ux-design-flow.config.md`，或者直接开始做设计稿——
skill 第 0 步发现配置不存在，会拿下面的问题问你并自动生成。

**只有 A 组 4 项必须回答**，B 组全部可以留空走默认值。留空不影响开工，
skill 真正用到某项时会单独问你，绝不自己瞎猜。

---

## A. 必答 4 项

没有这几项，第二步「代码对齐」就做不了——设计稿只能照需求文档的文字瞎编，
而这正是本工作流要杜绝的头号问题。

- **代码本地路径**：`{{CODE_LOCAL_PATH}}`
  <!-- 例：~/work/your-app。skill 会直接读这里的文件。必须是已经 clone 到本机的目录。 -->

- **页面代码目录**：`{{PAGE_DIR}}`
  <!-- 例：lib/features/<模块>/presentation/，组件在其 widgets/ 下。
       相对上面那个路径填。不确定就先随便给个大致目录，skill 会自己往下找。 -->

- **文案来源**：`{{COPY_SOURCE}}`
  <!-- 例：lib/l10n/app_localizations_en.dart，或 src/locales/zh.json。
       设计稿里的每一句文案都从这里取，不许自己编。 -->

- **配色/主题来源**：`{{THEME_SOURCE}}`
  <!-- 例：lib/core/theme/colors.dart，或 tailwind.config.js。 -->

---

## B. 选填 10 项（留空即用默认值）

- **项目/App 名称**：`{{PROJECT_NAME}}`
  <!-- 默认：取项目文件夹名。只影响设计稿标题和文件命名。 -->

- **技术栈**：`{{STACK}}`
  <!-- 默认：从代码里自动判断（有 pubspec.yaml 就是 Flutter，package.json 里有 react-native 就是 RN……）。
       影响调 ui-ux-pro-max 时传哪个 --stack。 -->

- **产品形态**：`{{PLATFORM}}`
  <!-- 默认：iOS + Android 双端 App。决定画多宽的手机框、要不要考虑响应式。 -->

- **代码仓库地址**：`{{CODE_REPO}}`
  <!-- 默认：从本地路径的 git remote 自动读。只在需要给别人贴链接时用得上。 -->

- **分支约定**：`{{BRANCHES}}`
  <!-- 默认：main = 线上生产，其余分支视为开发中。
       只有在需要区分「线上现状 vs 即将上线」时才重要。 -->

- **需求文档位置**：`{{PRD_LOCATION}}`
  <!-- 默认：开工时直接问你要，或让你把文档贴进对话。第一步靠它推导页面清单。 -->

- **设计稿输出目录**：`{{MOCKUP_DIR}}`
  <!-- 默认：docs/design/。整合稿和拆分后的单页都放这儿。 -->

- **决策日志路径**：`{{DECISION_LOG}}`
  <!-- 默认：<设计稿输出目录>/.decision-log.md。
       需求文档与代码矛盾、skill 建议与现有设计冲突，都记这里交你裁定。 -->

- **截图 skill 名**：`{{SHOTS_SKILL}}`
  <!-- 默认：ui-mockup-shots（本仓库自带）。第四步靠它逐屏出 PNG 肉眼核验。 -->

- **手机框 CSS class**：`{{SHELL_CLASS}}`
  <!-- 默认：.phone-shell（真实页面）/ .spec-shell（规格图）。改了要同步改 shots.py。 -->

---

## C. 本项目踩过的坑（初始为空，用一次记一条）

> 这一节是给**未来的自己**看的，不用一开始填。
> 每次发现「代码里的命名骗了你」「需求文档和实现不一致」这类问题，就补一条。
> 真实案例长这样：
> - 某项目 `AppColors.mint` 的实际色值是紫色 `#845EC9`，是早期改版遗留的命名 —— 读代码不能按常量名猜颜色。
> - 某项目文案方法名叫 `...PassportTitle`，取出来的字符串却是 `Diary $name` —— 方法名和内容对不上。

{{GOTCHAS}}

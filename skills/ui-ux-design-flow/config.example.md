# ui-ux-design-flow 项目配置模板

把本文件复制到 **你的项目根目录** 下的 `.claude/ui-ux-design-flow.config.md`，逐项填写。
skill 第 0 步会读它；不存在时会拿下面这些问题问你，答完自动生成。

填不出来的项写 `未配置` —— skill 用到时会单独问你，不会自己瞎猜。

---

## 1. 项目基本信息

- **项目/App 名称**：`{{PROJECT_NAME}}`
  <!-- 例：MyApp。用于设计稿标题、文件命名。 -->

- **技术栈**：`{{STACK}}`
  <!-- 例：Flutter / React Native / SwiftUI / Next.js。决定去哪找组件、调 ui-ux-pro-max 时传哪个 --stack。 -->

- **产品形态**：`{{PLATFORM}}`
  <!-- 例：iOS+Android 双端 App / 移动端 H5 / 桌面 Web。决定画多宽的手机框、要不要考虑响应式。 -->

## 2. 代码在哪（第二步「代码对齐」全靠这些）

- **代码仓库**：`{{CODE_REPO}}`
  <!-- 例：https://github.com/you/your-app.git。设计稿必须对着真实实现画，没有这个第二步就做不了。 -->

- **本地 clone 路径**：`{{CODE_LOCAL_PATH}}`
  <!-- 例：~/work/your-app。skill 会直接读这里的文件。 -->

- **分支约定**：`{{BRANCHES}}`
  <!-- 例：main = 线上生产，dev = 在做的新版本。用于区分「线上现状」和「即将上线」。 -->

- **页面代码目录**：`{{PAGE_DIR}}`
  <!-- 例：lib/features/<模块>/presentation/，组件在其 widgets/ 下。 -->

- **文案来源**：`{{COPY_SOURCE}}`
  <!-- 例：lib/l10n/app_localizations_en.dart。文案一律从这里取，不要自己编。 -->

- **配色/主题来源**：`{{THEME_SOURCE}}`
  <!-- 例：lib/core/theme/colors.dart。 -->

## 3. 产出放哪

- **设计稿输出目录**：`{{MOCKUP_DIR}}`
  <!-- 例：docs/design/<版本号>/。整合稿和拆分后的单页都放这儿。 -->

- **决策日志路径**：`{{DECISION_LOG}}`
  <!-- 例：docs/design/.decision-log.md。PRD 与代码矛盾、skill 建议与现有设计冲突，都记在这里交用户裁定。 -->

- **需求文档位置**：`{{PRD_LOCATION}}`
  <!-- 例：docs/prd/。第一步要通读它来推导页面清单。 -->

## 4. 截图核验

- **截图 skill 名**：`{{SHOTS_SKILL}}`
  <!-- 默认 ui-mockup-shots（本仓库自带）。第四步靠它逐屏出 PNG 肉眼核验。 -->

- **手机框 CSS class**：`{{SHELL_CLASS}}`
  <!-- 默认 .phone-shell（真实页面）/ .spec-shell（规格图）。改了要同步改 shots.py。 -->

## 5. 本项目踩过的坑（用一次记一条，初始可为空）

> 这一节是给**未来的自己**看的。每次发现「代码里的命名骗了你」「PRD 和实现不一致」这类问题，就补一条。
> 真实案例长这样：
> - 某项目 `AppColors.mint` 的值其实是紫色 `#845EC9`，是早期改版遗留的命名 —— 读代码不能按常量名猜颜色。
> - 某项目文案方法名叫 `...PassportTitle`，实际字符串却是 `Diary $name` —— 方法名和文案内容对不上。

{{GOTCHAS}}

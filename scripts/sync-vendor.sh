#!/usr/bin/env bash
# 把 vendor-skills/ 下的三个第三方 skill 同步到各自上游 main 的最新版。
# 跑完记得按打印出的 commit 号更新 NOTICE.md 的表格。
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR="$REPO/vendor-skills"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# 目录名|上游仓库|skill 在上游仓库里的路径|上游 LICENSE 相对仓库根的路径（空=已随 skill 目录分发）
SOURCES=(
  "ui-ux-pro-max|git@github.com:nextlevelbuilder/ui-ux-pro-max-skill.git|.claude/skills/ui-ux-pro-max|LICENSE"
  "make-interfaces-feel-better|git@github.com:jakubkrehel/make-interfaces-feel-better.git|skills/make-interfaces-feel-better|LICENSE"
  "frontend-design|git@github.com:anthropics/skills.git|skills/frontend-design|"
)

printf '%-32s %-42s %s\n' "SKILL" "COMMIT" "DATE"
for entry in "${SOURCES[@]}"; do
  IFS='|' read -r name url path license <<< "$entry"

  git clone --quiet --depth 1 "$url" "$TMP/$name"

  src="$TMP/$name/$path"
  [ -d "$src" ] || { echo "错误：上游 $url 里找不到 $path，目录结构可能变了" >&2; exit 1; }

  # --delete：上游删掉的文件本地也要删，避免旧版遗留
  rsync -a --delete "$src/" "$VENDOR/$name/"
  [ -n "$license" ] && cp "$TMP/$name/$license" "$VENDOR/$name/"

  find "$VENDOR/$name" -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

  printf '%-32s %-42s %s\n' \
    "$name" \
    "$(git -C "$TMP/$name" rev-parse --short HEAD)" \
    "$(git -C "$TMP/$name" log -1 --format=%ad --date=short)"
done

echo
echo "同步完成。下一步："
echo "  1. 按上面的 commit 号更新 NOTICE.md 的表格和同步日期"
echo "  2. git -C \"$REPO\" diff --stat  确认改动范围"
echo "  3. 上游若有破坏性改动，检查 skills/ui-ux-design-flow/SKILL.md 里对它们的描述是否还准"

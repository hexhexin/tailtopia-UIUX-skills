#!/usr/bin/env python3
"""TailTopia 整合 UI 稿逐屏截图器。

把 ui-*-integrated-*.html 这类"一页里排了 N 个手机框"的整合稿，
拆成一屏一张 PNG，供逐屏肉眼核验（布局崩没崩、SVG 画对没画对、
有没有把说明文字混进手机框里）。

用法：
    python3 shots.py <稿件.html>                  # 全量
    python3 shots.py <稿件.html> A7 P4            # 只截指定屏
    python3 shots.py <稿件.html> --list           # 只列屏号，不截图
    python3 shots.py <稿件.html> --sheet          # 额外拼一张缩略图总览
    python3 shots.py <稿件.html> -o /tmp/out      # 指定输出目录

默认输出到 <稿件同级>/.shots/（已在 .gitignore 忽略）。
"""
import argparse
import os
import re
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# 手机框 384×812 + 外边距；spec 规格图更高，给足空间避免底部被裁。
WIN_W, WIN_H = 412, 900
DIV_TOK = re.compile(r"<div\b|</div>")


def slice_div(src: str, start: int) -> int:
    """从 start 处的 <div 起按嵌套深度配对，返回闭合 </div> 的结束位置。

    不要用非贪婪正则 `<div class="phone-shell">.*?</div></div>` 取整块——
    屏内任何一处相邻的 `</div></div>` 都会让它提前截断，症状是截图一片空白。
    """
    depth = 0
    for m in DIV_TOK.finditer(src, start):
        depth += 1 if m.group(0).startswith("<div") else -1
        if depth == 0:
            return m.end()
    raise ValueError(f"div 未闭合，起始偏移 {start}")


def extract(src_html: str):
    """→ [(屏号, 该屏完整 HTML 片段)]，同时支持 .phone-shell 与 .spec-shell。"""
    style = re.search(r"<style>(.*?)</style>", src_html, re.S)
    defs = re.search(r'(<svg style="display:none".*?</svg>)', src_html, re.S)
    if not style:
        sys.exit("找不到 <style> 块，这不像是整合 UI 稿")
    style, defs = style.group(1), (defs.group(1) if defs else "")

    out = []
    tags = list(re.finditer(r'<span class="frame-tag">(.*?)</span>', src_html, re.S))
    for k, m in enumerate(tags):
        label = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        name = re.sub(r"[^A-Za-z0-9]", "", re.split(r"\s*·\s*", label)[0])
        stop = tags[k + 1].start() if k + 1 < len(tags) else len(src_html)
        pos = -1
        for cls in ('<div class="phone-shell">', '<div class="spec-shell">'):
            pos = src_html.find(cls, m.end(), stop)
            if pos >= 0:
                break
        if pos < 0:
            print(f"  ! {name} 没找到 phone-shell / spec-shell，跳过")
            continue
        frag = src_html[pos:slice_div(src_html, pos)]
        page = (
            '<!doctype html><html><head><meta charset="utf-8"><style>'
            + style
            + "\nbody{background:#FAF9FC;margin:0;padding:14px;display:flex}"
            + "</style></head><body>" + defs + frag + "</body></html>"
        )
        out.append((name, label, page))
    return out


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("html")
    ap.add_argument("screens", nargs="*", help="屏号，如 A7 P4；留空=全部")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--sheet", action="store_true", help="额外拼一张总览图")
    a = ap.parse_args()

    src = os.path.abspath(a.html)
    out = os.path.abspath(a.out) if a.out else os.path.join(os.path.dirname(src), ".shots")
    os.makedirs(out, exist_ok=True)
    screens = extract(open(src, encoding="utf-8").read())

    if a.list:
        for n, label, _ in screens:
            print(f"  {n:6} {label}")
        return

    if not os.path.exists(CHROME):
        sys.exit(f"找不到 Chrome：{CHROME}")

    want = set(a.screens) or None
    done = []
    for name, label, page in screens:
        if want and name not in want:
            continue
        f = os.path.join(out, f"{name}.html")
        png = os.path.join(out, f"{name}.png")
        open(f, "w", encoding="utf-8").write(page)
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=2", f"--window-size={WIN_W},{WIN_H}",
             f"--screenshot={png}", f"file://{f}"],
            capture_output=True, timeout=120,
        )
        ok = os.path.exists(png)
        done.append((name, png, ok))
        print(f"  {name:6} {'✓' if ok else '✗'} {label[:44]}")

    if not done:
        sys.exit("没有匹配到任何屏，用 --list 看有哪些屏号")
    print(f"\n→ {out}")

    if a.sheet:
        try:
            from PIL import Image
        except ImportError:
            print("! 需要 Pillow 才能拼总览图：pip install Pillow")
            return
        ims = [Image.open(p) for _, p, ok in done if ok]
        w, h = ims[0].size
        tw, th = int(w * 0.38), int(h * 0.38)
        cols = min(7, len(ims))
        rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw, rows * th), "white")
        for k, im in enumerate(ims):
            sheet.paste(im.resize((tw, th)), ((k % cols) * tw, (k // cols) * th))
        sp = os.path.join(out, "_sheet.png")
        sheet.save(sp)
        print(f"→ {sp}")


if __name__ == "__main__":
    main()

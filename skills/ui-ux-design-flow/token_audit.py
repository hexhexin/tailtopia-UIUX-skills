"""整合稿 design token 核对：列出稿子里用到的字号 / 行高 / 间距，标出不在项目 token 表里的值。

用法（在项目根目录执行）：
    python3 .claude/skills/ui-ux-design-flow/token_audit.py <稿件.html> [--config .claude/ui-ux-design-flow.config.md]

token 表从配置文件里这样一行注释读取：
    <!-- tokens: font-size=9,10,...; line-height=1,1.2,...; space=0,2,4,... -->

这是「对比」不是「评判」：脚本只告诉你稿子里一共用了几种值、哪些不在 token 表里、出现在哪几屏。
不在表里的值不一定错（代码里也有写死的页面），但每一个都要能在代码里找到出处。
另外检查：稿子是否依赖在线字体（离线截图会退回系统字体，行高不可信）。
"""
import argparse
import re
import sys
from collections import defaultdict

PROPS = {
    'font-size': 'font-size',
    'line-height': 'line-height',
    'margin': 'space', 'margin-top': 'space', 'margin-bottom': 'space',
    'margin-left': 'space', 'margin-right': 'space',
    'padding': 'space', 'padding-top': 'space', 'padding-bottom': 'space',
    'padding-left': 'space', 'padding-right': 'space',
    'gap': 'space', 'row-gap': 'space', 'column-gap': 'space',
}


def load_tokens(config_path):
    text = open(config_path, encoding='utf-8').read()
    m = re.search(r'<!--\s*tokens:(.*?)-->', text)
    if not m:
        sys.exit(f'配置文件里没有 "<!-- tokens: ... -->" 行：{config_path}')
    tokens = {}
    for part in m.group(1).split(';'):
        if '=' in part:
            k, v = part.split('=', 1)
            tokens[k.strip()] = {float(x) for x in v.split(',') if x.strip()}
    return tokens


def numbers(prop, value):
    """把一个声明值拆成数字；line-height 只认无单位倍数，其余只认 px。"""
    if prop == 'line-height':
        return [float(x) for x in re.findall(r'(?<![\d.])(\d*\.?\d+)(?![\d.]*(?:px|%|em|rem))', value)]
    return [float(x) for x in re.findall(r'(-?\d*\.?\d+)px', value)]


def screen_of(html, pos, tags):
    """位置 pos 属于哪一屏（取之前最近的 frame-tag）；在 <style> 里则返回选择器。"""
    best = None
    for p, name in tags:
        if p <= pos:
            best = name
        else:
            break
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('deck')
    ap.add_argument('--config', default='.claude/ui-ux-design-flow.config.md')
    ap.add_argument('--top', type=int, default=4, help='每个值最多列几处出处')
    a = ap.parse_args()

    tokens = load_tokens(a.config)
    html = open(a.deck, encoding='utf-8').read()
    tags = [(m.start(), m.group(1).split('·')[0].strip())
            for m in re.finditer(r'class="frame-tag">([^<]*)', html)]

    used = defaultdict(lambda: defaultdict(set))  # kind -> value -> {出处}

    # 只核手机框内：先切出每个 .phone-shell 的范围（按 div 嵌套配对），框外的说明区 / 流程条不算
    spans = []
    for m in re.finditer(r'<div class="phone-shell"', html):
        depth, i = 0, m.start()
        for t in re.finditer(r'<div\b|</div>', html[m.start():]):
            depth += 1 if t.group(0) != '</div>' else -1
            if depth == 0:
                spans.append((m.start(), m.start() + t.end()))
                break
    inside = lambda pos: any(a <= pos < b for a, b in spans)
    cls_in, cls_out = set(), set()
    for m in re.finditer(r'class="([^"]*)"', html):
        (cls_in if inside(m.start()) else cls_out).update(m.group(1).split())
    chrome = cls_out - cls_in
    ICON = {'ms'}  # 图标字号不是文字字号

    # <style> 块：出处 = 选择器
    for sm in re.finditer(r'<style>(.*?)</style>', html, flags=re.S):
        for rule in re.finditer(r'([^{}]+)\{([^{}]*)\}', sm.group(1)):
            sel = rule.group(1).strip().split(',')[0][-40:]
            sel_cls = set(re.findall(r'\.([A-Za-z0-9_-]+)', rule.group(1)))
            if not (sel_cls & cls_in) or (sel_cls & chrome) or (sel_cls & ICON):
                continue
            for decl in rule.group(2).split(';'):
                if ':' not in decl:
                    continue
                prop, val = [x.strip() for x in decl.split(':', 1)]
                kind = PROPS.get(prop)
                if kind:
                    for n in numbers(prop, val):
                        used[kind][abs(n)].add(sel)

    # 行内 style：出处 = 屏号
    for im in re.finditer(r'style="([^"]*)"', html):
        if not inside(im.start()):
            continue
        tag_start = html.rfind('<', 0, im.start())
        if re.search(r'class="[^"]*\bms\b', html[tag_start:im.start()]):
            continue
        where = screen_of(html, im.start(), tags) or '(页头)'
        for decl in im.group(1).split(';'):
            if ':' not in decl:
                continue
            prop, val = [x.strip() for x in decl.split(':', 1)]
            kind = PROPS.get(prop)
            if kind:
                for n in numbers(prop, val):
                    used[kind][abs(n)].add(where)

    bad_total = 0
    for kind in ('font-size', 'line-height', 'space'):
        vals = used.get(kind, {})
        allowed = tokens.get(kind, set())
        off = {v: w for v, w in vals.items() if v not in allowed}
        bad_total += len(off)
        print(f'\n## {kind}：共 {len(vals)} 种值，{len(off)} 种不在 token 表里')
        print('   在表里：' + ', '.join(f'{v:g}' for v in sorted(v for v in vals if v in allowed)))
        for v in sorted(off):
            where = sorted(off[v])
            more = f' 等 {len(where)} 处' if len(where) > a.top else ''
            print(f'   ✗ {v:g}  ← ' + ' / '.join(where[:a.top]) + more)

    if 'fonts.googleapis.com' in html and '@font-face' not in html:
        print('\n⚠️ 稿子依赖在线字体（Google Fonts）且没有内嵌 @font-face：离线截图会退回系统字体，行高、换行不可信。')

    print(f'\n合计 {bad_total} 种值不在 token 表里。每一种都要能在代码里找到出处（写进该屏 frame-cap），找不到就改成 token。')


if __name__ == '__main__':
    main()

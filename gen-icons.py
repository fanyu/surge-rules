#!/usr/bin/env python3
"""从一张映射表生成全部图标集到 icons/。改 ICONS 一行即可增删。

依赖: rsvg-convert (brew install librsvg), Pillow
"""
import json, os, subprocess, tempfile, urllib.request
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
LUCIDE = "https://cdn.jsdelivr.net/npm/lucide-static@latest/icons/{}.svg"
SIMPLE = "https://cdn.simpleicons.org/{}"          # 自带官方品牌色
SIMPLE_RAW = "https://cdn.jsdelivr.net/npm/simple-icons@13/icons/{}.svg"

# 名字 -> (线条版 lucide slug, 彩色版来源, 通用图标配色)
#   彩色版来源: ("si", slug) 用官方品牌色 / None 表示沿用线条版并上色
ICONS = {
    "proxy":              ("shield-check",  None,               "#0A84FF"),
    "oracle":             ("database",      ("si", "oracle"),   "#F80000"),
    "ai":                 ("brain-circuit", None,               "#AF52DE"),
    "aiproxy":            ("bot",           None,               "#BF5AF2"),
    "apple":              ("apple",         ("si", "apple"),    "#000000"),
    "apple_intelligence": ("sparkles",      None,               "#FF375F"),
    "brokers":            ("trending-up",   None,               "#34C759"),
    "microsoft":          ("layout-grid",   "MSGRID",           "#00A4EF"),
    "github":             ("github",        ("si", "github"),   None),
    "twitter":            ("twitter",       ("si", "x"),        None),
    "youtube":            ("youtube",       ("si", "youtube"),  None),
    "telegram":           ("send",          ("si", "telegram"), None),
    "spotify":            ("music",         ("si", "spotify"),  None),
    "adblock":            ("ban",           ("si", "adblock"),  None),
    "home":               ("house",         None,               "#FF9500"),
    "tailscale":          ("network",       None,               "#5E5CE6"),
    "line-a":             ("link",          None,               "#5856D6"),
    "line-b":             ("globe",         None,               "#32ADE6"),
    "figma":              ("figma",         ("si", "figma"),    None),
    "cf-worker":          ("cloud",         ("si", "cloudflare"), None),
}

S, PAD, RADIUS = 400, 58, 88


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
    return urllib.request.urlopen(req, timeout=30).read().decode()


def svg_to_png(svg, path):
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as f:
        f.write(svg)
        tmp = f.name
    subprocess.run(["rsvg-convert", "-w", str(S), "-h", str(S), "-o", path, tmp], check=True)
    os.unlink(tmp)


def microsoft_squares(path):
    """Simple Icons 因商标要求下架了微软图标，按官方四色手绘。"""
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for x, y, c in [(40, 40, "#F25022"), (210, 40, "#7FBA00"),
                    (40, 210, "#00A4EF"), (210, 210, "#FFB900")]:
        d.rectangle([x, y, x + 150, y + 150], fill=c)
    im.save(path)


def card(src, dst, bg):
    g = Image.open(src).convert("RGBA")
    c = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle([0, 0, S - 1, S - 1], radius=RADIUS, fill=bg)
    g = g.resize((S - 2 * PAD, S - 2 * PAD), Image.LANCZOS)
    c.paste(g, (PAD, PAD), g)
    c.save(dst)


def build_line(name, slug, stroke_width):
    s = fetch(LUCIDE.format(slug))
    return (s.replace('stroke="currentColor"', 'stroke="#000000"')
             .replace('stroke-width="2"', f'stroke-width="{stroke_width}"'))


def main():
    dirs = {k: os.path.join(ROOT, "icons", k) for k in
            ("lucide", "lucide-card", "lucide-thin", "lucide-thin-card",
             "lucide-color", "lucide-color-card")}
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)

    for name, (slug, color_src, tint) in ICONS.items():
        # lucide: 品牌用 Simple Icons 实心 logo（涂黑），通用图标用 Lucide 线条
        is_brand = isinstance(color_src, tuple)
        if is_brand:
            s = fetch(SIMPLE_RAW.format(color_src[1]))
            s = s.replace('fill="currentColor"', 'fill="#000000"')
            if "fill=" not in s.split(">")[0]:
                s = s.replace("<svg", '<svg fill="#000000"', 1)
            svg_to_png(s, f"{dirs['lucide']}/{name}.png")
        else:
            svg_to_png(build_line(name, slug, 2), f"{dirs['lucide']}/{name}.png")
        # lucide-thin: 全部走 Lucide 线条，笔画 1.25，避免实心块与细线混排
        svg_to_png(build_line(name, slug, 1.25), f"{dirs['lucide-thin']}/{name}.png")

        # 彩色版
        out = f"{dirs['lucide-color']}/{name}.png"
        if color_src == "MSGRID":
            microsoft_squares(out)
        elif color_src:
            try:
                svg_to_png(fetch(SIMPLE.format(color_src[1])), out)
            except Exception:                       # cdn.simpleicons.org 偶有缺项
                s = fetch(SIMPLE_RAW.format(color_src[1]))
                s = s.replace("<svg", f'<svg fill="{tint or "#000000"}"', 1)
                svg_to_png(s, out)
        else:
            svg_to_png(build_line(name, slug, 2).replace('stroke="#000000"', f'stroke="{tint}"'), out)

        card(f"{dirs['lucide']}/{name}.png",       f"{dirs['lucide-card']}/{name}.png",       (244, 244, 246, 255))
        card(f"{dirs['lucide-thin']}/{name}.png",  f"{dirs['lucide-thin-card']}/{name}.png",  (244, 244, 246, 255))
        card(f"{dirs['lucide-color']}/{name}.png", f"{dirs['lucide-color-card']}/{name}.png", (255, 255, 255, 255))
        print(f"  {name}")

    print(f"{len(ICONS)} 个图标 × 6 套")


if __name__ == "__main__":
    main()

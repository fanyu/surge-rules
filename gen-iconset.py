#!/usr/bin/env python3
"""从 icons/<set>/ 生成 Surge 自定义图标集清单 (iconset/<set>.json)。"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://raw.githubusercontent.com/fanyu/surge-rules/main/icons"
SETS = {
    "lucide":            "线条 · 纯黑",
    "lucide-card":       "线条 · 浅底圆角",
    "lucide-thin":       "细线条 · 纯黑",
    "lucide-thin-card":  "细线条 · 浅底圆角",
    "lucide-color":      "彩色 · 透明底",
    "lucide-color-card": "彩色 · 白底圆角",
}
LABEL = {"aiproxy":"AI Proxy","siri":"Siri","proxy":"Proxy","oracle":"Oracle","ai":"AI","apple":"Apple",
         "apple_intelligence":"Apple Intelligence","brokers":"Brokers",
         "microsoft":"Microsoft","github":"GitHub","twitter":"Twitter",
         "youtube":"YouTube","telegram":"Telegram","spotify":"Spotify",
         "adblock":"AdBlock","home":"Home","tailscale":"Tailscale",
         "line-a":"Link","line-b":"Globe","figma":"Figma","cf-worker":"Cloudflare"}

def entries(s, prefix=""):
    d = os.path.join(ROOT, "icons", s)
    return [{"name": prefix + LABEL.get(f[:-4], f[:-4]), "url": f"{BASE}/{s}/{f}"}
            for f in sorted(os.listdir(d)) if f.endswith(".png")]

out = os.path.join(ROOT, "iconset")
os.makedirs(out, exist_ok=True)
for s, desc in SETS.items():
    m = {"name": f"fanyu · {s}", "description": desc, "icons": entries(s)}
    json.dump(m, open(f"{out}/{s}.json", "w"), ensure_ascii=False, indent=1)
    print(f"{s}.json  {len(m['icons'])}")

# 全部合一，名字带前缀，用来在 Surge 里横向挑
allm = {"name": "fanyu · 全部", "description": "六套合一，前缀区分",
        "icons": [e for s in SETS for e in entries(s, f"{s.replace('lucide','L')} · ")]}
json.dump(allm, open(f"{out}/all.json", "w"), ensure_ascii=False, indent=1)
print(f"all.json  {len(allm['icons'])}")

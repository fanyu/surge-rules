#!/usr/bin/env python3
"""切换 Surge 配置里的策略组图标：./switch-icons.py <图标集|default|sf> [配置文件]

按策略组名映射，不按原 icon-url 的写法匹配 —— 之前的正则版本
在配置改成 SF:: 或策略组改名后就失效了。
只改本来就有 icon-url 的组；没有的保持没有。
"""
import os, re, sys, time

SETS = ["lucide", "lucide-card", "lucide-thin", "lucide-thin-card",
        "lucide-color", "lucide-color-card", "default", "sf"]
BASE = "https://raw.githubusercontent.com/fanyu/surge-rules/main/icons"

# 策略组名(去掉 emoji、小写) -> 仓库里的图标文件名
NAME2ICON = {
    "proxy": "proxy", "oracle": "oracle", "home": "home", "ai": "ai",
    "siriai": "siri", "siri": "siri", "appleai": "siri",
    "apple": "apple", "brokers": "brokers", "microsoft": "microsoft",
    "github": "github", "figma": "figma", "twitter": "twitter",
    "youtube": "youtube", "telegram": "telegram", "spotify": "spotify",
    "aiproxy": "aiproxy", "shadowsocks": "line-a", "adblock": "adblock",
    "cf-worker": "cf-worker", "tailnet": "tailscale",
}

# sf 模式用的系统符号，跟随明暗自动变色，不用托管
NAME2SF = {
    "proxy": "waveform", "oracle": "capsule", "home": "homekit",
    "ai": "sparkles", "siriai": "lasso.and.sparkles", "siri": "lasso.and.sparkles",
    "appleai": "lasso.and.sparkles", "apple": "apple.logo",
    "brokers": "arrow.uturn.up.square", "aiproxy": "carbon.monoxide.cloud",
}


def norm(name):
    """🇯🇵AIProxy -> aiproxy"""
    return re.sub(r"[^\w.-]", "", name).lower()


def main():
    argv = [a for a in sys.argv[1:] if a != "--bust"]
    # 图标内容变了但文件名没变时，Surge 可能还在用本地缓存。
    # 加个时间戳查询串换掉 URL，强制它重新下载。
    bust = f"?t={int(time.time())}" if "--bust" in sys.argv else ""
    if not argv or argv[0] not in SETS:
        sys.exit(f"用法: {sys.argv[0]} <{'|'.join(SETS)}> [conf] [--bust]")
    s = argv[0]
    conf = argv[1] if len(argv) > 1 else os.path.expanduser(
        "~/Library/Mobile Documents/iCloud~com~nssurge~inc/Documents/Surge-optimized.conf")
    sub = "" if s == "default" else f"{s}/"

    lines = open(conf, encoding="utf-8").read().split("\n")
    section, n = "", 0
    for i, line in enumerate(lines):
        if line.startswith("["):
            section = line
            continue
        if section != "[Proxy Group]" or "icon-url" not in line or "=" not in line:
            continue
        key = norm(line.split("=", 1)[0])
        if s == "sf":
            new = f"SF::{NAME2SF[key]}" if key in NAME2SF else None
        else:
            new = f"{BASE}/{sub}{NAME2ICON[key]}.png{bust}" if key in NAME2ICON else None
        if new is None:
            continue
        lines[i] = re.sub(r"icon-url ?= ?\"?[^,\"]+\"?", f"icon-url={new}", line)
        n += 1

    open(conf, "w", encoding="utf-8").write("\n".join(lines))
    print(f"{n} 个策略组 -> {s}")


if __name__ == "__main__":
    main()

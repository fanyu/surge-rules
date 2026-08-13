#!/bin/zsh
# 切换 Surge 配置里的图标集：./switch-icons.sh <图标集目录名|default> [配置文件]
set -e
SETS=(lucide lucide-card lucide-thin lucide-thin-card lucide-color lucide-color-card default)
SET="${1:?用法: $0 <${(j:|:)SETS}> [conf]}"
(($SETS[(Ie)$SET])) || { echo "未知图标集: $SET (可选: ${(j:, :)SETS})" >&2; exit 1; }
CONF="${2:-$HOME/Library/Mobile Documents/iCloud~com~nssurge~inc/Documents/Surge-optimized.conf}"
BASE="https://raw.githubusercontent.com/fanyu/surge-rules/main/icons"
[[ "$SET" == "default" ]] && DIR="" || DIR="$SET/"

# 外链和内置图标先归一到本仓库，之后才能统一切换。
# 只动这里点名的几个；其余 B1:: 内置图标是手动设的，保持原样。
perl -pi -e "s{icon-url=https://static\.figma\.com/[^,\s]+}{icon-url=$BASE/figma.png};
             s{icon-url=https://www\.apple\.com/[^,\s]+}{icon-url=$BASE/apple_intelligence.png};
             s{icon-url ?= ?\"B1::Household::Smart Home\"}{icon-url=$BASE/home.png};
             s{icon-url ?= ?\"?B1::Logos::Apple Music Lyrics\"?}{icon-url=$BASE/apple_intelligence.png};
             s{^(\N*AIProxy = (?:(?!icon-url)\N)*)\$}{\$1, icon-url=$BASE/aiproxy.png};
             s{\Q$BASE\E/(?:[\w-]+/)?([\w.-]+\.png)}{$BASE/$DIR\$1}g" "$CONF"
grep -c "$BASE/$DIR" "$CONF"

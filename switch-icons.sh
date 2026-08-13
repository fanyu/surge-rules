#!/bin/zsh
# 切换 Surge 配置里的图标集：./switch-icons.sh <图标集目录名|default> [配置文件]
set -e
SETS=(lucide lucide-card lucide-color lucide-color-card default)
SET="${1:?用法: $0 <${(j:|:)SETS}> [conf]}"
(($SETS[(Ie)$SET])) || { echo "未知图标集: $SET (可选: ${(j:, :)SETS})" >&2; exit 1; }
CONF="${2:-$HOME/Library/Mobile Documents/iCloud~com~nssurge~inc/Documents/Surge-optimized.conf}"
BASE="https://raw.githubusercontent.com/fanyu/surge-rules/main/icons"
[[ "$SET" == "default" ]] && DIR="" || DIR="$SET/"

# 外链图标先归一到本仓库，之后才能统一切换
perl -pi -e "s{icon-url=https://static\.figma\.com/[^,\s]+}{icon-url=$BASE/figma.png};
             s{icon-url=https://www\.apple\.com/[^,\s]+}{icon-url=$BASE/apple_intelligence.png};
             s{\Q$BASE\E/(?:[\w-]+/)?([\w.-]+\.png)}{$BASE/$DIR\$1}g" "$CONF"
grep -c "$BASE/$DIR" "$CONF"

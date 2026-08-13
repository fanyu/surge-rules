#!/bin/zsh
# 切换 Surge 配置里的图标集：./switch-icons.sh <lucide|lucide-card|default> [配置文件]
set -e
SET="${1:?用法: $0 <lucide|lucide-card|default> [conf]}"
CONF="${2:-$HOME/Library/Mobile Documents/iCloud~com~nssurge~inc/Documents/Surge-optimized.conf}"
BASE="https://raw.githubusercontent.com/fanyu/surge-rules/main/icons"
[[ "$SET" == "default" ]] && DIR="" || DIR="$SET/"

# 外链图标先归一到本仓库，之后才能统一切换
perl -pi -e "s{icon-url=https://static\.figma\.com/[^,\s]+}{icon-url=$BASE/figma.png};
             s{icon-url=https://www\.apple\.com/[^,\s]+}{icon-url=$BASE/apple_intelligence.png};
             s{\Q$BASE\E/(?:lucide-card/|lucide/)?([\w.-]+\.png)}{$BASE/$DIR\$1}g" "$CONF"
grep -c "$BASE/$DIR" "$CONF"

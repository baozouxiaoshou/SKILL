#!/bin/bash
# 用户故事分析师 Skill - 验证脚本

SKILL_NAME="user-story-analyst"
SKILL_PATH="/Users/llh_me/Documents/app/codex/agents/c-user-story-analyst"
SKILL_LINK="$HOME/.codex/skills/$SKILL_NAME"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }

echo "==========================================="
echo "  Skill 验证"
echo "==========================================="
echo ""

# 检查软链
if [ -L "$SKILL_LINK" ]; then
    TARGET=$(readlink "$SKILL_LINK")
    pass "软链存在：$SKILL_LINK -> $TARGET"
else
    fail "软链不存在：$SKILL_LINK"
    echo ""
    echo "请先运行 ./install.sh 安装"
    exit 1
fi

# 检查关键文件
echo ""
echo "📁 检查关键文件..."
for file in SKILL.md README.md README.en.md CHANGELOG.md LICENSE CONTRIBUTING.md prompts/system.md; do
    if [ -f "$SKILL_LINK/$file" ]; then
        pass "$file"
    else
        fail "$file 缺失"
    fi
done

# 检查双语版
if [ -f "$SKILL_LINK/docs/README-BILINGUAL.md" ]; then
    pass "docs/README-BILINGUAL.md（双语版）"
fi

# 检查模块
echo ""
echo "📦 检查模块..."
MODULES=(
    "templates:文档模板"
    "references:参考资料"
    "assets/checklist.md:需求评审清单"
    "assets/diagrams:可视化模板"
    "figma-plugin:Figma 插件"
    "assets/figma-bridge:Figma 集成"
    "assets/lark-bridge:飞书集成"
)
for module in "${MODULES[@]}"; do
    path="${module%%:*}"
    name="${module##*:}"
    if [ -e "$SKILL_LINK/$path" ]; then
        count=$(ls "$SKILL_LINK/$path" 2>/dev/null | wc -l | xargs)
        pass "$name ($path) - $count 个文件"
    else
        warn "$name ($path) 不存在"
    fi
done

# 检查 Python 依赖
echo ""
echo "🐍 检查 Python 脚本..."
PYTHON_SCRIPTS=(
    "assets/figma-bridge/skill_to_figma.py"
    "assets/lark-bridge/lark_webhook.py"
    "assets/lark-bridge/lark_doc_generator.py"
    "assets/lark-bridge/lark_base_sync.py"
)
for script in "${PYTHON_SCRIPTS[@]}"; do
    if [ -x "$SKILL_LINK/$script" ]; then
        pass "$script（可执行）"
    elif [ -f "$SKILL_LINK/$script" ]; then
        warn "$script（无执行权限，请运行 chmod +x）"
    else
        fail "$script 缺失"
    fi
done

# 检查 Node.js
echo ""
echo "📦 检查 Node.js 脚本..."
if [ -f "$SKILL_LINK/figma-plugin/code.js" ]; then
    pass "figma-plugin/code.js"
fi
if [ -f "$SKILL_LINK/figma-plugin/ui.html" ]; then
    pass "figma-plugin/ui.html"
fi

# 统计
echo ""
echo "📊 统计："
total_files=$(find "$SKILL_LINK" -type f 2>/dev/null | wc -l | xargs)
total_lines=$(find "$SKILL_LINK" -type f -exec cat {} \; 2>/dev/null | wc -l | xargs)
total_size=$(du -sh "$SKILL_LINK" 2>/dev/null | awk '{print $1}')
echo "  文件数: $total_files"
echo "  总行数: $total_lines"
echo "  总大小: $total_size"

echo ""
echo "==========================================="
echo "  验证完成"
echo "==========================================="

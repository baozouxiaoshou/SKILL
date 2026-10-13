#!/bin/bash
# 用户故事分析师 Skill - 一键安装脚本
#
# 使用方法：
#   chmod +x install.sh
#   ./install.sh
#
# 卸载：
#   ./install.sh --uninstall

set -e

SKILL_NAME="user-story-analyst"
SKILL_PATH="/Users/llh_me/Documents/app/codex/agents/c-user-story-analyst"
SKILL_LINK="$HOME/.codex/skills/$SKILL_NAME"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}✅${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠️${NC} $1"; }
log_err() { echo -e "${RED}❌${NC} $1"; }

# 卸载模式
if [ "$1" = "--uninstall" ]; then
    if [ -L "$SKILL_LINK" ]; then
        rm "$SKILL_LINK"
        log_info "已卸载：$SKILL_LINK"
    elif [ -d "$SKILL_LINK" ]; then
        log_warn "发现目录（非软链），跳过：$SKILL_LINK"
    else
        log_warn "Skill 未安装"
    fi
    exit 0
fi

echo "==========================================="
echo "  用户故事分析师 Skill 安装器"
echo "==========================================="
echo ""

# 1. 检查 Skill 源路径
if [ ! -d "$SKILL_PATH" ]; then
    log_err "Skill 源路径不存在：$SKILL_PATH"
    exit 1
fi
log_info "找到 Skill：$SKILL_PATH"

# 2. 创建 skills 目录
if [ ! -d "$HOME/.codex/skills" ]; then
    mkdir -p "$HOME/.codex/skills"
    log_info "创建目录：~/.codex/skills"
fi

# 3. 检查是否已安装
if [ -L "$SKILL_LINK" ]; then
    EXISTING=$(readlink "$SKILL_LINK")
    if [ "$EXISTING" = "$SKILL_PATH" ]; then
        log_info "Skill 已安装并指向正确路径"
    else
        log_warn "软链已存在但指向：$EXISTING"
        log_warn "当前 Skill 路径：$SKILL_PATH"
        echo ""
        read -p "是否替换为新路径？[y/N] " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            rm "$SKILL_LINK"
            log_info "已移除旧软链"
        else
            log_warn "已取消"
            exit 0
        fi
    fi
elif [ -d "$SKILL_LINK" ]; then
    log_err "$SKILL_LINK 是目录而非软链"
    log_err "请手动删除后重试"
    exit 1
fi

# 5. 创建软链
ln -s "$SKILL_PATH" "$SKILL_LINK"
log_info "软链已创建：$SKILL_LINK"

# 6. 验证
echo ""
echo "==========================================="
echo "  安装完成"
echo "==========================================="
echo ""
echo "📋 安装信息："
echo "  Skill 路径：$SKILL_PATH"
echo "  软链位置：$SKILL_LINK"
echo ""
echo "🔍 验证："
ls -la "$SKILL_LINK" 2>/dev/null | head -1
echo ""
echo "📁 软链内容（按目录）："
for dir in prompts templates references assets figma-plugin assets/diagrams assets/figma-bridge assets/lark-bridge; do
    if [ -d "$SKILL_LINK/$dir" ]; then
        count=$(ls "$SKILL_LINK/$dir" 2>/dev/null | wc -l | xargs)
        echo "  $dir/  ($count 项)"
    fi
done
echo ""
echo "🚀 下一步："
echo "  1. 重启 Codex（如果已运行）"
echo "  2. 在 Codex 中输入需求，自动调用 Skill"
echo ""
echo "📖 使用说明："
echo "  - System Prompt: $SKILL_LINK/prompts/system.md"
echo "  - README: $SKILL_LINK/README.md"
echo ""
echo "🗑️  卸载："
echo "  $0 --uninstall"

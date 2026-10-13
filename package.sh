#!/bin/bash
# 用户故事分析师 Skill - 打包脚本
#
# 用法：
#   ./package.sh              # 打包到 dist/
#   ./package.sh --output my-skill.zip   # 自定义输出
#   ./package.sh --no-clean   # 不清理 macOS 隐藏文件
#   ./package.sh --include-source  # 包含 .DS_Store 等
#
# 输出：
#   dist/user-story-analyst-v1.0.0.zip
#   dist/user-story-analyst-v1.0.0.zip.sha256

set -e

SKILL_NAME="user-story-analyst"
VERSION="1.0.0"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$SOURCE_DIR/dist"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认参数
OUTPUT_FILE=""
CLEAN_MACOS=true
VERBOSE=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --no-clean)
            CLEAN_MACOS=false
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "用法：./package.sh [选项]"
            echo ""
            echo "选项："
            echo "  --output FILE       自定义输出 ZIP 文件路径"
            echo "  --no-clean          不清理 macOS 隐藏文件"
            echo "  --verbose, -v       详细输出"
            echo "  --help, -h          显示帮助"
            exit 0
            ;;
        *)
            echo "未知参数：$1"
            echo "运行 ./package.sh --help 查看帮助"
            exit 1
            ;;
    esac
done

# 输出文件名
if [ -z "$OUTPUT_FILE" ]; then
    mkdir -p "$BUILD_DIR"
    OUTPUT_FILE="$BUILD_DIR/${SKILL_NAME}-v${VERSION}-${TIMESTAMP}.zip"
fi

log() {
    echo -e "${GREEN}✅${NC} $1"
}
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}
log_warn() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

echo "==========================================="
echo "  用户故事分析师 Skill - 打包"
echo "==========================================="
echo ""
log_info "源目录：$SOURCE_DIR"
log_info "输出文件：$OUTPUT_FILE"
echo ""

# 1. 检查前置
log_info "[1/6] 检查前置条件..."
if ! command -v zip > /dev/null; then
    echo "❌ 需要安装 zip 命令"
    echo "   macOS: brew install zip"
    echo "   Linux: apt install zip"
    exit 1
fi
if ! command -v shasum > /dev/null && ! command -v sha256sum > /dev/null; then
    echo "❌ 需要 sha256sum 或 shasum 命令"
    exit 1
fi
log "前置检查通过"

# 2. 创建临时打包目录
log_info "[2/6] 创建打包临时目录..."
TMP_PACKAGE=$(mktemp -d)
PACKAGE_ROOT="$TMP_PACKAGE/$SKILL_NAME"
mkdir -p "$PACKAGE_ROOT"
log "临时目录：$TMP_PACKAGE"

# 3. 复制文件
log_info "[3/6] 复制 Skill 文件..."
cd "$SOURCE_DIR"

# 使用 rsync 或 cp 复制所有文件，排除 .git
rsync -a \
    --exclude='.git' \
    --exclude='.DS_Store' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='dist' \
    --exclude='filter-out' \
    . "$PACKAGE_ROOT/" 2>/dev/null || \
cp -R . "$PACKAGE_ROOT/" 2>/dev/null

# 清理 macOS 隐藏文件
if [ "$CLEAN_MACOS" = true ]; then
    find "$PACKAGE_ROOT" -name '.DS_Store' -delete 2>/dev/null || true
    find "$PACKAGE_ROOT" -name '._*' -delete 2>/dev/null || true
    log "已清理 macOS 隐藏文件"
fi

# 4. 添加版本信息
log_info "[4/6] 添加版本信息..."
cat > "$PACKAGE_ROOT/VERSION.txt" << EOF
Skill: $SKILL_NAME
Version: $VERSION
Build Date: $(date +"%Y-%m-%d %H:%M:%S")
Source: $SOURCE_DIR
EOF
log "版本信息已写入"

# 5. 打包
log_info "[5/6] 打包 ZIP..."
cd "$TMP_PACKAGE"

if [ "$VERBOSE" = true ]; then
    zip -r "$OUTPUT_FILE" "$SKILL_NAME/"
else
    zip -r "$OUTPUT_FILE" "$SKILL_NAME/" -q
fi

ZIP_SIZE=$(du -h "$OUTPUT_FILE" | awk '{print $1}')
log "ZIP 已生成：$OUTPUT_FILE ($ZIP_SIZE)"

# 6. 计算校验和
log_info "[6/6] 计算 SHA256..."
if command -v shasum > /dev/null; then
    shasum -a 256 "$OUTPUT_FILE" | awk '{print $1}' > "$OUTPUT_FILE.sha256"
else
    sha256sum "$OUTPUT_FILE" | awk '{print $1}' > "$OUTPUT_FILE.sha256"
fi
SHA256=$(cat "$OUTPUT_FILE.sha256")
log "SHA256: ${SHA256:0:16}..."

# 清理临时目录
rm -rf "$TMP_PACKAGE"

# 输出打包报告
echo ""
echo "==========================================="
echo "  打包完成"
echo "==========================================="
echo ""

# 统计
FILE_COUNT=$(unzip -l "$OUTPUT_FILE" 2>/dev/null | tail -1 | awk '{print $2}')
LOG_LINES=$(unzip -p "$OUTPUT_FILE" "${SKILL_NAME}/CHANGELOG.md" 2>/dev/null | wc -l | xargs)

echo "📦 发布包信息："
echo "  文件名：$OUTPUT_FILE"
echo "  大小：$ZIP_SIZE"
echo "  文件数：$FILE_COUNT"
echo "  版本：v$VERSION"
echo ""
echo "🔐 校验："
echo "  SHA256: $SHA256"
echo "  校验文件：$OUTPUT_FILE.sha256"
echo ""
echo "📋 发布说明："
echo "  - 完整 Skill（36 文件 + VERSION.txt）"
echo "  - 含 CHANGELOG.md / LICENSE / CONTRIBUTING.md"
echo "  - 支持一键安装：./install.sh"
echo ""
echo "🚀 使用方式："
echo "  1. 分发 ZIP 给同事"
echo "  2. 解压：unzip user-story-analyst-v$VERSION.zip"
echo "  3. 安装：cd $SKILL_NAME && ./install.sh"
echo ""
echo "  或直接："
echo "  unzip user-story-analyst-v$VERSION.zip -d ~/.codex/skills/"
echo ""

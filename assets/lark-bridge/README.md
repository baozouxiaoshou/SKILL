# 飞书集成指南（Lark Integration）

> 把 Skill 输出自动推送到飞书工作流。

---

## 集成模块

| 模块 | 工具脚本 | 适用场景 |
|------|---------|---------|
| **飞书机器人** | `lark_webhook.py` | 群消息推送（最快）|
| **飞书文档** | `lark_doc_generator.py` | 创建结构化 PRD |
| **飞书多维表格** | `lark_base_sync.py` | Story 列表管理 |

---

## 模块 1：飞书群机器人（推荐入门）

### 配置步骤

#### Step 1：在飞书群添加机器人
1. 飞书群 → 设置 → 群机器人 → 添加机器人
2. 选择"自定义机器人"
3. 复制 Webhook URL（形如 `https://open.feishu.cn/...`）

#### Step 2：设置环境变量
```bash
export LARK_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxx"
```

或者用参数传入：
```bash
python lark_webhook.py output.md --webhook "https://..."
```

#### Step 3：使用
```bash
# 推送 Markdown（卡片格式）
python lark_webhook.py /path/to/skill_output.md

# 简单文本格式
python lark_webhook.py /path/to/skill_output.md --simple

# 预览消息（不发送）
python lark_webhook.py /path/to/skill_output.md --dry-run
```

### 消息效果
- **卡片格式**：自动识别 H1/H2/H3 标题、Mermaid 代码块、引用、列表
- **简单格式**：整段作为纯文本
- **安全签名**：可选添加 secret 校验（修改代码启用）

### 限制
- 卡片消息文本 ≤ 4000 字符（超出自动截断）
- 代码块文本 ≤ 2000 字符

---

## 模块 2：飞书文档生成器

### 配置步骤

#### Step 1：创建飞书 App
1. 访问 https://open.feishu.cn/app
2. 创建企业自建应用
3. 获取 App ID 和 App Secret

#### Step 2：配置权限
应用权限 → 开通：
- `docx:document:create` - 创建文档
- `docx:document:readonly` - 读取文档

#### Step 3：生成 API Payload
```bash
python lark_doc_generator.py skill_output.md --output doc_payload.json --show-sdk
```

输出包括：
- `doc_payload.json` - API 调用参数
- SDK 调用示例（Python）

#### Step 4：调用 API
参考官方文档：
https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/create

或使用 Python SDK：
```bash
pip install lark-oapi
```

---

## 模块 3：飞书多维表格同步

### 配置步骤

#### Step 1：在飞书创建多维表格
1. 飞书主页 → 新建 → 多维表格
2. 添加表（如 `User Story`）
3. 添加字段（按 BASE_FIELDS 定义）

#### Step 3：生成 CSV
```bash
# 生成 CSV（手动导入）
python lark_base_sync.py skill_output.md --format csv --output stories.csv

# 生成 JSON（程序化处理）
python lark_base_sync.py skill_output.md --format json --output stories.json

# 生成 API Payload（批量写入）
python lark_base_sync.py skill_output.md --format api --output base_payload.json \
  --app-token "bascnxxxxxxx" --table-id "tblxxxxxxx"
```

#### Step 4：导入到飞书
- **方式 A**：CSV → 在多维表格中导入
- **方式 B**：API → 用 `open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create`

### 字段映射

| Skill 输出 | 飞书 Base 字段 | 类型 |
|-----------|--------------|------|
| `Story ID` | Story ID | 文本 |
| `【Story XXX】标题` | 标题 | 文本 |
| `作为 [角色]` | 角色 | 文本 |
| `我想要 [想要]` | 想要 | 长文本 |
| `以便 [以便]` | 以便 | 长文本 |
| `【优先级】P0` | 优先级 | 单选 |
| `【故事点】5` | 故事点 | 数字 |
| `✅ Given... When... Then` | 验收标准 | 长文本 |

---

## 字段配置（BASE_FIELDS）

如果你创建多维表格，请按以下字段配置：

```
字段名          | 类型       | 备注
----------------|-----------|------
Story ID        | 文本       | 主键
标题             | 文本       |
角色             | 文本       |
想要             | 长文本     |
以便             | 长文本     |
优先级           | 单选       | P0/P1/P2/P3
故事点           | 数字       |
Epic            | 文本       |
状态             | 单选       | 待评审/开发中/已完成/已搁置
验收标准         | 长文本     |
备注             | 长文本     |
```

---

## 一键集成脚本

将以下内容保存为 `skill-to-lark.sh`：

```bash
#!/bin/bash
# 一键把 Skill 输出推送到飞书工作流

INPUT="$1"
WEBHOOK="${LARK_WEBHOOK_URL:-}"

if [ -z "$INPUT" ]; then
    echo "Usage: $0 <skill_output.md>"
    exit 1
fi

# 1. 推送到飞书群
if [ -n "$WEBHOOK" ]; then
    python lark_webhook.py "$INPUT" --webhook "$WEBHOOK"
fi

# 2. 生成飞书文档 Payload
python lark_doc_generator.py "$INPUT" --output lark_doc.json

# 3. 生成多维表格 CSV
python lark_base_sync.py "$INPUT" --format csv --output lark_stories.csv

echo "✅ 全部完成！"
echo "   - 飞书群消息：已推送"
echo "   - 飞书文档 Payload：lark_doc.json"
echo "   - 多维表格 CSV：lark_stories.csv"
```

---

## 完整使用示例

假设你已经运行了 Skill，输出文件是 `output.md`：

```bash
# 1. 设置 Webhook
export LARK_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"

# 2. 推送到飞书群（团队立即看到）
python3 lark_webhook.py output.md

# 3. 生成多维表格数据
python3 lark_base_sync.py output.md --format csv --output stories.csv

# 4. 手动在飞书 Base 导入 stories.csv

# 5. 生成飞书文档
python3 lark_doc_generator.py output.md --output doc_payload.json
# 然后用 API/SDK 创建文档
```

---

## 常见问题

### Q: 推送消息失败？
检查：
1. Webhook URL 是否正确
2. 网络是否能访问 `open.feishu.cn`
3. 消息长度（卡片 ≤ 30KB，文本 ≤ 4KB）

### Q: 多维表格导入失败？
检查：
1. CSV 字段名是否与飞书表格字段名一致
2. 单选字段值是否在选项内
3. 数字字段是否包含非数字字符

### Q: 飞书文档生成失败？
检查：
1. App ID / Secret 是否正确
2. 是否开通了文档权限
3. 文件夹 token 是否有效

---

## 高级用法

### 自定义消息卡片样式

编辑 `lark_webhook.py` 中的 `build_card_message()`，调整 header 颜色：

```python
"template": "blue"  # 改成 red / green / yellow / purple 等
```

### 自动定期推送

配合 cron：
```bash
# 每天上午 10 点推送今日 Story 状态
0 10 * * * cd /path/to/skill && python lark_webhook.py output.md
```

### 与 Skill 输出格式联动

在 `prompts/system.md` 中明确推荐输出格式：
- Story 用 `【优先级】P0 【故事点】3` 标注
- AC 用 `✅ Given... When... Then` 开头

---

## 后续扩展

- **审批流**：把 Story 评审作为飞书审批
- **任务联动**：Story 状态自动创建飞书任务
- **仪表盘**：从 Base 生成飞书仪表盘
- **周报自动生成**：每周自动从 Base 汇总

---

## 相关资源

- 飞书开放平台：https://open.feishu.cn/app
- 飞书机器人文档：https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot
- 飞书多维表格 API：https://open.feishu.cn/document/server-docs/docs/bitable-v1/bitable-overview
- Python SDK：https://pypi.org/project/lark-oapi/

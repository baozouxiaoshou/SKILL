# 贡献指南（Contributing Guide）

感谢你有兴趣贡献用户故事分析师 Skill！本文档会帮助你快速上手。

---

## 🎯 我们欢迎的贡献

- ✅ **新模板**：新的 Persona、Journey Map、AC 等模板
- ✅ **新方法论**：RICE、ICE、JTBD 等
- ✅ **新集成**：Notion、钉钉、企微等
- ✅ **新案例**：真实的 C 端 / B 端需求案例
- ✅ **Bug 修复**：脚本错误、文档错误
- ✅ **文档优化**：表述不清、链接失效、错别字
- ✅ **翻译**：中英双语版本

---

## 🚫 不接受的贡献

- ❌ 删除或弱化 C 端 / B 端场景适配
- ❌ 移除合规相关检查项
- ❌ 引入与项目目标无关的功能
- ❌ 不符合 MIT License 的内容
- ❌ 大规模重写（应先开 issue 讨论）

---

## 📁 项目结构

熟悉以下目录有助于你的工作：

```
user-story-analyst/
├── prompts/system.md          # 核心规则（最重要）
├── templates/                  # 文档模板
├── references/                 # 方法论 + 案例
├── assets/
│   ├── diagrams/               # Mermaid 模板
│   ├── figma-bridge/           # Figma 集成
│   └── lark-bridge/            # 飞书集成
├── SKILL.md                    # 角色定义
├── README.md                   # 使用说明
├── install.sh                  # 安装脚本
├── verify.sh                   # 验证脚本
└── package.sh                  # 打包脚本
```

---

## 🔧 开发流程

### Step 1：本地开发
```bash
# 1. 克隆仓库
git clone <repo-url>
cd user-story-analyst

# 2. 在 Codex 中安装 Skill
./install.sh

# 3. 修改文件
# ...

# 4. 测试修改
./verify.sh
```

### Step 2：提交变更

每个变更请附上：

```
<类型>(<范围>): <简短描述>

<详细描述>

关联 Issue: #xxx
```

类型：
- `feat` - 新功能
- `fix` - Bug 修复
- `docs` - 文档
- `style` - 格式（无功能变更）
- `refactor` - 重构
- `test` - 测试
- `chore` - 构建 / 工具

---

## 📋 添加新模板

如果你要新增一个模板（如 Persona B 端版）：

1. 在 `templates/` 中创建 `xxx.md`
2. 在 `prompts/system.md` 中增加触发规则
3. 在 `SKILL.md` 资源清单中增加条目
4. 在 `README.md` 中补充说明
5. 在 `CHANGELOG.md` 中记录

---

## 🧪 添加新集成

如果你要新增一个集成（如 Notion）：

1. 在 `assets/` 下创建新目录（如 `notion-bridge/`）
2. 实现 Python 转换脚本
3. 提供使用文档（`README.md`）
4. 在主 README 增加入口
5. 在 `verify.sh` 中增加检查

---

## 📝 文档规范

- 使用中文为主，关键术语保留英文
- Markdown 格式
- 代码块标注语言（```python, ```mermaid 等）
- 表格简洁清晰
- 链接使用相对路径

---

## 🐛 报告 Bug

请提供：

1. **环境**：操作系统、Codex 版本
3. **复现步骤**：详细的操作步骤
4. **期望行为**：应该发生什么
5. **实际行为**：实际发生了什么
6. **截图**：如果有

---

## 💡 提交 Feature Request

请说明：
1. **场景**：谁会用到
2. **问题**：当前痛点
3. **方案**：建议如何实现
4. **替代方案**：其他可能的实现

---

## 📞 联系方式

- Issue：<repo-url>/issues
- 讨论：<repo-url>/discussions
- 邮件：<team-email>

---

## 📜 License

提交代码即表示同意 MIT License。

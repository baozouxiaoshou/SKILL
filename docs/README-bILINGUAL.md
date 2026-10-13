# 用户故事分析师 / User Story Analyst

> **中英双语版** | **Bilingual Version**
> 
> 📖 [纯中文](README.md) | [English Only](README.en.md) | **Bilingual（本文件 / This File）**

---

## 📖 简介 / Overview

| 中文 | English |
|-------|---------|
| 一个覆盖 **C 端 + B 端轻量** 场景的需求分析 Skill。 | A requirement analysis Skill covering both **C-side** and **lightweight B-side** scenarios. |
| 你的使命：把模糊的业务诉求拆解为可执行、可测试、有价值的用户故事卡。 | Your mission: transform vague business requirements into executable, testable, valuable user story cards. |

---

## 📦 安装 / Installation

| 中文 | English |
|-------|---------|
| **一键安装（推荐）** | **Quick Install (Recommended)** |
| ```bash | ```bash |
| cd /Users/llh_me/Documents/app/codex/agents/c-user-story-analyst | cd /Users/llh_me/Documents/app/codex/agents/c-user-story-analyst |
| ./install.sh | ./install.sh |
| ``` | ``` |
| **手动安装** | **Manual Install** |
| ```bash | ```bash |
| mkdir -p ~/.codex/skills | mkdir -p ~/.codex/skills |
| ln -s /Users/llh_me/Documents/app/codex/agents/c-user-story-analyst \ | ln -s /Users/llh_me/Documents/app/codex/agents/c-user-story-analyst \ |
|       ~/.codex/skills/user-story-analyst |       ~/.codex/skills/user-story-analyst |
| ``` | ``` |
| **验证** | **Verify** |
| ```bash | ```bash |
| ./verify.sh | ./verify.sh |
| ``` | ``` |
| **卸载** | **Uninstall** |
| ```bash | ```bash |
| ./install.sh --uninstall | ./install.sh --uninstall |
| ``` | ``` |

---

## 🎯 适用场景 / Applicable Scenarios

| 中文 | English |
|-------|---------|
| 场景 | 典型输入 | 输出侧重 |
|------|---------|---------|
| **C 端产品** | 健身 App、早起打卡、社区功能 | 用户旅程、留存指标、AB 实验 |
| 轻量 B 端 | 合规填报、双语录入、内部工具、流程化系统 | 合规设计、版本快照、审计追溯 |
| 混合场景 | 跨境 C 端产品 | 体验 + 合规并重 |

| Scenario | Typical Input | Output Focus |
|----------|---------------|--------------|
| **C-side Products** | Fitness apps, habit tracking, community features | User journey, retention metrics, A/B testing |
| **Lightweight B-side** | Compliance forms, B-side entries, internal tools, workflow systems | Compliance design, version snapshots, audit trail |
| **Hybrid Scenarios** | Cross-border C-side products | Experience + compliance equally important |

---

## 🚀 快速使用 / Quick Start

| 中文 | English |
|-------|---------|
| **方式 1**：作为 Codex Skill 使用（install.sh 一键安装）| **Method 1**: Use as Codex Skill (install.sh handles this) |
| **方式 2**：直接使用 System Prompt | **Method 2**: Use System Prompt standalone |
| 读取 `prompts/system.md`，作为 ChatGPT / Claude / Cursor 等的系统提示词。 | Read `prompts/system.md` and copy it as the system prompt for ChatGPT / Claude / Cursor. |

---

## 📊 工作流 / Workflow

| 步骤 | 中文 | English |
|------|-------|---------|
| **Step 0** | 场景判断 → 自动识别 C 端 / B 端轻量 | Scenario Detection → Auto-identify C-side / B-side lightweight |
| **Step 1** | 澄清需求 → 主动提 5-8 个关键问题 | Requirement Clarification → 5-8 critical questions |
| **Step 2** | 构建 Persona → 根据场景选择画像类型 | Persona → Consumer or professional |
| **Step 3** | 绘制 Journey Map | Journey Mapping |
| **Step 4** | 拆解 Story → Epic → User Story + AC | Story Decomposition → Epic → User Story + AC |
| **Step 5** | 评估优先级 + 输出指标/实验/合规建议 | Priority + Metrics / Experiment / Compliance |

---

## ⚖️ 场景差异对照 / Scenario Comparison

| 维度 | C 端场景 | B 端轻量场景 |
|------|---------|-------------|
| 目标用户 | 普通消费者 | 专业人士 / 员工 |
| 决策链 | 极短 | 中-长 |
| 核心痛点 | 体验、便捷、情感 | 效率、合规、准确 |
| 需求来源 | 用户调研、数据、竞品 | 业务部门、规章制度、客户 |
| 周期 | 周级 | 月级 |
| **北极指标** | 留存率、活跃度 | 任务完成率、合规率、提交成功率 |
| **AC 必含** | 体验、异常、边界 | 合规、安全、审计、可追溯 |
| **Persona 关键** | 生活形态、情感 | 角色职责、专业背景、工作流 |
| **可视化重点** | 用户旅程 | 流程图 + 角色协作 |

| Dimension | C-side | B-side Lightweight |
|-----------|--------|-------------------|
| Persona Type | Consumer | Professional / Employee |
| Decision Chain | Very short | Medium-long |
| Core Pain Point | Experience, convenience, emotion | Efficiency, compliance, accuracy |
| Requirement Source | User research, data, competitors | Business units, regulations, clients |
| Cycle | Weekly | Monthly |
| **North Star** | Retention, activity | Task completion, compliance rate |
| **Must-have AC** | Experience, edge cases | Compliance, security, traceability |
| **Persona Key** | Lifestyle, emotion | Role, expertise, workflow |
| **Visualization Focus** | User journey | Process + role collaboration |

---

## 🎨 核心方法论 / Core Methodologies

| 方法 | 中文 | English |
|------|-------|---------|
| INVEST | 故事质量：独立/可协商/有价值/可估算/小/可测试 | Story quality: Independent/Negotiable/Valuable/Estimable/Small/Testable |
| Given-When-Then | 验收：前置/动作/结果 | Acceptance: Given/When/Then |
| KANO | 优先级：基本型/期望型/兴奋型/无差异型/反向型 | Priority: Must-be/One-dimensional/Attractive/Indifferent/Reverse |
| MoSCoW | 排序：Must/Should/Could/Won't | Sorting: Must/Should/Could/Won't |
| JTBD | 用户"雇佣"产品完成任务 | Users "hire" products to do jobs |

---

## 🛠️ 集成能力 / Integration Capabilities

| 中文 | English |
|-------|---------|
| **Figma 插件** | **Figma Plugin** |
| 见 `figma-plugin/README.md`，安装后可在 Figma 中生成原型 | See `figma-plugin/README.md`. Generate prototypes in Figma after installation. |
| **飞书集成** | **Lark / Feishu Integration** |
| 见 `assets/lark-bridge/README.md`： | See `assets/lark-bridge/README.md`: |
| - 飞书群机器人 Webhook 推送 | - Webhook push to Lark groups |
| - 飞书文档 API 生成 | - Lark DOC API generation |
| - 飞书多维表格 Base 同步 | - Lark Base (multi-dim table) sync |

---

## 📁 项目结构 / Project Structure

```
user-story-analyst/
├── SKILL.md                       # 角色定义 / Role definition
├── README.md                      # 中文版 / Chinese
├── README.en.md                   # 英文版 / English
├── CHANGELOG.md                   # 变更日志 / Change log
├── LICENSE                        # MIT 许可证
├── CONTRIBUTING.md                # 贡献指南 / Contributing guide
├── prompts/
│   └── system.md                  # System Prompt
├── templates/                     # 文档模板 (6 个)
│   ├── persona.md
│   ├── journey-map.md
│   ├── user-story.md
│   ├── acceptance-criteria.md
│   ├── kano.md
│   └── ab-test.md
├── references/                    # 参考资料 (2 个)
│   ├── methodology.md
│   └── examples.md
└── assets/
    ├── checklist.md               # 评审清单 / Checklist
    ├── diagrams/                  # Mermaid 模板 (10 类)
    ├── figma-bridge/              # Figma 集成
    └── lark-bridge/               # 飞书集成
```

---

## 📊 规模统计 / Statistics

| 项 | 值 |
|------|------|
| 文件数 / Files | 42 |
| 总行数 / Lines | 7700+ |
| 总大小 / Size | 360 KB |
| 打包后 / Packed ZIP | 92 KB |

---

## 🔧 自定义 / Customization

| 中文 | English |
|-------|---------|
| 修改 `prompts/system.md` 即可调整智能体行为：| Modify `prompts/system.md` to customize agent behavior: |
| - 调整输出语言 | - Output language |
| - 强化特定场景 | - Strengthen specific scenarios |
| - 增加新方法论 | - Add new methodologies |
| - 调整场景判断规则 | - Adjust scenario detection rules |

---

## 📜 许可证 / License

| 中文 | English |
|-------|---------|
| MIT License。详见 [LICENSE](LICENSE) 文件。 | MIT License. See [LICENSE](LICENSE) for details. |

---

## 🔗 相关链接 / Related Links

| 资源 / Resource | 链接 / Link |
|------|------|
| 飞书开放平台 / Lark Open Platform | https://open.feishu.cn/app |
| Figma 插件文档 / Figma Plugin Docs | https://www.figma.com/plugin-docs/ |
| Mermaid 在线编辑器 / Mermaid Live Editor | https://mermaid.live/ |
| 飞书 Python SDK / Lark Python SDK | https://pypi.org/project/lark-oapi/ |

---

## 📞 联系方式 / Contact

| 中文 | English |
|-------|---------|
| Issue / 提问：项目仓库的 Issue 区 | Issues / Questions: Use project repository's Issues section |
| 贡献：见 [CONTRIBUTING.md](CONTRIBUTING.md) | Contributing: See [CONTRIBUTING.md](CONTRIBUTING.md) |

---

**版本 / Version**：v1.0.0  
**发布日期 / Release Date**：2026-10-13  
**维护 / Maintainers**：User Story Analyst Contributors

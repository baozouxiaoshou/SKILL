# 变更日志（Changelog）

本文档记录用户故事分析师 Skill 的所有重要变更。

---

## [1.0.0] - 2026-10-13

### 🎉 首次发布

#### 核心能力
- ✅ **场景判断**：自动识别 C 端 / B 端轻量场景
- ✅ **需求澄清**：主动追问 5-8 个关键问题
- ✅ **用户画像**：C 端 Persona + B 端专业人士 Persona 双版本
- ✅ **用户旅程图**：Mermaid 模板（5 个变体）
- ✅ **用户故事拆解**：Epic → Story → Task，含 INVEST 自检
- ✅ **验收标准**：Given-When-Then 三段式，含 C/B 端差异维度
- ✅ **KANO 分类**：C 端 + B 端双版，含实战案例
- ✅ **AB 实验设计**：含样本量、显著性、回滚方案

#### 文档模板（6 个）
- `templates/persona.md` - 用户画像
- `templates/journey-map.md` - 用户旅程图
- `templates/user-story.md` - 用户故事卡
- `templates/acceptance-criteria.md` - 验收标准
- `templates/kano.md` - KANO 分类
- `templates/ab-test.md` - AB 实验

#### 参考资料（2 个）
- `references/methodology.md` - 方法论参考（场景差异对照）
- `references/examples.md` - 完整案例（C 端健身 App + B 端 RAS 双语录入）

#### 可视化模板（10 类 Mermaid，53 个变体）
- `assets/diagrams/user-journey.md` - 用户旅程图
- `assets/diagrams/user-story-map.md` - 用户故事地图
- `assets/diagrams/flowchart.md` - 流程图
- `assets/diagrams/swimlane.md` - 泳道图（B 端协作）
- `assets/diagrams/sequence.md` - 时序图
- `assets/diagrams/state-diagram.md` - 状态机
- `assets/diagrams/er-diagram.md` - ER 图
- `assets/diagrams/gantt.md` - 甘特图
- `assets/diagrams/mindmap.md` - 思维导图
- `assets/diagrams/kano-radar.md` - KANO 雷达图 + 饼图

#### 集成能力
- ✅ **Figma 集成**：`figma-plugin/`（4 文件）+ `assets/figma-bridge/skill_to_figma.py`
- ✅ **飞书集成**：`assets/lark-bridge/`（5 文件）
    - `lark_webhook.py` - 飞书群机器人
    - `lark_doc_generator.py` - 飞书文档生成
    - `lark_base_sync.py` - 飞书多维表格同步
- ✅ **评审清单**：`assets/checklist.md`（INVEST + 场景适配 + B 端合规）

#### 工具脚本
- `install.sh` - 一键安装 / 卸载
- `verify.sh` - 验证 Skill 完整性
- `package.sh` - 一键打包分发

---

## 版本说明

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范。

版本号格式：`主版本号.次版本号.修订号`

- **主版本号**：重大重构、API 不兼容变更
- **次版本号**：新功能、向后兼容
- **修订号**：Bug 修复、文档更新

---

## 升级指南

从 0.x 升级到 1.0：

1. 旧版本没有场景判断功能，建议重新跑 Skill 验证输出
2. 模板文件结构有调整，请使用 `templates/` 下的最新版
3. Figma 插件是新增模块，无需迁移
4. 飞书集成是新增模块，无需迁移

---

## 后续计划

### [1.1.0] - 计划中
- 🔄 增加 Mermaid v10+ 渲染能力
- 🔄 增加 Notion / 钉钉集成
- 🔄 Skill 自动更新检查

### [2.0.0] - 远期
- 🔄 支持动态加载 Skill（无需重启）
- 🔄 支持自定义 Persona + KANO 模板
- 🔄 支持多语言（中英双语）

---

## 贡献者

- **需求分析师团队** - 方法论指导
- **前端开发** - Figma 插件实现
- **后端开发** - Python 工具脚本
- **QA 团队** - 测试用例

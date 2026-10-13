# 可视化模板库（Diagram Templates）

> Mermaid.js 模板集合，覆盖 C 端 + B 端典型图表。

---

## 模板清单

| 文件 | 图表类型 | 适用场景 | 推荐频次 |
|------|---------|---------|---------|
| `user-journey.md` | 用户旅程图 | C 端产品体验全景 | ⭐⭐⭐⭐⭐ |
| `user-story-map.md` | 用户故事地图 | Epic 拆解 | ⭐⭐⭐⭐⭐ |
| `flowchart.md` | 流程图 | 业务流程、操作流程 | ⭐⭐⭐⭐⭐ |
| `swimlane.md` | 泳道图 | B 端跨角色协作 | ⭐⭐⭐⭐ |
| `sequence.md` | 时序图 | 系统交互、API 调用 | ⭐⭐⭐⭐ |
| `state-diagram.md` | 状态机 | 订单、用户、合规状态 | ⭐⭐⭐⭐ |
| `er-diagram.md` | ER 图 | B 端数据模型 | ⭐⭐⭐ |
| `gantt.md` | 甘特图 | Sprint / 项目计划 | ⭐⭐⭐ |
| `mindmap.md` | 思维导图 | 需求结构、头脑风暴 | ⭐⭐⭐ |
| `kano-radar.md` | KANO 雷达图 | 多维评分、优先级 | ⭐⭐ |

---

## 使用方式

### 1. 复制粘贴到 Markdown
所有模板都是 Mermaid 代码块，可直接复制到 `.md` 文件中：
````markdown
```mermaid
flowchart LR
    A --> B
```
````

### 2. 复制到支持 Mermaid 的工具
- GitHub / GitLab / Gitee（Markdown 预览）
- Notion / 飞书 / 钉钉（文档）
- Obsidian / Typora（笔记）
- Figma 插件（如 Mermaid 插件）

### 3. 配合 System Prompt 使用
在 prompts/system.md 中已经引用这些模板，使用 Skill 时自动调用。

---

## Mermaid 通用规范

### 方向
- `LR`（Left to Right）：横向，**推荐用于流程图**
- `TB`（Top to Bottom）：纵向，用于层级结构
- `RL` / `BT`：反向流动

### 节点形状

```
A[方形] - 普通节点
A(圆角) - 普通节点
B{菱形} - 判断节点
C((圆形)) - 起点/终点
D>不对称] - 流程节点
E[[子流程]] - 子流程
F[(数据库)] - 数据库
G[/平行四边形/] - 输入输出
H[\平行四边形\] - 输入输出
```

### 边样式

```
A --> B      - 实线箭头
A --- B      - 实线无箭头
A -.-> B     - 虚线箭头
A ==> B      - 加粗箭头
A -- 文字 --> B - 带文字标签
A --文字--- B - 文字无箭头
A -.文字.-> B - 虚线带文字
```

### 颜色与样式

```
style A fill:#e3f2fd,stroke:#1976d2
style A,B,C fill:#fff3e0
classDef red fill:#ffcdd2
class A,B red
```

---

## 选择图表的决策树

```
要表达什么？
│
├─ 用户体验/行为
│  ├─ 单个用户全旅程 → user-journey.md
│  └─ 多个用户角色 → swimlane.md
│
├─ 业务流程
│  ├─ 单流程 → flowchart.md
│  ├─ 跨角色 → swimlane.md
│  └─ 系统间 → sequence.md
│
├─ 需求拆解
│  ├─ Epic 拆解 → user-story-map.md
│  └─ 头脑风暴 → mindmap.md
│
├─ 数据/状态
│  ├─ 状态流转 → state-diagram.md
│  └─ 数据模型 → er-diagram.md
│
└─ 项目管理
   ├─ Sprint 计划 → gantt.md
   └─ 优先级评分 → kano-radar.md
```

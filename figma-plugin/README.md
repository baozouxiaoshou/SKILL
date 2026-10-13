# Figma 插件：User Story Analyst

> 把 Skill 输出自动转换为 Figma 原型。

---

## 文件清单

```
figma-plugin/
├── manifest.json     # Figma 插件清单
├── code.ts          # 主逻辑（TypeScript）
├── ui.html           # UI 界面
└── README.md         # 本文件
```

---

## 快速开始

### 1. 准备文件
Figma 插件要求 TypeScript 文件，但开发时可以是 `.js`。本项目提供的是开发版本：
- `manifest.json` 直接可用
- `code.js` 改名为 `code.ts` 即可（功能一致）
- `ui.html` 直接可用

### 2. 在 Figma 中运行
1. 打开 Figma 桌面端
2. 菜单 → Plugins → Development → **Import plugin from manifest...**
3. 选择本目录的 `manifest.json`
4. 完成！现在可以在 Plugins 菜单中找到 "User Story Analyst"

### 3. 使用流程
1. 在 Codex 中跑用户故事分析师 Skill
2. 复制输出的 Markdown
3. 在 Figma 中运行插件
4. 粘贴文本 → 点击"生成"

---

## 功能特性

### v1.0 支持

| 功能 | 说明 |
|------|------|
| ✅ 标题解析 | 识别 H1 |
| ✅ 场景徽章 | C 端 / B 端颜色标识 |
| ✅ 用户画像卡片 | 自动创建 Persona 卡 |
| ✅ 用户故事卡片 | 自动创建 Story 卡 |
| ✅ Mermaid 占位框 | 显示代码，可手动渲染 |
| ✅ 验收标准列表 | 文本展示 |

### 限制
- ❌ 不直接渲染 Mermaid（需用 mermaid.live）
- ❌ 不创建组件库
- ❌ 不支持复杂表格

---

## 使用示例

### Step 1：运行 Skill
在 Codex 中说："帮我做一个 AI 训练计划推荐的需求分析"

Skill 输出会包含 Mermaid 图、用户故事等。

### Step 2：复制输出
复制整个 Markdown 内容。

### Step 3：在 Figma 中生成
1. 打开任意 Figma 文件
2. Plugins → User Story Analyst
3. 粘贴文本
4. 点击"生成 Figma 原型"

生成的内容包括：
- 📋 主 Frame（含标题）
- 🎯 场景徽章
- 👤 3 张 Persona 卡片
- 📖 6 张用户故事卡片
- 📊 Mermaid 代码占位框
- ✅ 验收标准列表

---

## 扩展开发

### 修改识别规则
编辑 `code.ts` 中的 `parseSkillOutput()`，添加新识别规则：

```typescript
// 新增：识别 KANO 分类
const kanoRegex = /\[(.+?)\]\s+(\d+)%/g;
while ((kanoMatch = kanoRegex.exec(raw)) !== null) {
  result.kano.push({
    feature: kanoMatch[1].trim(),
    percentage: kanoMatch[2]
  });
}
```

### 修改颜色规范
编辑 `code.ts` 中的 `createXxxCard()` 函数：

```typescript
// 改用品牌色
card.fills = [{ type: 'SOLID', color: { r: 0.95, g: 0.92, b: 0.98 } }];
```

### 添加新的节点类型
在 `handleSkillOutput()` 中添加新的 section：

```typescript
// 新增：优先级图表
if (parsed.kano && parsed.kano.length > 0) {
  const kanoSection = createSection("🎯 KANO 分类", 36);
  mainFrame.appendChild(kanoSection);
  // ... 渲染 KANO 数据
}
```

---

## 故障排查

### 插件加载失败
- 检查 `manifest.json` 的 JSON 语法
- 确认 `editorType` 是 `["figma"]` 而非 `["figjam"]`

### 解析无内容
- 检查 Markdown 是否符合格式
- 在控制台查看 `parseSkillOutput()` 的结果

### Mermaid 图不渲染
v1.0 限制，需手动复制到 mermaid.live 渲染后粘贴。

---

## 升级路径

- **v1.0**（当前）：基础解析 + Frame 生成
- **v2.0**：集成 mermaid.js 客户端，自动渲染 Mermaid 为 Figma 节点
- **v3.0**：双向同步（修改 Story 后回写 Skill）

---

## 相关资源

- Skill 主项目：`/Users/llh_me/Documents/app/codex/agents/c-user-story-analyst/`
- 桥接指南：`../assets/figma-bridge/README.md`
- Figma 插件开发文档：https://www.figma.com/plugin-docs/
- Mermaid 渲染器：https://mermaid.live/

// Figma 插件主逻辑 - User Story Analyst
// 用于将 Skill 输出（Markdown + Mermaid）转换为 Figma 原型

// 接收 Skill 输出的主入口
async function handleSkillOutput(skillOutput) {
  const parsed = parseSkillOutput(skillOutput);

  // 创建主 Frame
  const mainFrame = figma.createFrame();
  mainFrame.name = "📋 Skill Output - " + new Date().toLocaleString('zh-CN');
  mainFrame.layoutMode = "VERTICAL";
  mainFrame.itemSpacing = 32;
  mainFrame.paddingLeft = 64;
  mainFrame.paddingRight = 64;
  mainFrame.paddingTop = 64;
  mainFrame.paddingBottom = 64;
  mainFrame.primaryAxisSizingMode = "AUTO";
  mainFrame.counterAxisSizingMode = "AUTO";
  mainFrame.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
  mainFrame.x = 0;
  mainFrame.y = 0;

  // 1. 标题区
  const title = figma.createText();
  title.fontName = { family: "Inter", style: "Bold" };
  title.fontSize = 32;
  title.characters = parsed.title || "用户故事分析";
  title.fills = [{ type: 'SOLID', color: { r: 0.1, g: 0.1, b: 0.1 } }];
  mainFrame.appendChild(title);

  // 2. 场景判断
  if (parsed.sceneType) {
    const sceneBadge = createBadge(
      "场景：" + parsed.sceneType,
      parsed.sceneType === "C 端" ? "#e3f2fd" : "#fff3e0"
    );
    mainFrame.appendChild(sceneBadge);
  }

  // 3. 用户画像
  if (parsed.personas && parsed.personas.length > 0) {
    const personaSection = createSection("👤 用户画像", 36);
    mainFrame.appendChild(personaSection);

    for (const persona of parsed.personas) {
      const card = createPersonaCard(persona);
      mainFrame.appendChild(card);
    }
  }

  // 4. 用户故事
  if (parsed.stories && parsed.stories.length > 0) {
    const storySection = createSection("📖 用户故事", 36);
    mainFrame.appendChild(storySection);

    for (const story of parsed.stories) {
      const card = createStoryCard(story);
      mainFrame.appendChild(card);
    }
  }

  // 5. Mermaid 图
  if (parsed.diagrams && parsed.diagrams.length > 0) {
    const diagramSection = createSection("📊 可视化图表", 36);
    mainFrame.appendChild(diagramSection);

    for (const diagram of parsed.diagrams) {
      await createDiagramCard(diagram, mainFrame);
    }
  }

  // 6. 验收标准
  if (parsed.acceptanceCriteria && parsed.acceptanceCriteria.length > 0) {
    const acSection = createSection("✅ 验收标准", 36);
    mainFrame.appendChild(acSection);

    for (const ac of parsed.acceptanceCriteria) {
      const acText = figma.createText();
      acText.fontName = { family: "Inter", style: "Regular" };
      acText.fontSize = 14;
      acText.characters = ac;
      acText.fills = [{ type: 'SOLID', color: { r: 0.3, g: 0.3, b: 0.3 } }];
      mainFrame.appendChild(acText);
    }
  }

  // 选中主 Frame
  figma.currentPage.selection = [mainFrame];
  figma.viewport.scrollAndZoomIntoView([mainFrame]);

  return mainFrame.id;
}

// ============ 解析器 ============

function parseSkillOutput(raw) {
  const result = {
    title: '',
    sceneType: '',
    personas: [],
    stories: [],
    diagrams: [],
    acceptanceCriteria: []
  };

  // 解析标题（# 开头的第一行）
  const titleMatch = raw.match(/^#\s+(.+)$/m);
  if (titleMatch) result.title = titleMatch[1].trim();

  // 解析场景判断
  const sceneMatch = raw.match(/\*\*场景类型[：:]\*\*\s*(.+?)(?:\n|$)/);
  if (sceneMatch) result.sceneType = sceneMatch[1].trim();

  // 解析 Persona 卡片（"### Persona 1: 昵称" 开头）
  const personaRegex = /###\s+(?:🎭\s+)?Persona\s+\d+[：:](.+)/g;
  let personaMatch;
  while ((personaMatch = personaRegex.exec(raw)) !== null) {
    const name = personaMatch[1].trim();
    // 提取后续描述直到下一个 ###
    const startIdx = personaMatch.index + personaMatch[0].length;
    const nextSection = raw.slice(startIdx).search(/\n###\s|\n##\s/);
    const endIdx = nextSection === -1 ? raw.length : startIdx + nextSection;
    const description = raw.slice(startIdx, endIdx).trim();

    result.personas.push({ name, description });
  }

  // 解析用户故事（"作为 XX，我想要 XX，以便 XX" 格式）
  const storyRegex = /作为 \[(.+?)\][，,]\s*我想要 \[(.+?)\][，,]\s*以便 \[(.+?)\]/g;
  let storyMatch;
  while ((storyMatch = storyRegex.exec(raw)) !== null) {
    result.stories.push({
      role: storyMatch[1].trim(),
      want: storyMatch[2].trim(),
      benefit: storyMatch[3].trim()
    });
  }

  // 解析 Mermaid 代码块
  const mermaidRegex = /```mermaid\n([\s\S]+?)\n```/g;
  let mermaidMatch;
  while ((mermaidMatch = mermaidRegex.exec(raw)) !== null) {
    result.diagrams.push({
      code: mermaidMatch[1].trim()
    });
  }

  // 解析验收标准（"- Given..." 格式）
  const acRegex = /^[✅-]\s+(Given[^\n]+)/gm;
  let acMatch;
  while ((acMatch = acRegex.exec(raw)) !== null) {
    result.acceptanceCriteria.push(acMatch[1].trim());
  }

  return result;
}

// ============ UI 组件构建器 ============

function createSection(title, spacingTop) {
  const section = figma.createFrame();
  section.name = title;
  section.layoutMode = "VERTICAL";
  section.itemSpacing = 16;
  section.fills = [];
  section.primaryAxisSizingMode = "AUTO";
  section.counterAxisSizingMode = "AUTO";

  const text = figma.createText();
  text.fontName = { family: "Inter", style: "Semi Bold" };
  text.fontSize = 20;
  text.characters = title;
  text.fills = [{ type: 'SOLID', color: { r: 0.1, g: 0.1, b: 0.1 } }];
  section.appendChild(text);

  return section;
}

function createBadge(text, bgColor) {
  const badge = figma.createFrame();
  badge.layoutMode = "HORIZONTAL";
  badge.paddingLeft = 12;
  badge.paddingRight = 12;
  badge.paddingTop = 6;
  badge.paddingBottom = 6;
  badge.cornerRadius = 16;
  badge.primaryAxisSizingMode = "AUTO";
  badge.counterAxisSizingMode = "AUTO";
  badge.fills = [{ type: 'SOLID', color: hexToRgb(bgColor) }];

  const label = figma.createText();
  label.fontName = { family: "Inter", style: "Medium" };
  label.fontSize = 12;
  label.characters = text;
  label.fills = [{ type: 'SOLID', color: { r: 0.1, g: 0.1, b: 0.1 } }];
  badge.appendChild(label);

  return badge;
}

function createPersonaCard(persona) {
  const card = figma.createFrame();
  card.name = "Persona: " + persona.name;
  card.layoutMode = "VERTICAL";
  card.itemSpacing = 8;
  card.paddingLeft = 16;
  card.paddingRight = 16;
  card.paddingTop = 16;
  card.paddingBottom = 16;
  card.cornerRadius = 8;
  card.fills = [{ type: 'SOLID', color: { r: 0.97, g: 0.97, b: 0.97 } }];
  card.strokes = [{ type: 'SOLID', color: { r: 0.9, g: 0.9, b: 0.9 } }];
  card.strokeWeight = 1;
  card.primaryAxisSizingMode = "AUTO";
  card.counterAxisSizingMode = "FIXED";
  card.resize(400, card.height);

  const name = figma.createText();
  name.fontName = { family: "Inter", style: "Semi Bold" };
  name.fontSize = 16;
  name.characters = "👤 " + persona.name;
  name.fills = [{ type: 'SOLID', color: { r: 0.1, g: 0.1, b: 0.1 } }];
  card.appendChild(name);

  const desc = figma.createText();
  desc.fontName = { family: "Inter", style: "Regular" };
  desc.fontSize = 12;
  desc.characters = persona.description.slice(0, 500);
  desc.fills = [{ type: 'SOLID', color: { r: 0.3, g: 0.3, b: 0.3 } }];
  desc.textAutoResize = "HEIGHT";
  card.appendChild(desc);

  return card;
}

function createStoryCard(story) {
  const card = figma.createFrame();
  card.name = "Story: " + story.want.slice(0, 30);
  card.layoutMode = "VERTICAL";
  card.itemSpacing = 8;
  card.paddingLeft = 16;
  card.paddingRight = 16;
  card.paddingTop = 16;
  card.paddingBottom = 16;
  card.cornerRadius = 8;
  card.fills = [{ type: 'SOLID', color: { r: 0.99, g: 0.95, b: 0.86 } }];
  card.strokes = [{ type: 'SOLID', color: { r: 0.95, g: 0.85, b: 0.6 } }];
  card.strokeWeight = 1;
  card.primaryAxisSizingMode = "AUTO";
  card.counterAxisSizingMode = "FIXED";
  card.resize(500, card.height);

  const role = figma.createText();
  role.fontName = { family: "Inter", style: "Regular" };
  role.fontSize = 12;
  role.characters = "👤 作为 " + story.role;
  role.fills = [{ type: 'SOLID', color: { r: 0.4, g: 0.4, b: 0.4 } }];
  card.appendChild(role);

  const want = figma.createText();
  want.fontName = { family: "Inter", style: "Semi Bold" };
  want.fontSize = 14;
  want.characters = "🎯 我想要：" + story.want;
  want.fills = [{ type: 'SOLID', color: { r: 0.1, g: 0.1, b: 0.1 } }];
  card.appendChild(want);

  const benefit = figma.createText();
  benefit.fontName = { family: "Inter", style: "Regular" };
  benefit.fontSize = 12;
  benefit.characters = "💎 以便：" + story.benefit;
  benefit.fills = [{ type: 'SOLID', color: { r: 0.3, g: 0.3, b: 0.6 } }];
  card.appendChild(benefit);

  return card;
}

async function createDiagramCard(diagram, parent) {
  const card = figma.createFrame();
  card.name = "Mermaid Diagram";
  card.layoutMode = "VERTICAL";
  card.itemSpacing = 8;
  card.paddingLeft = 16;
  card.paddingRight = 16;
  card.paddingTop = 16;
  card.paddingBottom = 16;
  card.cornerRadius = 8;
  card.fills = [{ type: 'SOLID', color: { r: 0.95, g: 0.97, b: 1.0 } }];
  card.primaryAxisSizingMode = "AUTO";
  card.counterAxisSizingMode = "FIXED";
  card.resize(700, card.height);

  // 标题
  const title = figma.createText();
  title.fontName = { family: "Inter", style: "Semi Bold" };
  title.fontSize = 14;
  title.characters = "📊 Mermaid 图（请在 Figma 之外渲染）";
  title.fills = [{ type: 'SOLID', color: { r: 0.1, g: 0.1, b: 0.5 } }];
  card.appendChild(title);

  // 显示代码（用户可手动复制到 Mermaid Live Editor）
  const codeText = figma.createText();
  codeText.fontName = { family: "JetBrains Mono", style: "Regular" };
  codeText.fontSize = 11;
  codeText.characters = diagram.code;
  codeText.fills = [{ type: 'SOLID', color: { r: 0.2, g: 0.2, b: 0.2 } }];
  codeText.layoutSizingHorizontal = "FILL";
  card.appendChild(codeText);

  parent.appendChild(card);
}

function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16) / 255,
    g: parseInt(result[2], 16) / 255,
    b: parseInt(result[3], 16) / 255
  } : { r: 0.9, g: 0.9, b: 0.9 };
}

// ============ 消息处理 ============

figma.ui.onmessage = async (msg) => {
  if (msg.type === 'generate') {
    try {
      const frameId = await handleSkillOutput(msg.payload);
      figma.ui.postMessage({ type: 'success', frameId: frameId });
    } catch (err) {
      figma.ui.postMessage({ type: 'error', message: err.message });
    }
  }
};

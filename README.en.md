# User Story Analyst

> A requirement analysis Skill covering both **C-side** and **lightweight B-side** scenarios.

📖 **Languages**: [中文](README.md) | **English**（本文件 / This File）| [中英双语 / Bilingual](docs/README-BILINGUAL.md)

## 📦 Installation

#### Quick Install (Recommended)
```bash
cd /Users/llh_me/Documents/app/codex/agents/c-user-story-analyst
./install.sh
```

#### Manual Install
```bash
mkdir -p ~/.codex/skills
ln -s /Users/llh_me/Documents/app/codex/agents/c-user-story-analyst \
      ~/.codex/skills/user-story-analyst
```

#### Verify
```bash
./verify.sh
```

#### Uninstall
```bash
./install.sh --uninstall
```

---

## Applicable Scenarios

| Scenario | Typical Input | Output Focus |
|----------|---------------|--------------|
| **C-side Products** | Fitness apps, habit tracking, community features | User journey, retention metrics, A/B testing |
| **Lightweight B-side** | Compliance forms, B-side entries, internal tools, workflow systems | Compliance design, version snapshots, audit trail |
| **Hybrid Scenarios** | Cross-border C-side products | Experience + compliance equally important |

---

## Quick Start

### Method 1: As Codex Skill
The install script handles this automatically.

### Method 2: Use System Prompt Standalone
Read `prompts/system.md` and copy it as the system prompt for ChatGPT / Claude / Cursor.

---

## What You Get

A skill that transforms vague business requirements into **executable, testable, valuable** user story cards, covering:

- ✅ **Scenario Detection** - Auto-identify C-side vs lightweight B-side
- ✅ **Requirement Clarification** - 5-8 critical questions
- ✅ **Persona Building** - C-side consumers + B-side professionals
- ✅ **Journey Mapping** - Visual user journey
- ✅ **Story Decomposition** - Epic → Story → Task with INVEST principles
- ✅ **Acceptance Criteria** - Given-When-Then format
- ✅ **Priority Classification** - KANO model + MoSCoW
- ✅ **A/B Experiment Design** - Sample size, significance, rollback plans
- ✅ **Compliance Design** - Term library, audit logs, version snapshots (B-side)
- ✅ **Visualization Templates** - 10 categories of Mermaid diagrams

---

## Project Structure

```
user-story-analyst/
├── SKILL.md                       # Role definition
├── README.md                      # Chinese variant
├── README.en.md                   # English variant (this file)
├── CHANGELOG.md                   # Change log
├── LICENSE                        # MIT License
├── CONTRIBUTING.md                # Contributing guide
├── prompts/
│   └── system.md                  # System Prompt
├── templates/                     # Document templates (6 files)
│   ├── persona.md                 # Persona template
│   ├── journey-map.md             # Journey map template
│   ├── user-story.md              # User story card
│   ├── acceptance-criteria.md     # Acceptance criteria template
│   ├── kano.md                    # KANO classification
│   └── ab-test.md                 # A/B experiment template
├── references/                    # References (2 files)
│   ├── methodology.md             # Methodology reference
│   └── examples.md                # Complete examples
└── assets/
    ├── checklist.md               # Review checklist
    ├── diagrams/                  # Mermaid templates (10 categories)
    │   ├── README.md
    │   ├── user-journey.md
    │   ├── user-story-map.md
    │   ├── flowchart.md
    │   ├── swimlane.md
    │   ├── sequence.md
    │   ├── state-diagram.md
    │   ├── er-diagram.md
    │   ├── gantt.md
    │   ├── mindmap.md
    │   └── kano-radar.md
    ├── figma-bridge/              # Figma integration
    │   ├── README.md
    │   └── skill_to_figma.py      # Markdown → Figma JSON converter
    └── lark-bridge/               # Lark (Feishu) integration
        ├── README.md              # Integration guide
        ├── config.example.json    # Configuration example
        ├── lark_webhook.py        # Webhook push
        ├── lark_doc_generator.py  # Document generator
        └── lark_base_sync.py      # Base (multi-dim table) sync
└── figma-plugin/                  # Figma plugin (4 files)
    ├── manifest.json
    ├── code.js
    ├── ui.html
    └── README.md
```

---

## Workflow (6 Steps)

```
Step 0: Scenario Detection → Auto-identify C-side / B-side lightweight
Step 2: Persona → Consumer or professional
Step 4: Story Decomposition → Epic → User Story + AC
Step 5: Priority + Metrics / Experiment / Compliance
```

---

## Scenario Comparison

| Dimension | C-side | B-side Lightweight |
|-----------|--------|-------------------|
| Persona Type | Consumer | Professional / Employee |
| Core Pain Point | Experience, convenience, emotion | Efficiency, compliance, accuracy |
| North Star | Retention, activity | Task completion, compliance rate |
| Must-have AC | Experience, edge cases | Compliance, security, traceability |
| Visualization Focus | User journey | Process + role collaboration |
| Priority Principle | Value × cost | Compliance baseline > business value |

---

## Customization

Edit `prompts/system.md` to customize:

- Output language (Chinese / English / Bilingual)
- Strengthen specific areas (e-commerce, content, compliance)
- Add new methodologies (RICE, ICE)
- Adjust scenario detection rules

---

## Integration Capabilities

### Figma Plugin
See `figma-plugin/README.md` for installation and usage.

### Lark / Feishu
See `assets/lark-bridge/README.md` for:
- Webhook push to Lark groups
- Lark DOC generation
- Lark Base (multi-dim table) sync

---

## Resources Structure

```
user-story-analyst/
├── SKILL.md                       # Role definition
├── README.md                      # Chinese variant
├── README.en.md                   # English variant
├── CHANGELOG.md                   # Change log
├── LICENSE                        # MIT License
├── CONTRIBUTING.md                # Contributing guide
├── prompts/system.md              # System Prompt
├── templates/                     # Document templates (6 files)
├── references/                    # References (2 files)
└── assets/
    ├── checklist.md               # Review checklist
    └── diagrams/                  # Mermaid templates
```

---

## Customization

Modify `prompts/system.md` to adjust agent behavior:
- Output language
- Strengthen specific scenarios
- Add new methodologies

---

## Contribution

Improve documentation or add cases via `references/examples.md`.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Related Resources

- Lark Open Platform: https://open.feishu.cn/app
- Figma Plugin Docs: https://www.figma.com/plugin-docs/
- Mermaid Live Editor: https://mermaid.live/

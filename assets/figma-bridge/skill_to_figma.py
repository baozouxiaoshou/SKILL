#!/usr/bin/env python3
"""
Skill 输出 → Figma 插件可消费格式转换器

输入：Skill 输出的 Markdown 文件
输出：Figma 插件可直接使用的 JSON 格式

使用方法：
    python skill_to_figma.py <input.md> <output.json>
    
或者：
    python skill_to_figma.py --clipboard  # 从剪贴板读取
"""
import json
import re
import sys
import argparse
from pathlib import Path


def parse_markdown(raw: str) -> dict:
    """解析 Skill 输出的 Markdown"""
    result = {
        "title": "",
        "sceneType": "",
        "personas": [],
        "stories": [],
        "diagrams": [],
        "acceptanceCriteria": [],
        "metadata": {}
    }
    
    # 解析标题
    title_match = re.search(r'^#\s+(.+)$', raw, re.MULTILINE)
    if title_match:
        result["title"] = title_match.group(1).strip()
    
    # 解析场景判断
    scene_match = re.search(r'\*\*场景类型\*\*[：:]\s*(.+?)(?:\n|$)', raw)
    if scene_match:
        result["sceneType"] = scene_match.group(1).strip()
    
    # 解析 Persona
    persona_pattern = re.compile(
        r'###\s+(?:🎭\s+)?Persona\s+\d+[：:]\s*(.+?)(?:\n|$)',
        re.MULTILINE
    )
    for match in persona_pattern.finditer(raw):
        name = match.group(1).strip()
        start = match.end()
        # 找下一个 ### 或 ##
        next_match = re.search(r'\n#{2,3}\s', raw[start:])
        end = start + next_match.start() if next_match else len(raw)
        description = raw[start:end].strip()
        result["personas"].append({
            "name": name,
            "description": description[:500]
        })
    
    # 解析用户故事
    story_pattern = re.compile(
        r'作为\s*\[(.+?)\][，,]\s*'
        r'我想要\s*\[(.+?)\][，,]\s*'
        r'以便\s*\[(.+?)\]'
    )
    for match in story_pattern.finditer(raw):
        result["stories"].append({
            "role": match.group(1).strip(),
            "want": match.group(2).strip(),
            "benefit": match.group(3).strip()
        })
    
    # 解析 Mermaid 代码块
    mermaid_pattern = re.compile(r'```mermaid\n([\s\S]+?)\n```')
    for match in mermaid_pattern.finditer(raw):
        code = match.group(1).strip()
        diagram_type = detect_diagram_type(code)
        result["diagrams"].append({
            "code": code,
            "type": diagram_type
        })
    
    # 解析验收标准
    ac_pattern = re.compile(r'^[✅\-\*]\s+(Given.+?)(?=\n\n|\n[✅\-\*]|\Z)', re.MULTILINE | re.DOTALL)
    for match in ac_pattern.finditer(raw):
        ac_text = match.group(1).strip()
        if ac_text:
            result["acceptanceCriteria"].append(ac_text)
    
    # 元数据
    result["metadata"] = {
        "parsedAt": "",
        "storyCount": len(result["stories"]),
        "personaCount": len(result["personas"]),
        "diagramCount": len(result["diagrams"])
    }
    
    return result


def detect_diagram_type(code: str) -> str:
    """识别 Mermaid 图类型"""
    first_line = code.split('\n')[0].strip().lower()
    if first_line.startswith('flowchart') or first_line.startswith('graph'):
        return 'flowchart'
    elif first_line.startswith('sequencediagram'):
        return 'sequence'
    elif first_line.startswith('statediagram'):
        return 'state'
    elif first_line.startswith('erdiagram'):
        return 'er'
    elif first_line.startswith('gantt'):
        return 'gantt'
    elif first_line.startswith('classdiagram'):
        return 'class'
    elif first_line.startswith('mindmap'):
        return 'mindmap'
    elif 'radar-beta' in code or 'pie' in first_line:
        return 'chart'
    else:
        return 'unknown'


def to_figma_format(parsed: dict) -> dict:
    """转换为 Figma 插件可直接消费的格式"""
    return {
        "version": "1.0",
        "source": "user-story-analyst-skill",
        "title": parsed["title"],
        "sceneType": parsed["sceneType"],
        "components": {
            "personas": [
                {
                    "type": "CARD",
                    "name": f"Persona: {p['name']}",
                    "color": "GRAY",
                    "content": p
                }
                for p in parsed["personas"]
            ],
            "stories": [
                {
                    "type": "CARD",
                    "name": f"Story: {s['want'][:30]}",
                    "color": "YELLOW",
                    "content": s
                }
                for s in parsed["stories"]
            ],
            "diagrams": [
                {
                    "type": "DIAGRAM_PLACEHOLDER",
                    "name": f"Diagram: {d['type']}",
                    "color": "BLUE",
                    "content": d
                }
                for d in parsed["diagrams"]
            ],
            "acceptanceCriteria": [
                {
                    "type": "TEXT",
                    "name": "AC",
                    "color": "GREEN",
                    "content": ac
                }
                for ac in parsed["acceptanceCriteria"]
            ]
        },
        "metadata": parsed["metadata"]
    }


def main():
    parser = argparse.ArgumentParser(description="Skill 输出转换为 Figma 插件格式")
    parser.add_argument("input", nargs="?", help="输入的 Markdown 文件路径")
    parser.add_argument("output", nargs="?", help="输出的 JSON 文件路径")
    parser.add_argument("--clipboard", action="store_true", help="从剪贴板读取")
    parser.add_argument("--print", action="store_true", help="打印到控制台而不写文件")
    
    args = parser.parse_args()
    
    # 读取内容
    if args.clipboard:
        try:
            import pyperclip
            raw = pyperclip.paste()
        except ImportError:
            print("❌ 需要 pyperclip 库：`pip install pyperclip`")
            sys.exit(1)
    elif args.input:
        content = Path(args.input).read_text(encoding='utf-8')
        raw = content
    else:
        print("❌ 请提供输入文件路径或使用 --clipboard")
        parser.print_help()
        sys.exit(1)
    
    # 解析 + 转换
    parsed = parse_markdown(raw)
    figma_format = to_figma_format(parsed)
    
    # 输出
    output_json = json.dumps(figma_format, ensure_ascii=False, indent=2)
    
    if args.print:
        print(output_json)
    elif args.output:
        Path(args.output).write_text(output_json, encoding='utf-8')
        print(f"✅ 已转换：{args.output}")
        print(f"   标题: {parsed['title']}")
        print(f"   场景: {parsed['sceneType']}")
        print(f"   Persona: {len(parsed['personas'])} 个")
        print(f"   Story: {len(parsed['stories'])} 个")
        print(f"   Mermaid: {len(parsed['diagrams'])} 个")
        print(f"   AC: {len(parsed['acceptanceCriteria'])} 条")
    else:
        print(output_json)


if __name__ == "__main__":
    main()

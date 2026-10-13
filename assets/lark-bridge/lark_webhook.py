#!/usr/bin/env python3
"""
飞书群机器人 Webhook 推送工具

功能：
- 把 Skill 输出的 Markdown 推送到飞书群
- 支持卡片消息、富文本消息
- 自动适配飞书消息格式

使用方法：
1. 在飞书群中添加机器人，获取 Webhook URL
2. 设置环境变量 LARK_WEBHOOK_URL
3. 运行：python lark_webhook.py <markdown_file>
"""
import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path


def parse_markdown_sections(raw: str) -> list[dict]:
    """把 Markdown 解析为飞书消息区块"""
    sections = []
    current_section = {"type": "text", "content": ""}
    
    lines = raw.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Mermaid 代码块
        if line.strip().startswith('```mermaid'):
            # 累积之前的文本
            if current_section["content"].strip():
                sections.append(current_section)
                current_section = {"type": "text", "content": ""}
            
            # 读取 mermaid 代码块
            mermaid_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                mermaid_lines.append(lines[i])
                i += 1
            
            sections.append({
                "type": "code",
                "language": "mermaid",
                "content": '\n'.join(mermaid_lines).strip()
            })
            i += 1
            continue
        
        # 普通代码块
        if line.strip().startswith('```'):
            if current_section["content"].strip():
                sections.append(current_section)
                current_section = {"type": "text", "content": ""}
            
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            
            sections.append({
                "type": "code",
                "language": "text",
                "content": '\n'.join(code_lines).strip()
            })
            i += 1
            continue
        
        # 标题
        if line.startswith('# '):
            if current_section["content"].strip():
                sections.append(current_section)
                current_section = {"type": "text", "content": ""}
            sections.append({"type": "heading", "level": 1, "content": line[2:].strip()})
        elif line.startswith('## '):
            if current_section["content"].strip():
                sections.append(current_section)
                current_section = {"type": "text", "content": ""}
            sections.append({"type": "heading", "level": 2, "content": line[3:].strip()})
        elif line.startswith('### '):
            if current_section["content"].strip():
                sections.append(current_section)
                current_section = {"type": "text", "content": ""}
            sections.append({"type": "heading", "level": 3, "content": line[4:].strip()})
        elif line.startswith('#### '):
            if current_section["content"].strip():
                sections.append(current_section)
                current_section = {"type": "text", "content": ""}
            sections.append({"type": "heading", "level": 4, "content": line[5:].strip()})
        # 分隔线
        elif line.strip() in ('---', '***'):
            if current_section["content"].strip():
                sections.append(current_section)
                current_section = {"type": "text", "content": ""}
            sections.append({"type": "divider"})
        # 引用
        elif line.startswith('> '):
            if current_section["content"].strip():
                sections.append(current_section)
                current_section = {"type": "text", "content": ""}
            quote_lines = []
            while i < len(lines) and lines[i].startswith('> '):
                quote_lines.append(lines[i][2:])
                i += 1
            sections.append({"type": "quote", "content": '\n'.join(quote_lines).strip()})
            continue
        else:
            current_section["content"] += line + '\n'
        
        i += 1
    
    # 最后一段
    if current_section["content"].strip():
        sections.append(current_section)
    
    return sections


def build_card_message(sections: list[dict], title: str = "") -> dict:
    """构建飞书卡片消息"""
    elements = []
    header_title = title or "用户故事分析"
    
    for section in sections:
        if section["type"] == "heading":
            level = section["level"]
            # H1 / H2 用 markdown 标签
            tag = f"heading{level}"
            elements.append({
                "tag": tag,
                "text": {
                    "tag": "lark_md",
                    "content": section["content"]
                }
            })
        elif section["type"] == "code":
            # 代码块用 note 元素
            code_text = section["content"][:2000]  # 飞书限制
            if len(section["content"]) > 2000:
                code_text += "\n... (截断)"
            elements.append({
                "tag": "note",
                "elements": [
                    {
                        "tag": "plain_text",
                        "content": f"```{section['language']}\n{code_text}\n```"
                    }
                ]
            })
        elif section["type"] == "quote":
            elements.append({
                "tag": "quote",
                "text": {
                    "tag": "lark_md",
                    "content": section["content"]
                }
            })
        elif section["type"] == "divider":
            elements.append({"tag": "hr"})
        elif section["type"] == "text":
            text = section["content"].strip()
            if text:
                elements.append({
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": text[:4000]  # 飞书限制
                    }
                })
    
    return {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True,
                "enable_forward": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "tag": "plain_text",
                    "content": header_title[:30]
                }
            },
            "elements": elements
        }
    }


def build_simple_message(raw: str, title: str = "") -> dict:
    """构建飞书简单文本消息"""
    content = raw.strip()
    if title:
        content = f"**{title}**\n\n{content}"
    
    return {
        "msg_type": "text",
        "content": {
            "text": content[:4000]  # 飞书限制
        }
    }


def send_to_lark(webhook_url: str, message: dict) -> tuple[bool, str]:
    """发送消息到飞书"""
    data = json.dumps(message, ensure_ascii=False).encode('utf-8')
    
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            body = response.read().decode('utf-8')
            result = json.loads(body)
            
            if result.get('StatusCode') == 0 or result.get('code') == 0:
                return True, "发送成功"
            else:
                return False, f"飞书返回错误: {body}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP 错误: {e.code} - {e.reason}"
    except urllib.error.URLError as e:
        return False, f"网络错误: {e.reason}"
    except Exception as e:
        return False, f"未知错误: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="推送 Skill 输出到飞书群")
    parser.add_argument("input", help="Skill 输出的 Markdown 文件")
    parser.add_argument("--webhook", help="飞书机器人 Webhook URL")
    parser.add_argument("--title", default="用户故事分析", help="消息标题")
    parser.add_argument("--simple", action="store_true", help="使用简单文本而非卡片")
    parser.add_argument("--dry-run", action="store_true", help="只生成消息不发送")
    
    args = parser.parse_args()
    
    # 获取 Webhook URL
    webhook_url = args.webhook or os.environ.get('LARK_WEBHOOK_URL')
    if not webhook_url and not args.dry_run:
        print("❌ 请提供 Webhook URL：")
        print("   --webhook https://open.feishu.cn/...")
        print("   或设置环境变量 LARK_WEBHOOK_URL")
        sys.exit(1)
    
    # 读取 Markdown
    raw = Path(args.input).read_text(encoding='utf-8')
    
    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', raw, re.MULTILINE)
    if title_match and not args.title:
        args.title = title_match.group(1).strip()
    
    # 构建消息
    if args.simple:
        message = build_simple_message(raw, args.title)
    else:
        sections = parse_markdown_sections(raw)
        message = build_card_message(sections, args.title)
    
    if args.dry_run:
        print(json.dumps(message, ensure_ascii=False, indent=2))
        return
    
    # 发送
    success, msg = send_to_lark(webhook_url, message)
    if success:
        print(f"✅ {msg}")
    else:
        print(f"❌ {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()

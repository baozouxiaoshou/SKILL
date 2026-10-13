#!/usr/bin/env python3
"""
飞书文档生成器

功能：
- 把 Skill 输出的 Markdown 转换为飞书 DOC API 调用所需的 JSON
- 用户可配合飞书开放平台 App ID + Secret 调用

使用方法：
1. 在飞书开放平台创建 App（https://open.feishu.cn/app）
2. 配置权限：docx:document:create 等
3. 复制生成的 JSON 到 API 工具调用，或配合 SDK

参考：
- 飞书开放平台：https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/create
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def parse_markdown_blocks(raw: str) -> list[dict]:
    """解析 Markdown 为飞书文档块结构"""
    blocks = []
    
    lines = raw.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # H1-H9 标题
        m = re.match(r'^(#{1,9})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            blocks.append({
                "block_type": 3 + level,  # 飞书: H1=3, H2=4, ...
                "heading" + str(level): {
                    "elements": [{"text_run": {"content": m.group(2).strip()}}],
                    "style": {}
                }
            })
            i += 1
            continue
        
        # Mermaid / 代码块
        if line.strip().startswith('```'):
            language = "plain_text"
            if 'mermaid' in line.lower():
                language = "mermaid"
            
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            
            blocks.append({
                "block_type": 14,  # Code block
                "code": {
                    "elements": [{
                        "text_run": {
                            "content": '\n'.join(code_lines)[:4000]
                        }
                    }],
                    "style": {"language": language_to_code_lang(language)}
                }
            })
            i += 1
            continue
        
        # 分隔线
        if line.strip() in ('---', '***', '___'):
            blocks.append({"block_type": 22})  # Divider
            i += 1
            continue
        
        # 引用
        if line.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].startswith('> '):
                quote_lines.append(lines[i][2:])
                i += 1
            blocks.append({
                "block_type": 15,  # Quote
                "quote": {
                    "elements": [{
                        "text_run": {"content": '\n'.join(quote_lines)}
                    }],
                    "style": {}
                }
            })
            continue
        
        # 无序列表
        if re.match(r'^[\-\*\+]\s+', line):
            list_items = []
            while i < len(lines) and re.match(r'^[\-\*\+]\s+', lines[i]):
                item_text = re.sub(r'^[\-\*\+]\s+', '', lines[i])
                list_items.append(item_text)
                i += 1
            blocks.append({
                "block_type": 12,  # Bullet list
                "bullet": {
                    "elements": [{"text_run": {"content": '\n'.join(list_items)}}],
                    "style": {}
                }
            })
            continue
        
        # 有序列表
        if re.match(r'^\d+\.\s+', line):
            list_items = []
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i]):
                item_text = re.sub(r'^\d+\.\s+', '', lines[i])
                list_items.append(item_text)
                i += 1
            blocks.append({
                "block_type": 13,  # Ordered list
                "ordered": {
                    "elements": [{"text_run": {"content": '\n'.join(list_items)}}],
                    "style": {}
                }
            })
            continue
        
        # 空行
        if not line.strip():
            i += 1
            continue
        
        # 普通段落
        text = line
        while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r'^[#\->]', lines[i + 1]) and not lines[i + 1].startswith('```'):
            text += '\n' + lines[i + 1]
            i += 1
        
        blocks.append({
            "block_type": 2,  # Text
            "text": {
                "elements": parse_inline(text),
                "style": {}
            }
        })
        i += 1
    
    return blocks


def parse_inline(text: str) -> list[dict]:
    """解析行内格式（粗体、斜体、代码）"""
    elements = []
    
    # 简化处理：飞书的 text_run 支持加粗、斜体、删除线
    # 这里做基础实现
    
    # 拆分 [text](url) 链接
    # 拆分 **bold** 为粗体
    
    # 简化版：整段作为普通文本
    elements.append({
        "text_run": {
            "content": text
        }
    })
    
    return elements


def language_to_code_lang(language: str) -> int:
    """代码块语言映射（飞书 API）"""
    mapping = {
        "mermaid": 42,  # mermaid（如果支持）
        "javascript": 6,
        "python": 22,
        "typescript": 28,
        "json": 9,
        "bash": 8,
        "css": 7,
        "html": 4,
        "sql": 27
    }
    return mapping.get(language.lower(), 1)  # 1 = plain text


def to_doc_api_payload(title: str, blocks: list[dict], folder_token: str = "") -> dict:
    """生成飞书创建文档的 API 调用参数"""
    return {
        "title": title,
        "folder_token": folder_token,
        "blocks": blocks[:500],  # 飞书限制每次最多 500 块
        "_meta": {
            "doc_type": "docx",
            "total_blocks": len(blocks)
        }
    }


def to_sdk_call_examples(payload: dict) -> str:
    """生成 SDK 调用示例代码"""
    return f"""
// Python SDK 调用示例（需要安装 lark-oapi）
// pip install lark-oapi

import lark_oapi as lark
from lark_oapi.api.docs.v1 import DocumentCreateRequest, DocumentCreateRequestBody, Block

# 读取生成的 JSON
with open('doc_payload.json', 'r') as f:
    payload = json.load(f)

# 构造请求
request = DocumentCreateRequest.builder()\\
    .request_body(
        DocumentCreateRequestBody.builder()
        .title(payload['title'])
        .folder_token(payload.get('folder_token', ''))
        .build()
    )\\
    .build()

# 发起调用（需要先初始化 client）
response = client.docs.v1.document.create(request)
print(response)


// curl 调用示例
# 1. 先获取 tenant_access_token
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \\
  -H "Content-Type: application/json" \\
  -d '{{"app_id":"YOUR_APP_ID","app_secret":"YOUR_APP_SECRET"}}'

# 2. 创建文档（用 doc_payload.json）
curl -X POST https://open.feishu.cn/open-apis/docs/v1/documents \\
  -H "Authorization: Bearer YOUR_TENANT_ACCESS_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d @doc_payload.json
"""


def main():
    parser = argparse.ArgumentParser(description="把 Markdown 转换为飞书文档 API 调用参数")
    parser.add_argument("input", help="Skill 输出的 Markdown 文件")
    parser.add_argument("--title", help="文档标题")
    parser.add_argument("--output", help="输出 JSON 文件")
    parser.add_argument("--folder-token", default="", help="目标文件夹 token")
    parser.add_argument("--show-sdk", action="store_true", help="显示 SDK 调用示例")
    
    args = parser.parse_args()
    
    # 读取
    raw = Path(args.input).read_text(encoding='utf-8')
    
    # 提取标题
    title = args.title
    if not title:
        title_match = re.search(r'^#\s+(.+)$', raw, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = "用户故事分析"
    
    # 解析
    blocks = parse_markdown_blocks(raw)
    api_payload = to_doc_api_payload(title, blocks, args.folder_token)
    
    # 输出
    output_json = json.dumps(api_payload, ensure_ascii=False, indent=2)
    
    if args.output:
        Path(args.output).write_text(output_json, encoding='utf-8')
        print(f"✅ 已生成：{args.output}")
        print(f"   标题: {title}")
        print(f"   块数: {len(blocks)}")
    else:
        print(output_json)
    
    if args.show_sdk:
        print()
        print("=" * 60)
        print("SDK 调用示例：")
        print("=" * 60)
        print(to_sdk_call_examples(api_payload))


if __name__ == "__main__":
    main()

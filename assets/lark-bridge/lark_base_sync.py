#!/usr/bin/env python3
"""
飞书多维表格（Base）同步工具

功能：
- 把 Skill 输出的 Story 列表转为飞书多维表格可导入的格式
- 支持生成 CSV（手动导入）或 JSON（API 批量写入）

使用方法：
1. 在飞书中创建多维表格（Base），添加 Story 表
3. 字段：Story ID / 标题 / 角色 / 想要 / 以便 / 优先级 / 故事点 / 状态
4. 用本工具生成 CSV → 在 Base 中导入
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any


# 飞书多维表格字段配置
BASE_FIELDS = [
    {"name": "Story ID", "type": "text", "required": True},
    {"name": "标题", "type": "text", "required": True},
    {"name": "角色", "type": "text"},
    {"name": "想要", "type": "long_text"},
    {"name": "以便", "type": "long_text"},
    {"name": "优先级", "type": "select", "options": ["P0", "P1", "P2", "P3"]},
    {"name": "故事点", "type": "number"},
    {"name": "Epic", "type": "text"},
    {"name": "状态", "type": "select", "options": ["待评审", "开发中", "已完成", "已搁置"]},
    {"name": "验收标准", "type": "long_text"},
    {"name": "备注", "type": "long_text"}
]


def parse_stories(raw: str) -> list[dict]:
    """从 Skill 输出中解析 Story 列表"""
    stories = []
    
    # 匹配 Story 块
    # 格式 1：作为 [X]，我想要 [Y]，以便 [Z]
    story_pattern = re.compile(
        r'【?Story\s+([\d\.]+)?】?\s*[:：]?\s*(.+?)\n'
        r'作为\s*\[(.+?)\][，,]\s*'
        r'我想要\s*\[(.+?)\][，,]\s*'
        r'以便\s*\[(.+?)\][。\.\n]?',
        re.MULTILINE | re.DOTALL
    )
    
    # 简化版本：找到所有 "作为 [X]，我想要 [Y]，以便 [Z]"
    simple_pattern = re.compile(
        r'(?:【?Story\s+([\d\.]+)?】?\s*[:：]?\s*(.+?)\n)?'
        r'作为\s*\[(.+?)\][，,]\s*'
        r'我想要\s*\[(.+?)\][，,]\s*'
        r'以便\s*\[(.+?)\]',
    )
    
    story_id_counter = 1
    for match in simple_pattern.finditer(raw):
        story_id = match.group(1) or f"STORY-{story_id_counter:03d}"
        title = match.group(2) or match.group(4)  # 优先用 Story 标题
        role = match.group(3).strip()
        want = match.group(4).strip()
        benefit = match.group(5).strip()
        
        # 提取优先级和故事点
        priority = extract_priority(raw, match.start())
        story_points = extract_story_points(raw, match.start())
        
        # 提取验收标准（在 Story 范围内）
        ac = extract_ac(raw, match.end())
        
        stories.append({
            "Story ID": story_id,
            "标题": title.strip() if title else want[:30],
            "角色": role,
            "想要": want,
            "以便": benefit,
            "优先级": priority,
            "故事点": story_points,
            "Epic": "",
            "状态": "待评审",
            "验收标准": ac,
            "备注": ""
        })
        story_id_counter += 1
    
    return stories


def find_story_block_end(raw: str, position: int) -> int:
    """找到当前 Story 块的结束位置"""
    next_boundary = re.search(r'\n【?Story\s|\n##\s', raw[position:])
    if next_boundary:
        return position + next_boundary.start()
    return min(position + 1000, len(raw))


def extract_priority(raw: str, position: int) -> str:
    """从 Story 块内提取优先级"""
    end = find_story_block_end(raw, position)
    block = raw[position:end]
    
    m = re.search(r'【优先级】\s*(P[0-3])', block)
    if m:
        return m.group(1)
    return 'P2'  # 默认


def extract_story_points(raw: str, position: int) -> str:
    """从 Story 块内提取故事点"""
    end = find_story_block_end(raw, position)
    block = raw[position:end]
    
    m = re.search(r'【故事点】\s*(\d+)', block)
    if m:
        return m.group(1)
    return ''


def extract_ac(raw: str, position: int) -> str:
    """从 Story 之后提取验收标准"""
    # 找到下一个 Story 或下一个 ##
    next_story = re.search(r'\n【?Story|##\s', raw[position:])
    end = position + next_story.start() if next_story else min(position + 1000, len(raw))
    
    section = raw[position:end]
    
    # 找所有以 ✅ 或 - 开头的 AC
    ac_pattern = re.compile(r'[✅\-\*]\s+(Given[\s\S]+?)(?=\n\n|\n[✅\-\*]|\Z)', re.MULTILINE)
    acs = []
    for m in ac_pattern.finditer(section):
        acs.append(m.group(1).strip())
    
    return '\n'.join(acs)


def to_base_records(stories: list[dict]) -> list[dict]:
    """转换为飞书多维表格记录格式"""
    records = []
    for story in stories:
        record = {"fields": story}
        records.append(record)
    return records


def to_csv(records: list[dict]) -> str:
    """生成 CSV（用于手动导入飞书多维表格）"""
    if not records:
        return ""
    
    fieldnames = [f["name"] for f in BASE_FIELDS]
    output = []
    
    writer = csv.DictWriter(
        sys.stdout if True else open('/dev/null', 'w'),
        fieldnames=fieldnames
    )
    
    # 写入表头
    output.append(','.join(fieldnames))
    
    # 写入记录
    for record in records:
        row = []
        for field in fieldnames:
            value = str(record['fields'].get(field, ''))
            # CSV 转义
            if ',' in value or '"' in value or '\n' in value:
                value = '"' + value.replace('"', '""') + '"'
            row.append(value)
        output.append(','.join(row))
    
    return '\n'.join(output)


def to_batch_create_payload(records: list[dict], app_token: str, table_id: str) -> dict:
    """生成批量写入 API 调用参数"""
    return {
        "app_token": app_token,
        "table_id": table_id,
        "records": records,
        "_meta": {
            "total_records": len(records),
            "fields_definition": BASE_FIELDS
        }
    }


def main():
    parser = argparse.ArgumentParser(description="把 Skill Story 转为飞书多维表格格式")
    parser.add_argument("input", help="Skill 输出的 Markdown 文件")
    parser.add_argument("--format", choices=['csv', 'json', 'api'], default='csv', help="输出格式")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--app-token", default="YOUR_APP_TOKEN", help="飞书 Base app token")
    parser.add_argument("--table-id", default="YOUR_TABLE_ID", help="飞书 Base table ID")
    
    args = parser.parse_args()
    
    # 读取
    raw = Path(args.input).read_text(encoding='utf-8')
    
    # 解析
    stories = parse_stories(raw)
    
    if not stories:
        print("⚠️  未找到 Story")
        print("   请检查 Markdown 中是否包含：作为 [X]，我想要 [Y]，以便 [Z]")
        sys.exit(0)
    
    records = to_base_records(stories)
    
    # 输出
    if args.format == 'csv':
        output_text = to_csv(records)
        if args.output:
            Path(args.output).write_text(output_text, encoding='utf-8')
            print(f"✅ CSV 已生成：{args.output}")
        else:
            print(output_text)
    elif args.format == 'json':
        output_json = json.dumps(records, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(output_json, encoding='utf-8')
            print(f"✅ JSON 已生成：{args.output}")
        else:
            print(output_json)
    elif args.format == 'api':
        payload = to_batch_create_payload(records, args.app_token, args.table_id)
        output_json = json.dumps(payload, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(output_json, encoding='utf-8')
            print(f"✅ API Payload 已生成：{args.output}")
        else:
            print(output_json)
    
    # 统计
    print(f"\n📊 统计：")
    print(f"   Story 数：{len(stories)}")
    if stories:
        priorities = {}
        for s in stories:
            p = s.get("优先级", "P2")
            priorities[p] = priorities.get(p, 0) + 1
        print(f"   优先级分布：{priorities}")


if __name__ == "__main__":
    main()

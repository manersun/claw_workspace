#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快手视频直播 Arya 日志数据查询工具
查询直播流调试日志和质量指标

Usage:
    python query_arya_log.py --stream-id "ps86J2LkzJA" [options]
"""

import argparse
import json
import sys
import os
from datetime import datetime
from pathlib import Path
import requests
from typing import Optional, List, Dict, Any


# API 配置
API_HOST = "video-data.corp.kuaishou.com"
API_PATH = "/api/template/query"
DEFAULT_TEMPLATE = "video_live_intelligent_debug_arya_log_data"
DEFAULT_FILTER = "reportFlag = 1"


def build_params(
    stream_id: str,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    extra_filter: str = DEFAULT_FILTER
) -> List[Dict[str, str]]:
    """构建查询参数"""
    now = int(datetime.now().timestamp() * 1000)
    one_hour_ago = now - 3600000
    
    params = [
        {"name": "stream_id", "value": stream_id},
        {"name": "start_timestamp", "value": str(start_time or one_hour_ago)},
        {"name": "end_timestamp", "value": str(end_time or now)},
        {"name": "start_client_timestamp", "value": str(start_time or one_hour_ago)},
        {"name": "end_client_timestamp", "value": str(end_time or now)},
        {"name": "extra_filter", "value": extra_filter}
    ]
    
    return params


def query_arya_log(
    stream_id: str,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    extra_filter: str = DEFAULT_FILTER,
    template_name: str = DEFAULT_TEMPLATE
) -> Dict[str, Any]:
    """
    查询 Arya 日志数据
    
    Args:
        stream_id: 直播流 ID
        start_time: 开始时间戳（毫秒）
        end_time: 结束时间戳（毫秒）
        extra_filter: 额外过滤条件
        template_name: 查询模板名
    
    Returns:
        API 响应数据
    """
    url = f"https://{API_HOST}{API_PATH}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "params": build_params(stream_id, start_time, end_time, extra_filter),
        "templateName": template_name
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(
            f"Connection failed. This API requires internal network access.\n{e}"
        )
    except requests.exceptions.Timeout:
        raise TimeoutError("Request timeout. Please try again.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"HTTP error: {e}")


def format_table(data: Dict[str, Any], max_rows: int = 20) -> str:
    """格式化为表格输出"""
    lines = []
    
    # 表头
    lines.append("┌─────────────────────┬──────────────┬──────────────┬─────────────┐")
    lines.append("│ 字段                │ 值           │ 类型         │ 说明        │")
    lines.append("├─────────────────────┼──────────────┼──────────────┼─────────────┤")
    
    # 数据行
    if "data" in data and isinstance(data["data"], list):
        for i, row in enumerate(data["data"][:max_rows]):
            if isinstance(row, dict):
                for key, value in list(row.items())[:3]:
                    value_str = str(value)[:12]
                    type_str = type(value).__name__[:12]
                    lines.append(f"│ {key:<19} │ {value_str:<12} │ {type_str:<12} │             │")
            else:
                lines.append(f"│ {str(row)[:60]:<60} │             │")
        
        if len(data["data"]) > max_rows:
            lines.append(f"│ ... (共 {len(data['data'])} 条记录) ...                                │")
    
    lines.append("└─────────────────────┴──────────────┴──────────────┴─────────────┘")
    
    return "\n".join(lines)


def print_result(data: Dict[str, Any], output_format: str = "table"):
    """打印结果"""
    if output_format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif output_format == "table":
        print(format_table(data))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="快手视频直播 Arya 日志数据查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python query_arya_log.py --stream-id "ps86J2LkzJA"
  python query_arya_log.py --stream-id "xxx" --start-time 1772379600000 --end-time 1772380200000
  python query_arya_log.py --stream-id "xxx" --output json
        """
    )
    
    parser.add_argument(
        "--stream-id",
        type=str,
        required=True,
        help="直播流 ID (必需)"
    )
    
    parser.add_argument(
        "--start-time",
        type=int,
        help="查询开始时间戳（毫秒）"
    )
    
    parser.add_argument(
        "--end-time",
        type=int,
        help="查询结束时间戳（毫秒）"
    )
    
    parser.add_argument(
        "--extra-filter",
        type=str,
        default=DEFAULT_FILTER,
        help=f"额外过滤条件 (默认：{DEFAULT_FILTER})"
    )
    
    parser.add_argument(
        "--template",
        type=str,
        default=DEFAULT_TEMPLATE,
        help=f"查询模板名 (默认：{DEFAULT_TEMPLATE})"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        choices=["table", "json"],
        default="table",
        help="输出格式 (默认：table)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细信息"
    )
    
    args = parser.parse_args()
    
    try:
        if args.verbose:
            print(f"🔍 查询流 ID: {args.stream_id}")
            print(f"📅 时间范围：{args.start_time} - {args.end_time}")
            print(f"🔧 过滤条件：{args.extra_filter}")
            print(f"📋 模板：{args.template}")
            print()
        
        # 执行查询
        result = query_arya_log(
            stream_id=args.stream_id,
            start_time=args.start_time,
            end_time=args.end_time,
            extra_filter=args.extra_filter,
            template_name=args.template
        )
        
        # 输出结果
        print_result(result, args.output)
        
        # 保存日志
        log_file = Path.home() / ".openclaw" / "arya-log-query.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "a") as f:
            f.write(f"{datetime.now().isoformat()} - Query stream_id={args.stream_id}\n")
        
    except ValueError as e:
        print(f"❌ 参数错误：{e}", file=sys.stderr)
        sys.exit(1)
    except ConnectionError as e:
        print(f"❌ 连接错误：{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 查询失败：{e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

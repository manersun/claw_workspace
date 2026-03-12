#!/usr/bin/env python3
"""
直播监控脚本 - 每 5 分钟查询直播数据并发送 QQ 告警
"""

import sys
import os
import json
import time
import requests
from datetime import datetime

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

STREAM_ID = "EzCcbKcPEns"
QQ_USER_ID = "3812303292"  # 从之前数据获取

API_URL = "http://video-data.corp.kuaishou.com/api/template/query"
TEMPLATE_NAME = "video_live_intelligent_debug_arya_log_data"

def get_timestamp_ms():
    """获取当前时间戳 (毫秒)"""
    return int(time.time() * 1000)

def query_arya_log(stream_id, start_time, end_time):
    """查询 Arya 日志数据"""
    payload = {
        "params": [
            {"name": "stream_id", "value": stream_id},
            {"name": "start_timestamp", "value": start_time},
            {"name": "end_timestamp", "value": end_time},
            {"name": "start_client_timestamp", "value": start_time},
            {"name": "end_client_timestamp", "value": end_time},
            {"name": "extra_filter", "value": "reportFlag = 1"}
        ],
        "templateName": TEMPLATE_NAME
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

def analyze_data(data):
    """分析直播数据，返回问题和告警级别"""
    issues = []
    warnings = []
    
    if not data.get('data') or not data['data'].get('data'):
        return {"status": "no_data", "issues": ["无数据返回"], "warnings": []}
    
    records = data['data']['data']
    
    for record in records:
        # 检查错误码
        err_code = record.get('errCode', '')
        if err_code and err_code != '0':
            issues.append(f"错误码：{err_code}")
        
        # 检查帧率
        enc_fps = record.get('vtxEncFps', 0)
        cap_fps = record.get('vtxCapFps', 0)
        target_fps = 30
        
        if enc_fps < target_fps * 0.7:  # 低于目标 70%
            issues.append(f"编码帧率偏低：{enc_fps}fps (目标{target_fps}fps)")
        elif enc_fps < target_fps * 0.9:
            warnings.append(f"编码帧率略低：{enc_fps}fps")
        
        if cap_fps > enc_fps * 1.2:  # 捕获比编码高 20% 以上
            warnings.append(f"编码瓶颈：捕获{cap_fps}fps > 编码{enc_fps}fps")
        
        # 检查码率
        enc_kbps = record.get('vtxEncKbps', 0)
        target_kbps = record.get('vtxTgtBr', 10000)
        
        if enc_kbps < target_kbps * 0.5:  # 低于目标 50%
            issues.append(f"码率偏低：{enc_kbps}kbps (目标{target_kbps}kbps)")
        
        # 检查编码重启
        restart_cnt = record.get('vtxEncRestartCnt', 0)
        if restart_cnt > 5:
            issues.append(f"编码重启次数过多：{restart_cnt}")
        
        # 检查编码回退
        fallback = record.get('vtxEncFallback', 0)
        if fallback > 0:
            issues.append(f"编码回退发生：{fallback}次")
        
        # 检查设备温度
        device_temp = record.get('deviceTemp', '0')
        try:
            device_temp_num = float(device_temp) if device_temp else 0
            if device_temp_num > 45000:  # 假设单位是 0.001 度
                warnings.append(f"设备温度偏高：{device_temp_num/1000:.1f}°C")
        except (ValueError, TypeError):
            pass
        
        # 检查应用状态
        app_state = record.get('appState', '0')
        if app_state != '0':
            issues.append(f"应用状态异常：{app_state}")
    
    return {
        "status": "ok" if not issues else "warning",
        "issues": issues,
        "warnings": warnings,
        "record_count": len(records)
    }

def format_qq_message(analysis, data):
    """格式化 QQ 消息"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if analysis['status'] == 'no_data':
        return f"""⚠️ 直播监控告警

📺 直播 ID: {STREAM_ID}
⏰ 时间：{now}
❌ 状态：无数据返回

请检查直播是否正常推流。"""
    
    if not analysis['issues'] and not analysis['warnings']:
        return None  # 正常不发送
    
    # 获取最新数据点
    latest = data['data']['data'][0] if data.get('data') and data['data'].get('data') else {}
    
    msg = f"""{'🚨' if analysis['issues'] else '⚠️'} 直播监控告警

📺 直播 ID: `{STREAM_ID}`
⏰ 时间：{now}
📊 数据点：{analysis.get('record_count', 0)}个"""

    if analysis['issues']:
        msg += "\n\n【严重问题】\n"
        for issue in analysis['issues']:
            msg += f"❌ {issue}\n"
    
    if analysis['warnings']:
        msg += "\n【警告】\n"
        for warn in analysis['warnings']:
            msg += f"⚠️ {warn}\n"
    
    # 添加关键指标
    if latest:
        msg += f"""
【关键指标】
📹 编码帧率：{latest.get('vtxEncFps', 'N/A')}fps
📡 编码码率：{latest.get('vtxEncKbps', 'N/A')}kbps
🎥 捕获帧率：{latest.get('vtxCapFps', 'N/A')}fps
🔧 编码重启：{latest.get('vtxEncRestartCnt', 'N/A')}次
"""
    
    msg += "\n请及时检查直播状态！"
    
    return msg

def send_qq_message(message):
    """通过 QQ 发送消息"""
    if not message:
        return {"status": "skipped", "reason": "无消息需要发送"}
    
    # 使用 OpenClaw message 工具的方式
    # 这里输出消息，由调用方处理
    print(f"QQ_MESSAGE:{message}")
    return {"status": "sent"}

def main():
    """主函数"""
    print(f"[{datetime.now().isoformat()}] 开始监控直播 {STREAM_ID}")
    
    # 计算时间范围 (最近 5 分钟)
    end_time = get_timestamp_ms()
    start_time = end_time - 5 * 60 * 1000  # 5 分钟前
    
    print(f"查询时间范围：{start_time} - {end_time}")
    
    # 查询数据
    result = query_arya_log(STREAM_ID, start_time, end_time)
    
    if result.get('status') == 'error':
        error_msg = f"❌ 查询失败：{result.get('message', '未知错误')}"
        print(error_msg)
        send_qq_message(error_msg)
        return 1
    
    # 分析数据
    analysis = analyze_data(result)
    print(f"分析结果：{json.dumps(analysis, ensure_ascii=False, indent=2)}")
    
    # 发送 QQ 消息
    qq_message = format_qq_message(analysis, result)
    result_msg = send_qq_message(qq_message)
    
    print(f"QQ 发送结果：{result_msg}")
    
    if analysis['status'] == 'ok' and not analysis['warnings']:
        print("✅ 直播状态正常，无需告警")
        return 0
    elif analysis['issues']:
        print("🚨 发现严重问题，已发送告警")
        return 2
    else:
        print("⚠️ 发现警告，已发送通知")
        return 1

if __name__ == '__main__':
    sys.exit(main())

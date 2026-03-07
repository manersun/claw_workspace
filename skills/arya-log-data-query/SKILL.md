---
name: arya-log-data-query
description: 查询快手视频直播 Arya 调试日志数据（内部 API）。使用场景：(1) 查询直播间智能调试日志 (2) 分析直播流质量指标 (3) 监控直播异常事件。支持自定义时间范围、流 ID、过滤条件。需要内网访问和有效 Cookie。
---

# Arya 日志数据查询技能

## 快速开始

```bash
# 基础查询
python scripts/query_arya_log.py --stream-id "ps86J2LkzJA"

# 指定时间范围
python scripts/query_arya_log.py \
  --stream-id "ps86J2LkzJA" \
  --start-time 1772379600000 \
  --end-time 1772380200000

# 自定义过滤条件
python scripts/query_arya_log.py \
  --stream-id "ps86J2LkzJA" \
  --extra-filter "reportFlag = 1"

# 输出 JSON 格式
python scripts/query_arya_log.py --stream-id "xxx" --output json
```

## 配置

### 必需参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--stream-id` | 直播流 ID | `ps86J2LkzJA` |

### 可选参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--start-time` | 查询开始时间戳（毫秒） | 当前时间 -1 小时 |
| `--end-time` | 查询结束时间戳（毫秒） | 当前时间 |
| `--extra-filter` | 额外过滤条件 | `reportFlag = 1` |
| `--template` | 查询模板名 | `video_live_intelligent_debug_arya_log_data` |
| `--output` | 输出格式 | `table` |
| `--cookie` | Cookie 文件路径 | `~/.openclaw/arya-log-cookie.txt` |

### Cookie 配置

**方法 1：环境变量**
```bash
export ARYA_LOG_COOKIE="apdid=...; accessproxy_session=..."
```

**方法 2：配置文件**
```bash
# 创建 Cookie 文件
echo "apdid=...; accessproxy_session=..." > ~/.openclaw/arya-log-cookie.txt
```

**方法 3：命令行参数**
```bash
python scripts/query_arya_log.py --stream-id "xxx" --cookie "/path/to/cookie.txt"
```

## API 详情

**接口地址：** `video-data.corp.kuaishou.com/api/template/query`

**请求方式：** POST

**请求头：**
```
Content-Type: application/json
Cookie: <your_cookie>
```

**请求体：**
```json
{
  "params": [
    {"name": "stream_id", "value": "ps86J2LkzJA"},
    {"name": "start_timestamp", "value": 1772379600000},
    {"name": "end_timestamp", "value": 1772380200000},
    {"name": "start_client_timestamp", "value": 1772379600000},
    {"name": "end_client_timestamp", "value": 1772380200000},
    {"name": "extra_filter", "value": "reportFlag = 1"}
  ],
  "templateName": "video_live_intelligent_debug_arya_log_data"
}
```

## 使用场景

### 1. 直播质量分析

```bash
# 查询特定直播流的调试日志
python scripts/query_arya_log.py \
  --stream-id "ps86J2LkzJA" \
  --start-time 1772379600000 \
  --end-time 1772380200000 \
  --extra-filter "reportFlag = 1"
```

### 2. 定时监控

```bash
# 添加到 crontab，每 5 分钟查询一次
*/5 * * * * cd /path/to/skills/arya-log-data-query && \
  python scripts/query_arya_log.py \
    --stream-id "your_stream_id" \
    --output json >> /var/log/arya-log.log
```

### 3. 数据分析

```bash
# 导出 JSON 用于后续分析
python scripts/query_arya_log.py \
  --stream-id "ps86J2LkzJA" \
  --output json > data.json

# 用 jq 处理
cat data.json | jq '.data[] | select(.error_count > 0)'
```

## 错误处理

### 常见错误

**错误 1：Cookie 过期**
```
Error: Authentication failed. Cookie may be expired.
解决：更新 Cookie 文件
```

**错误 2：内网访问限制**
```
Error: Connection timeout. This API requires internal network access.
解决：确保在公司内网或通过 VPN 访问
```

**错误 3：流 ID 不存在**
```
Error: Stream ID not found: xxx
解决：检查流 ID 是否正确
```

## 相关技能

- `video-frames` - 视频帧提取
- `healthcheck` - 系统健康检查
- `github` - 代码管理

## 安全说明

⚠️ **重要：**

1. **Cookie 包含敏感信息**，不要提交到 Git
2. **内网 API**，仅限公司内部使用
3. **不要分享**你的 Cookie 给外部人员
4. 建议将 Cookie 文件添加到 `.gitignore`

## 维护

**更新 Cookie：**
```bash
# 从浏览器复制最新 Cookie
echo "apdid=...; accessproxy_session=..." > ~/.openclaw/arya-log-cookie.txt
```

**查看日志：**
```bash
tail -f ~/.openclaw/arya-log-query.log
```

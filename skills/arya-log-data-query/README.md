# Arya Log Data Query Skill

快手视频直播 Arya 日志数据查询工具。

## 快速开始

### 1. 安装依赖

```bash
cd scripts
pip install -r requirements.txt
```

### 2. 运行查询

```bash
# 基础查询
python scripts/query_arya_log.py --stream-id "ps86J2LkzJA"

# 指定时间范围
python scripts/query_arya_log.py \
  --stream-id "ps86J2LkzJA" \
  --start-time 1772379600000 \
  --end-time 1772380200000

# JSON 输出
python scripts/query_arya_log.py --stream-id "xxx" --output json
```

## 参数说明

| 参数 | 必需 | 说明 |
|------|------|------|
| `--stream-id` | ✅ | 直播流 ID |
| `--start-time` | ❌ | 开始时间戳（毫秒） |
| `--end-time` | ❌ | 结束时间戳（毫秒） |
| `--extra-filter` | ❌ | 过滤条件 |
| `--template` | ❌ | 查询模板名 |
| `--output` | ❌ | 输出格式 (table/json) |

## 注意事项

⚠️ **重要：**
- 需要内网访问（video-data.corp.kuaishou.com）
- 无需配置 Cookie，直接调用

## 错误排查

**连接失败：**
- 确保在公司内网
- 检查是否可以访问 video-data.corp.kuaishou.com

**流 ID 不存在：**
- 检查流 ID 是否正确

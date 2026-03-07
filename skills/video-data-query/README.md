# 视频数据查询 Skill

快手内部视频直播数据查询工具。

## 快速开始

### 1. 安装依赖

```bash
cd scripts
pip install -r requirements.txt
```

### 2. 配置 Cookie

**方法 1：环境变量（推荐）**
```bash
export VIDEO_DATA_COOKIE="apdid=...; accessproxy_session=..."
```

**方法 2：配置文件**
```bash
echo "apdid=...; accessproxy_session=..." > ~/.openclaw/video-data-cookie.txt
```

### 3. 运行查询

```bash
# 基础查询
python scripts/query_video_data.py --stream-id "eXkmWrpRCdU"

# 指定时间范围
python scripts/query_video_data.py \
  --stream-id "eXkmWrpRCdU" \
  --start-time 1772013000000 \
  --end-time 1772013600000

# JSON 输出
python scripts/query_video_data.py --stream-id "xxx" --output json
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
- 需要内网访问
- Cookie 包含敏感信息，不要提交到 Git
- Cookie 会过期，需定期更新

## 更新 Cookie

从浏览器复制最新 Cookie：
```bash
echo "apdid=...; accessproxy_session=..." > ~/.openclaw/video-data-cookie.txt
```

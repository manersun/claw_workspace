---
name: toutiao-news-monitor
description: 定时爬取今日头条新闻并推送到指定渠道。使用场景：(1) 监控特定关键词的最新新闻 (2) 定时推送新闻摘要到 QQ/Telegram (3) 保存新闻数据到 JSON/CSV。支持自定义关键词、爬取频率、推送渠道。
---

# 今日头条新闻监控技能

## 快速开始

运行爬虫并推送新闻：

```bash
# 基础用法（爬取并保存）
python scripts/crawl_news.py --keyword "美国 伊朗" --save

# 推送到 QQ
python scripts/crawl_news.py --keyword "美国 伊朗" --push-qq <openid>

# 推送到 Telegram
python scripts/crawl_news.py --keyword "美国 伊朗" --push-telegram <chat_id>
```

## 配置参数

### 必需参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--keyword` | 搜索关键词 | `"美国 伊朗 战争"` |
| `--save` | 保存数据到文件 | `--save` |

### 可选参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--push-qq` | 推送 QQ 号（openid） | 不推送 |
| `--push-telegram` | 推送 Telegram 聊天 ID | 不推送 |
| `--max-pages` | 最多爬取页数 | 2 |
| `--delay` | 请求间隔（秒） | 2 |

## 定时执行

### 方法 1：使用系统 cron

```bash
# 编辑 crontab
crontab -e

# 每 2 小时执行一次
0 */2 * * * cd /Users/sunyu.maner/.openclaw/workspace/skills/toutiao-news-monitor && python scripts/crawl_news.py --keyword "美国 伊朗" --save
```

### 方法 2：使用 OpenClaw 定时任务

在 `~/.openclaw/cron/` 创建任务：

```bash
# 创建定时任务
mkdir -p ~/.openclaw/cron
cat > ~/.openclaw/cron/news-monitor.json << 'EOF'
{
  "schedule": "0 */2 * * *",
  "command": "python /Users/sunyu.maner/.openclaw/workspace/skills/toutiao-news-monitor/scripts/crawl_news.py",
  "args": ["--keyword", "美国 伊朗", "--push-qq", "063A5CF23D86E5BCE5BA7BB48E9B0773"],
  "enabled": true
}
EOF
```

## 输出文件

爬取后生成：

- `data/news_YYYYMMDD_HHMMSS.json` - 完整数据
- `data/news_YYYYMMDD_HHMMSS.csv` - 表格数据
- `logs/crawl.log` - 爬取日志

## 推送格式

### QQ 推送

```
🕷️ 美伊战争最新消息

🔴 美以袭击伊朗第 8 天，伊朗发射超重型导弹复仇
📰 来源：大象新闻 | ⏰ 4 小时前
🔗 https://www.toutiao.com/article/...
```

### Telegram 推送

格式类似，支持 Markdown 渲染。

## 故障排查

### 爬取不到数据

- 检查网络连接
- 增加 `--delay` 参数
- 更换关键词

### 推送失败

- QQ：确认 openid 正确（32 位十六进制）
- Telegram：确认 bot token 配置
- 检查渠道是否启用

## 相关技能

- `github` - 提交数据到 GitHub
- `weather` - 获取天气信息
- `healthcheck` - 系统健康检查

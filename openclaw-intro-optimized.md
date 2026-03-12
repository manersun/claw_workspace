# OpenClaw 完全指南 🦞

> **运行在你自己设备上的个人 AI 助理，拥有完整系统控制能力**

---

## 🚀 30 秒速读

### OpenClaw 是什么？

OpenClaw 是一款运行在**您自己的设备上**的**个人 AI 助理**，拥有**完整系统控制能力**。它是 GitHub 上面的开源项目，能够操作你的文件、浏览器、终端、消息应用等。

### 核心亮点

| 指标 | 数据 |
|------|------|
| 🏆 GitHub Stars | 25 万+ (历史第一) |
| ⚡ 原型到发布 | 1 小时 |
| 🌍 单周访问量 | 200 万+ |
| 🇨🇳 中国用户占比 | 超 50% |
| 📅 项目启动 | 2025 年 11 月 |

### 适合谁？

- ✅ 想用 AI 自动化日常任务
- ✅ 想控制自己的 AI 数据 (本地运行)
- ✅ 想扩展 AI 能力 (爬虫/文件/消息/浏览器)
- ✅ 开发者和技术爱好者

### 快速开始

```bash
# 一行命令安装
curl -fsSL https://openclaw.ai/install.sh | bash

# 或使用 Homebrew (macOS)
brew install openclaw
```

---

## 1. 源起 🦞

### 时间轴

| 时间 | 事件 |
|------|------|
| 2025.04 | Peter 开始探索 AI Agent |
| 2025.11 | Claude Opus 4.5 发布，项目迎来质变 |
| 2025.11 | OpenClaw 项目发起 |
| 2026.01 | GitHub 发布，首周 13.8 万 stars |
| 2026.02 | Peter 加入 OpenAI |
| 2026.03 | 突破 25 万 stars，GitHub 历史第一 |

### 关键洞察

> Steinberger 借助 Claude Code CLI 连接 WhatsApp 的能力，敏锐地意识到该技术可拓展至更广泛的应用场景，并据此快速构建出 OpenClaw 原型。

**💡 启示**: 机遇往往近在咫尺，关键在于发现机遇的洞察力 + 转化为成果的行动力。

### 关于作者

**Peter Steinberger** | [@steipete](https://x.com/steipete)

| 维度 | 详情 |
|------|------|
| 国籍 | 奥地利 |
| 教育 | 维也纳科技大学 计算机与信息科学 |
| 创业 | 2011 年创立 PSPDFKit (PDF 处理技术) |
| AI 探索 | 2025.06 成立 Amantus Machina |
| OpenClaw | 2025.11 发起 |
| 新起点 | 2026.02 加入 OpenAI |

**核心能力**: PDF 技术 × AI Agent × 开源社区

---

## 2. 知面 — OpenClaw 是什么 🎭

### 定义

**OpenClaw** 是一款运行在**您自己的设备上**的、拥有**完整系统控制能力**的**个人 AI 助理**。

### 核心能力

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw 能力矩阵                      │
├─────────────────────────────────────────────────────────┤
│  📁 文件系统   │  读取/写入/编辑/搜索/组织文件            │
│  🌐 浏览器     │  打开网页/截图/提取内容/自动化操作        │
│  💻 终端       │  执行命令/运行脚本/管理进程              │
│  💬 消息       │  WhatsApp/Telegram/QQ/Discord/微信       │
│  🔧 工具调用   │  内置 20+ Tools (搜索/天气/Git/...)      │
│  🧠 技能扩展   │  Skill 化插件架构，社区贡献技能           │
│  📅 定时任务   │  Cron 调度/心跳检查/自动提醒             │
│  🎙️ 语音       │  TTS 语音合成/语音消息                  │
└─────────────────────────────────────────────────────────┘
```

### 使用场景

| 场景 | 示例 |
|------|------|
| **信息获取** | "搜索最近的 AI 新闻，总结成 3 点" |
| **文件处理** | "把 Downloads 里的 PDF 整理到 Documents" |
| **自动化** | "每天早上 9 点检查邮件并摘要" |
| **内容创作** | "帮我写一篇小红书笔记，主题是 XXX" |
| **代码辅助** | "检查这个项目的 git 状态并提交变更" |
| **数据爬取** | "爬取 XX 网站的数据，保存为 CSV" |

### 核心优势

| 优势 | 说明 |
|------|------|
| 🔒 **隐私安全** | 运行在本地，数据不出设备 |
| ⚡ **响应迅速** | 无网络延迟，直接操作系统 |
| 🔧 **深度集成** | 文件/终端/浏览器/消息全打通 |
| 🧩 **可扩展** | Skill 化架构，无限扩展能力 |
| 💰 **成本可控** | 只付模型 API 费用，无订阅费 |
| 🌍 **多平台** | macOS/Windows/Linux 全支持 |

---

## 3. 知心 — 架构与组件 ⚙️

### 整体架构

```
┌──────────────────────────────────────────────────────────┐
│                     用户 (自然语言)                        │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│                    OpenClaw Agent                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐ │
│  │  会话管理   │  │  记忆系统   │  │  决策引擎          │ │
│  └────────────┘  └────────────┘  └────────────────────┘ │
└────────────────────┬─────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Tools     │ │   Skills    │ │   Plugins   │
│  (内置能力)  │ │  (技能包)    │ │  (扩展插件)  │
└─────────────┘ └─────────────┘ └─────────────┘
         │           │           │
         └───────────┼───────────┘
                     ▼
┌──────────────────────────────────────────────────────────┐
│                    操作系统层                              │
│  文件系统 │ 浏览器 │ 终端 │ 消息应用 │ 网络 │ 设备        │
└──────────────────────────────────────────────────────────┘
```

### 核心组件

#### 3.1 Gateway (网关)

**作用**: OpenClaw 的"大脑"，负责会话管理、工具调度、消息路由

**配置**: `~/.openclaw/openclaw.json`

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "auth": {
      "mode": "token",
      "token": "xxx"
    }
  }
}
```

#### 3.2 Tools (工具)

**内置原子能力**，直接由 OpenClaw 运行时提供：

| Tool | 用途 |
|------|------|
| `read` / `write` / `edit` | 文件操作 |
| `exec` / `process` | 命令执行 |
| `web_search` / `web_fetch` | 网络访问 |
| `browser` | 浏览器控制 |
| `message` | 消息发送 |
| `cron` | 定时任务 |
| `memory_search` / `memory_get` | 记忆系统 |
| `sessions_spawn` / `subagents` | 子 Agent 管理 |

#### 3.3 Skills (技能)

**基于 Tools 封装的高级任务模块**，可扩展：

| Skill | 功能 |
|-------|------|
| `weather` | 天气查询 |
| `github` | GitHub 操作 |
| `n8n` | n8n 工作流管理 |
| `xhs` | 小红书内容创作 |
| `summarize` | 内容摘要 |
| `healthcheck` | 系统安全检查 |

**位置**: `~/.openclaw/workspace/skills/`

#### 3.4 Memory (记忆系统)

**长期记忆** + **短期记忆** 双层结构：

```
~/.openclaw/workspace/
├── MEMORY.md              # 长期记忆 ( curated )
└── memory/
    ├── 2026-03-11.md      # 每日日志
    ├── 2026-03-12.md      # 今日日志
    └── ...
```

#### 3.5 Channels (通信渠道)

支持多种消息平台：

| Channel | 状态 |
|---------|------|
| Web Chat | ✅ 内置 |
| QQ Bot | ✅ 插件 |
| Telegram | ✅ 插件 |
| WhatsApp | ✅ 插件 |
| Discord | ✅ 插件 |
| Slack | ✅ 插件 |

---

## 4. 知用 — 部署与配置 🛠️

### 4.1 安装

#### macOS (Homebrew)

```bash
brew install openclaw
```

#### 通用 (curl)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

#### 验证安装

```bash
openclaw --version
openclaw status
```

### 4.2 首次配置

#### 步骤 1: 启动向导

```bash
openclaw onboard
```

#### 步骤 2: 配置模型

编辑 `~/.openclaw/openclaw.json`:

```json
{
  "models": {
    "providers": {
      "bailian": {
        "baseUrl": "https://dashscope.aliyuncs.com/v1",
        "apiKey": "sk-xxx",
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "qwen3.5-plus",
            "contextWindow": 1000000
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian/qwen3.5-plus"
      }
    }
  }
}
```

#### 步骤 3: 配置通信渠道 (可选)

**QQ Bot**:

```json
{
  "channels": {
    "qqbot": {
      "enabled": true,
      "appId": "102924452",
      "clientSecret": "xxx"
    }
  }
}
```

#### 步骤 4: 重启 Gateway

```bash
openclaw gateway restart
```

### 4.3 工作区文件

```
~/.openclaw/workspace/
├── AGENTS.md           # 行为规范
├── SOUL.md             # 人格定义
├── USER.md             # 用户信息
├── IDENTITY.md         # 身份卡片
├── TOOLS.md            # 环境配置
├── HEARTBEAT.md        # 心跳任务
├── MEMORY.md           # 长期记忆
├── openclaw.json       # (可选) 本地配置
└── memory/
    └── YYYY-MM-DD.md   # 每日日志
```

### 4.4 常用命令

```bash
# 状态检查
openclaw status
openclaw doctor

# Gateway 管理
openclaw gateway start
openclaw gateway stop
openclaw gateway restart

# 配置管理
openclaw config get
openclaw config patch

# 插件管理
openclaw plugins list
openclaw plugins install <plugin>

# 技能管理
skillhub search <keyword>
skillhub install <skill>
skillhub list

# 会话管理
openclaw sessions list
```

---

## 5. 实战 — 完整案例 📖

### 案例：新闻爬取 → 总结 → QQ 推送

#### 5.1 创建爬虫技能

```bash
cd ~/.openclaw/workspace/skills
mkdir news-crawler
```

创建 `SKILL.md`:

```markdown
---
name: news-crawler
description: 爬取科技新闻并总结
---

# News Crawler

爬取指定网站的科技新闻，提取标题、摘要、链接。
```

创建 `script.py`:

```python
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def fetch_news(url='https://example.com'):
    """爬取新闻列表"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_list = []
    for item in soup.select('.news-item'):
        news_list.append({
            'title': item.select_one('.title').text,
            'link': item.select_one('a')['href'],
            'time': item.select_one('.time').text
        })
    
    return news_list

if __name__ == '__main__':
    news = fetch_news()
    print(f"爬取到 {len(news)} 条新闻")
    for n in news[:5]:
        print(f"- {n['title']}")
```

#### 5.2 上传到 Git

```bash
cd ~/.openclaw/workspace
git add skills/news-crawler
git commit -m "add news crawler skill"
git push origin main
```

#### 5.3 执行爬取

在对话中说：

```
运行 news crawler，爬取最近的科技新闻
```

#### 5.4 提炼内容

```
把爬到的新闻总结一下，提取最重要的 5 条
```

#### 5.5 生成文件

```
把总结保存为 markdown 文件
```

生成 `news-summary-2026-03-12.md`:

```markdown
# 科技新闻摘要 - 2026-03-12

## Top 5 新闻

1. **OpenAI 发布 GPT-5** - 性能提升 10 倍...
2. **Google 推出新 TPU** - 训练速度提升 5 倍...
3. **Meta 开源新模型** - 支持 100 种语言...
4. **苹果发布 M4 芯片** - AI 性能翻倍...
5. **特斯拉 FSD 更新** - 支持完全自动驾驶...
```

#### 5.6 发送到 QQ

```
把新闻摘要发到 QQ 群
```

---

### 完整流程示意

```
用户指令
   │
   ▼
┌─────────────────┐
│ 1. 创建爬虫技能  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Git 提交      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. 执行爬取      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. AI 总结       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. 生成文件      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 6. QQ 推送       │
└─────────────────┘
```

---

## 6. 展望 — 未来方向 🔮

### 当前局限

| 局限 | 说明 |
|------|------|
| 模型依赖 | 需要配置第三方 API |
| 学习曲线 | 需要理解基本概念 |
| 生态建设 | Skills 数量还在增长 |
| 文档完善 | 中文文档有待补充 |

### 未来方向

1. **更多 Skills** - 社区贡献，覆盖更多场景
2. **图形界面** - 降低使用门槛
3. **技能市场** - 一键安装热门技能
4. **多 Agent 协作** - 复杂任务分解
5. **本地模型** - 支持 Ollama 等本地部署
6. **企业版** - 团队协作、权限管理

### 我的看法

OpenClaw 代表了 AI Agent 的未来方向：

- **本地优先**: 数据隐私和安全
- **能力开放**: 不局限于聊天，能真正"做事"
- **社区驱动**: 开源生态，快速迭代
- **用户可控**: 用户决定 AI 能做什么

**预测**: 2026 年底，OpenClaw 或将成为个人 AI 助理的"标准配置"，如同今天的浏览器。

---

## 7. 资源 📚

### 官方资源

| 资源 | 链接 |
|------|------|
| GitHub | https://github.com/openclaw/openclaw |
| 文档 | https://docs.openclaw.ai |
| 技能市场 | https://clawhub.com |
| Discord | https://discord.com/invite/clawd |

### 社区资源

| 资源 | 说明 |
|------|------|
| 腾讯云公众号 | OpenClaw 技术解析 |
| 字节跳动技术团队 | AI Agent 实践 |
| InfoQ | OpenClaw 专题报道 |
| 国内外技术博客 | 部署教程和案例 |

### 学习路径

```
新手 → 部署安装 → 基础配置 → 使用内置 Tools
              ↓
进阶 → 安装 Skills → 配置 Channels → 定时任务
              ↓
高级 → 开发 Skills → 多 Agent 协作 → 企业部署
```

---

## 8. 常见问题 ❓

### Q: 安全吗？AI 会不会乱删文件？

**A**: OpenClaw 运行在本地，所有操作可审计。可配置安全策略：

```json
{
  "gateway": {
    "nodes": {
      "denyCommands": [
        "rm -rf",
        "sudo",
        "format"
      ]
    }
  }
}
```

危险操作需用户确认。

---

### Q: 需要付费吗？

**A**: 
- OpenClaw 本身：**免费** (开源)
- 大模型 API：**按量付费** (如通义千问/Claude/OpenAI)
- 推荐国内模型：通义千问、智谱、MiniMax (成本低，速度快)

---

### Q: 和 ChatGPT 有什么区别？

| 维度 | ChatGPT | OpenClaw |
|------|---------|----------|
| 运行位置 | 云端 | 本地 |
| 能力范围 | 聊天 | 聊天 + 操作系统 |
| 数据隐私 | 数据上云 | 数据本地 |
| 扩展性 | 有限 | 无限 (Skills) |
| 成本 | 订阅制 | 按量付费 |

**简单说**: ChatGPT 只能聊天，OpenClaw 能操作你的电脑。

---

### Q: 国内能用吗？

**A**: 可以。配置国内模型 API：

```json
{
  "models": {
    "providers": {
      "bailian": {
        "baseUrl": "https://dashscope.aliyuncs.com/v1",
        "apiKey": "sk-xxx"
      },
      "zhipu": {
        "baseUrl": "https://open.bigmodel.cn/api/paas/v4",
        "apiKey": "xxx"
      }
    }
  }
}
```

---

### Q: 支持哪些模型？

**A**: 支持所有 OpenAI 兼容 API：

- **国内**: 通义千问、智谱、MiniMax、Kimi、DeepSeek
- **国际**: OpenAI、Claude、Gemini、Groq

---

### Q: 如何备份配置？

**A**: 备份以下文件：

```bash
# 配置
cp ~/.openclaw/openclaw.json ~/backup/

# 工作区
cp -r ~/.openclaw/workspace ~/backup/

# 技能
cp -r ~/.openclaw/extensions ~/backup/
```

---

## 附录：快速参考卡

### 核心文件

| 文件 | 作用 | 编辑频率 |
|------|------|----------|
| `openclaw.json` | 系统配置 | 低 |
| `SOUL.md` | 人格定义 | 中 |
| `USER.md` | 用户信息 | 中 |
| `TOOLS.md` | 环境配置 | 高 |
| `MEMORY.md` | 长期记忆 | 自动 |

### 核心命令

```bash
# 检查状态
openclaw status

# 重启
openclaw gateway restart

# 搜索技能
skillhub search <keyword>

# 安装技能
skillhub install <skill>

# Git 提交
cd ~/.openclaw/workspace
git add . && git commit -m "msg" && git push
```

### 环境变量

| 变量 | 用途 |
|------|------|
| `N8N_API_KEY` | n8n API 密钥 |
| `GEMINI_API_KEY` | Gemini API 密钥 |
| `OPENAI_API_KEY` | OpenAI API 密钥 |
| `FIRECRAWL_API_KEY` | Firecrawl 网页提取 |

---

**文档版本**: 1.0  
**最后更新**: 2026-03-12  
**作者**: 基于社区资料整理优化

---

*本文档通过 OpenClaw 辅助编写，旨在帮助新手快速了解和使用 OpenClaw。*

# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## n8n

- **实例类型**: 待配置
- **API URL**: `N8N_BASE_URL` (待填写)
- **API Key**: `N8N_API_KEY` (存入 `~/.config/openclaw/settings.json`)

### 配置步骤

1. 创建配置文件:
```bash
mkdir -p ~/.config/openclaw
code ~/.config/openclaw/settings.json
```

2. 添加配置:
```json
{
  "skills": {
    "n8n": {
      "env": {
        "N8N_API_KEY": "你的 API Key",
        "N8N_BASE_URL": "https://你的 n8n 地址"
      }
    }
  }
}
```

3. 验证连接:
```bash
cd ~/.openclaw/workspace/skills/n8n
python3 scripts/n8n_api.py list-workflows --pretty
```

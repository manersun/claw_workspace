# Python 爬虫框架

简单的通用网页爬虫，支持数据抓取、解析和保存。

## 安装

```bash
pip install -r requirements.txt
```

## 使用

### 基础用法

```bash
python main.py
```

### 自定义爬虫

继承 `Spider` 类并重写 `parse` 方法：

```python
from spider import Spider

class MySpider(Spider):
    def parse(self, html: str):
        # 使用 BeautifulSoup 解析 HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        items = []
        for elem in soup.select('.target-class'):
            items.append({
                'title': elem.find('h1').text,
                'link': elem.find('a')['href']
            })
        return items

# 使用
spider = MySpider('https://example.com')
spider.run(['https://example.com/page1', 'https://example.com/page2'])
spider.save_json()
```

## 功能

- ✅ 自动请求管理（Session）
- ✅ User-Agent 伪装
- ✅ 请求间隔控制（避免被封）
- ✅ 错误处理和日志
- ✅ 支持 JSON/CSV 导出
- ✅ 易于扩展

## 注意事项

1. **遵守 robots.txt** - 爬取前检查目标网站的 robots.txt
2. **控制请求频率** - 设置合适的 delay，避免给服务器造成压力
3. **合法合规** - 仅爬取公开数据，遵守网站服务条款

## 许可证

MIT

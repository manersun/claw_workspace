#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用网页爬虫框架
支持：请求、解析、数据保存、错误处理
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Spider:
    """通用爬虫类"""
    
    def __init__(self, base_url: str, delay: float = 1.0):
        """
        初始化爬虫
        
        Args:
            base_url: 目标网站基础 URL
            delay: 请求间隔（秒），避免请求过快
        """
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.data: List[Dict] = []
        
    def fetch(self, url: str, params: Optional[Dict] = None) -> Optional[str]:
        """
        获取网页内容
        
        Args:
            url: 目标 URL
            params: 查询参数
            
        Returns:
            网页 HTML 文本，失败返回 None
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            time.sleep(self.delay)  # 礼貌爬取
            return response.text
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def parse(self, html: str) -> List[Dict]:
        """
        解析网页内容（子类重写此方法）
        
        Args:
            html: 网页 HTML
            
        Returns:
            解析后的数据列表
        """
        raise NotImplementedError("子类需要实现 parse 方法")
    
    def save_json(self, filename: str = None):
        """保存数据为 JSON"""
        if not filename:
            filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        logger.info(f"Data saved to {filename}")
    
    def save_csv(self, filename: str = None):
        """保存数据为 CSV"""
        if not filename:
            filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if not self.data:
            logger.warning("No data to save")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)
        logger.info(f"Data saved to {filename}")
    
    def run(self, urls: List[str]):
        """
        运行爬虫
        
        Args:
            urls: 要爬取的 URL 列表
        """
        for url in urls:
            html = self.fetch(url)
            if html:
                items = self.parse(html)
                self.data.extend(items)
                logger.info(f"Collected {len(items)} items from {url}")
        
        logger.info(f"Total collected: {len(self.data)} items")
        return self.data


class ExampleSpider(Spider):
    """示例爬虫 - 抓取新闻标题"""
    
    def parse(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        items = []
        
        # 示例：抓取所有链接和标题（根据实际网站修改选择器）
        for link in soup.find_all('a', href=True):
            title = link.get_text(strip=True)
            href = link['href']
            if title and len(title) > 5:  # 过滤短文本
                items.append({
                    'title': title,
                    'url': href if href.startswith('http') else self.base_url + href
                })
        
        return items


def main():
    """主函数"""
    # 示例：爬取 GitHub 趋势页面
    spider = ExampleSpider(base_url='https://github.com', delay=1.0)
    urls = ['https://github.com/trending']
    
    spider.run(urls)
    spider.save_json()
    spider.save_csv()
    
    print(f"\n✅ 爬取完成！共 {len(spider.data)} 条数据")


if __name__ == '__main__':
    main()

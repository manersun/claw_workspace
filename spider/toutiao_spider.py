#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日头条爬虫 - 获取美国和伊朗战争相关新闻
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ToutiaoSpider:
    """今日头条新闻爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.toutiao.com/',
        })
        self.news_list: List[Dict] = []
        
    def search_news(self, keyword: str, offset: int = 0, count: int = 20) -> List[Dict]:
        """
        搜索新闻
        
        Args:
            keyword: 搜索关键词
            offset: 偏移量
            count: 返回数量
            
        Returns:
            新闻列表
        """
        # 今日头条搜索 API（可能随时间变化）
        url = "https://www.toutiao.com/api/search/content/"
        params = {
            'keyword': keyword,
            'offset': offset,
            'count': count,
            'format': 'json',
            'cur_tab_title': 'news',
            'timestamp': int(time.time() * 1000)
        }
        
        try:
            logger.info(f"Searching: {keyword} (offset={offset})")
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get('data'):
                return data['data']
            else:
                logger.warning("No data returned from API")
                return []
                
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode failed: {e}")
            return []
    
    def parse_news(self, raw_data: List) -> List[Dict]:
        """
        解析新闻数据
        
        Args:
            raw_data: API 返回的原始数据
            
        Returns:
            解析后的新闻列表
        """
        parsed = []
        
        for item in raw_data:
            # 跳过广告和非新闻内容
            if item.get('type') != 'article':
                continue
            
            news = {
                'title': item.get('title', ''),
                'abstract': item.get('abstract', ''),
                'url': self._build_url(item),
                'source': item.get('source', '未知'),
                'publish_time': self._format_time(item.get('publish_time')),
                'behot_time': datetime.fromtimestamp(item.get('behot_time', 0)).strftime('%Y-%m-%d %H:%M:%S') if item.get('behot_time') else '',
                'comment_count': item.get('comment_count', 0),
                'digg_count': item.get('digg_count', 0),
            }
            
            # 只保留有标题的内容
            if news['title']:
                parsed.append(news)
        
        return parsed
    
    def _build_url(self, item: Dict) -> str:
        """构建新闻 URL"""
        article_url = item.get('article_url', '')
        if article_url:
            return article_url
        
        # 备用：使用 article_id 构建
        article_id = item.get('item_id', '') or item.get('group_id', '')
        if article_id:
            return f"https://www.toutiao.com/a{article_id}/"
        
        return ''
    
    def _format_time(self, publish_time) -> str:
        """格式化发布时间"""
        if not publish_time:
            return ''
        
        try:
            # 今日头条时间戳可能是秒或毫秒
            if publish_time > 10000000000:
                publish_time = publish_time / 1000
            return datetime.fromtimestamp(publish_time).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return str(publish_time)
    
    def crawl(self, keywords: List[str], max_pages: int = 3) -> List[Dict]:
        """
        爬取新闻
        
        Args:
            keywords: 搜索关键词列表
            max_pages: 每个关键词最多爬取的页数
            
        Returns:
            所有新闻列表
        """
        all_news = []
        
        for keyword in keywords:
            logger.info(f"{'='*50}")
            logger.info(f"Crawling keyword: {keyword}")
            logger.info(f"{'='*50}")
            
            for page in range(max_pages):
                offset = page * 20
                raw_data = self.search_news(keyword, offset=offset, count=20)
                
                if not raw_data:
                    logger.warning(f"No more results for '{keyword}' at page {page+1}")
                    break
                
                parsed = self.parse_news(raw_data)
                all_news.extend(parsed)
                logger.info(f"Page {page+1}: collected {len(parsed)} articles")
                
                # 礼貌爬取，避免请求过快
                time.sleep(2)
        
        self.news_list = all_news
        logger.info(f"\n✅ Total collected: {len(all_news)} articles")
        return all_news
    
    def save_json(self, filename: str = None):
        """保存为 JSON"""
        if not filename:
            filename = f"toutiao_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.news_list, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved to {filename}")
    
    def save_csv(self, filename: str = None):
        """保存为 CSV"""
        import csv
        
        if not filename:
            filename = f"toutiao_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if not self.news_list:
            logger.warning("No data to save")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['title', 'abstract', 'url', 'source', 'publish_time', 
                         'behot_time', 'comment_count', 'digg_count']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.news_list)
        logger.info(f"Saved to {filename}")
    
    def print_summary(self):
        """打印新闻摘要"""
        print("\n" + "="*80)
        print(f"共找到 {len(self.news_list)} 条相关新闻")
        print("="*80)
        
        for i, news in enumerate(self.news_list[:20], 1):  # 只显示前 20 条
            print(f"\n[{i}] {news['title']}")
            print(f"    来源：{news['source']} | 时间：{news['behot_time']}")
            print(f"    摘要：{news['abstract'][:100]}..." if len(news['abstract']) > 100 else f"    摘要：{news['abstract']}")
            print(f"    链接：{news['url']}")
            print(f"    评论：{news['comment_count']} | 点赞：{news['digg_count']}")
        
        if len(self.news_list) > 20:
            print(f"\n... 还有 {len(self.news_list) - 20} 条新闻，请查看保存的文件")


def main():
    """主函数"""
    spider = ToutiaoSpider()
    
    # 搜索关键词
    keywords = [
        '美国 伊朗 战争',
        '美国 伊朗 冲突',
        '美国 伊朗 军事',
        '伊朗 战争 最新消息',
    ]
    
    # 爬取新闻
    spider.crawl(keywords, max_pages=2)
    
    # 打印摘要
    spider.print_summary()
    
    # 保存数据
    spider.save_json()
    spider.save_csv()
    
    print("\n✅ 爬取完成！")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日头条新闻爬虫 - SKILL 执行脚本
支持：关键词搜索、数据保存、QQ/Telegram 推送
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

# 添加父目录到路径（支持从 SKILL 目录外调用）
sys.path.insert(0, str(Path(__file__).parent.parent))

from spider.toutiao_spider import ToutiaoSpider


def parse_args():
    parser = argparse.ArgumentParser(description='今日头条新闻爬虫')
    parser.add_argument('--keyword', type=str, required=True, help='搜索关键词')
    parser.add_argument('--save', action='store_true', help='保存数据到文件')
    parser.add_argument('--push-qq', type=str, help='推送 QQ（openid）')
    parser.add_argument('--push-telegram', type=str, help='推送 Telegram（chat_id）')
    parser.add_argument('--max-pages', type=int, default=2, help='最多爬取页数')
    parser.add_argument('--delay', type=float, default=2.0, help='请求间隔（秒）')
    return parser.parse_args()


def push_to_qq(openid: str, news_list: list):
    """推送新闻到 QQ"""
    if not news_list:
        print("⚠️ 没有新闻可推送")
        return
    
    # 构建消息
    top_news = news_list[:3]  # 只推送前 3 条
    message = f"🕷️ {args.keyword} 最新消息\n\n"
    
    for i, news in enumerate(top_news, 1):
        title = news.get('title', '无标题')
        source = news.get('source', '未知')
        time_str = news.get('behot_time', '')
        url = news.get('url', '')
        
        message += f"{i}. {title}\n"
        message += f"   📰 {source} | ⏰ {time_str}\n"
        message += f"   🔗 {url}\n\n"
    
    message += f"\n💡 数据来源：今日头条\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    # 调用 QQ Bot API（需要配置 token）
    # 这里简化处理，实际需要通过 OpenClaw message 工具发送
    print(f"📱 准备推送 QQ {openid}:")
    print(message[:200] + "..." if len(message) > 200 else message)
    
    # TODO: 集成 OpenClaw message 工具
    # exec(f'openclaw message send --channel qqbot --target {openid} -m "{message}"')


def push_to_telegram(chat_id: str, news_list: list):
    """推送新闻到 Telegram"""
    if not news_list:
        print("⚠️ 没有新闻可推送")
        return
    
    print(f"📱 准备推送 Telegram {chat_id}（功能待实现）")


def main():
    global args
    args = parse_args()
    
    print(f"🕷️ 开始爬取：{args.keyword}")
    print(f"📄 最多 {args.max_pages} 页 | ⏱️ 间隔 {args.delay}秒")
    
    # 创建爬虫
    spider = ToutiaoSpider()
    spider.delay = args.delay
    
    # 爬取新闻
    keywords = [args.keyword]
    news_list = spider.crawl(keywords, max_pages=args.max_pages)
    
    if not news_list:
        print("❌ 未找到相关新闻")
        return
    
    print(f"✅ 共爬取 {len(news_list)} 条新闻")
    
    # 保存数据
    if args.save:
        output_dir = Path(__file__).parent / 'data'
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存 JSON
        json_file = output_dir / f'news_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        print(f"💾 已保存：{json_file}")
        
        # 保存 CSV
        spider.save_csv(str(output_dir / f'news_{timestamp}.csv'))
    
    # 推送 QQ
    if args.push_qq:
        push_to_qq(args.push_qq, news_list)
    
    # 推送 Telegram
    if args.push_telegram:
        push_to_telegram(args.push_telegram, news_list)
    
    # 打印摘要
    print("\n📰 新闻摘要：")
    for i, news in enumerate(news_list[:5], 1):
        print(f"{i}. {news.get('title', '无标题')}")
    
    print("\n✅ 完成！")


if __name__ == '__main__':
    main()

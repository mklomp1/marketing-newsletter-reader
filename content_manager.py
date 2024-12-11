import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from urllib.request import urlopen
from xml.etree import ElementTree

class ContentManager:
    def __init__(self, article_manager, notes_manager):
        self.article_manager = article_manager
        self.notes_manager = notes_manager
        self.feeds = {
            "Search Engine Land": "https://searchengineland.com/feed",
            "Search Engine Journal": "https://www.searchenginejournal.com/feed",
            "Frankwatching": "https://www.frankwatching.com/feed/"
        }

    def parse_rss(self, url):
        """Parse RSS feed using built-in XML parser"""
        try:
            response = urlopen(url)
            tree = ElementTree.parse(response)
            root = tree.getroot()
            
            # Find the correct RSS namespace
            ns = {'': root.tag.split('}')[0].strip('{') if '}' in root.tag else ''}
            
            articles = []
            for item in root.findall('.//item', ns):
                article = {
                    'title': item.find('title', ns).text if item.find('title', ns) is not None else 'No title',
                    'link': item.find('link', ns).text if item.find('link', ns) is not None else '',
                    'description': item.find('description', ns).text if item.find('description', ns) is not None else '',
                    'date': item.find('pubDate', ns).text if item.find('pubDate', ns) is not None else ''
                }
                articles.append(article)
            return articles
        except Exception as e:
            print(f"Error parsing RSS feed: {e}")
            return []

    def fetch_news(self):
        all_articles = []
        for source, url in self.feeds.items():
            articles = self.parse_rss(url)
            for article in articles:
                article['source'] = source
            all_articles.extend(articles)
        return all_articles

    # ... rest of the class implementation ...
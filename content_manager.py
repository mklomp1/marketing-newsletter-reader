import feedparser
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from read_tracker import ReadTracker

class ContentManager:
    def __init__(self):
        self.feeds = {
            "Search Engine Land": "https://searchengineland.com/feed",
            "Search Engine Journal": "https://www.searchenginejournal.com/feed",
            "Frankwatching": "https://www.frankwatching.com/feed/"
        }
        
        self.newsletter_sources = {
            "PPC Mastery": {
                "url": "https://www.ppcmastery.com/blog",
                "type": "ppc"
            }
        }
        
        self.saved_content = []
        self.read_tracker = ReadTracker()
        self.load_saved_content()

    def refresh_all_content(self):
        self.fetch_news()
        self.fetch_newsletters()

    def fetch_news(self):
        for source, url in self.feeds.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    is_read = self.read_tracker.is_read(entry.link)
                    yield {
                        'title': entry.title,
                        'link': entry.link,
                        'source': source,
                        'date': entry.published,
                        'read': is_read
                    }
            except Exception as e:
                print(f"Error fetching {source}: {e}")

    def fetch_newsletters(self):
        for source, info in self.newsletter_sources.items():
            try:
                response = requests.get(info['url'])
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.find_all('article')
                for article in articles:
                    link = article.find('a')['href']
                    is_read = self.read_tracker.is_read(link)
                    yield {
                        'title': article.find('h2').text.strip(),
                        'link': link,
                        'source': source,
                        'date': article.find('time').text if article.find('time') else 'No date',
                        'read': is_read
                    }
            except Exception as e:
                print(f"Error fetching {source}: {e}")

    def mark_as_read(self, article_url):
        self.read_tracker.mark_as_read(article_url)

    def is_read(self, article_url):
        return self.read_tracker.is_read(article_url)

    def load_saved_content(self):
        try:
            with open('saved_content.json', 'r') as f:
                self.saved_content = json.load(f)
        except FileNotFoundError:
            self.saved_content = []

    def save_content(self, content):
        self.saved_content.append(content)
        with open('saved_content.json', 'w') as f:
            json.dump(self.saved_content, f)
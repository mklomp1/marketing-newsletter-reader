import json
from datetime import datetime

class ReadTracker:
    def __init__(self):
        self.read_file = 'read_status.json'
        self.read_articles = self.load_read_status()

    def load_read_status(self):
        try:
            with open(self.read_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_read_status(self):
        with open(self.read_file, 'w') as f:
            json.dump(self.read_articles, f)

    def mark_as_read(self, article_url):
        self.read_articles[article_url] = {
            'read_date': datetime.now().isoformat(),
            'last_updated': None
        }
        self.save_read_status()

    def is_read(self, article_url):
        return article_url in self.read_articles

    def get_read_date(self, article_url):
        if article_url in self.read_articles:
            return self.read_articles[article_url]['read_date']
        return None
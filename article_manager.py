import json
from datetime import datetime

class ArticleManager:
    def __init__(self):
        self.read_file = 'read_status.json'
        self.saved_file = 'saved_articles.json'
        self.read_articles = self.load_read_status()
        self.saved_articles = self.load_saved_articles()

    def load_read_status(self):
        try:
            with open(self.read_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def load_saved_articles(self):
        try:
            with open(self.saved_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def mark_as_read(self, article_url):
        self.read_articles[article_url] = {
            'read_date': datetime.now().isoformat(),
            'last_updated': None
        }
        self.save_read_status()

    def is_read(self, article_url):
        return article_url in self.read_articles

    def save_article(self, article_data):
        if not any(saved['url'] == article_data['url'] for saved in self.saved_articles):
            article_data['saved_date'] = datetime.now().isoformat()
            self.saved_articles.append(article_data)
            self.save_saved_articles()
            return True
        return False

    def remove_saved_article(self, article_url):
        self.saved_articles = [a for a in self.saved_articles if a['url'] != article_url]
        self.save_saved_articles()

    def save_read_status(self):
        with open(self.read_file, 'w') as f:
            json.dump(self.read_articles, f)

    def save_saved_articles(self):
        with open(self.saved_file, 'w') as f:
            json.dump(self.saved_articles, f)
import json
from datetime import datetime

class NotesManager:
    def __init__(self):
        self.notes_file = 'article_notes.json'
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.notes_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_notes(self):
        with open(self.notes_file, 'w') as f:
            json.dump(self.notes, f)

    def add_or_update_note(self, article_url, note_text):
        if note_text.strip():  # Only save if note isn't empty
            self.notes[article_url] = {
                'text': note_text,
                'last_updated': datetime.now().isoformat()
            }
        else:
            self.delete_note(article_url)  # Remove if note is empty
        self.save_notes()

    def delete_note(self, article_url):
        if article_url in self.notes:
            del self.notes[article_url]
            self.save_notes()

    def get_note(self, article_url):
        return self.notes.get(article_url, {}).get('text', '')

    def has_note(self, article_url):
        return article_url in self.notes

    def get_articles_with_notes(self):
        return list(self.notes.keys())

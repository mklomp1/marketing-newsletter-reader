import feedparser
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from tkinter import ttk, messagebox

class ContentManager:
    def __init__(self, article_manager, notes_manager):
        self.article_manager = article_manager
        self.notes_manager = notes_manager
        self.feeds = {
            "Search Engine Land": "https://searchengineland.com/feed",
            "Search Engine Journal": "https://www.searchenginejournal.com/feed",
            "Frankwatching": "https://www.frankwatching.com/feed/"
        }

    def create_content_tree(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("date", "source", "title", "notes")
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        tree.heading("date", text="Date")
        tree.heading("source", text="Source")
        tree.heading("title", text="Title")
        tree.heading("notes", text="Notes")

        tree.column("date", width=100)
        tree.column("source", width=150)
        tree.column("title", width=300)
        tree.column("notes", width=200)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return tree

    def refresh_notes_tab(self, tree):
        for item in tree.get_children():
            tree.delete(item)

        # Get all articles with notes
        noted_articles = []
        for feed_source, feed_url in self.feeds.items():
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    if self.notes_manager.has_note(entry.link):
                        note_text = self.notes_manager.get_note(entry.link)
                        noted_articles.append({
                            'date': entry.published,
                            'source': feed_source,
                            'title': entry.title,
                            'url': entry.link,
                            'note': note_text[:100] + '...' if len(note_text) > 100 else note_text
                        })
            except Exception as e:
                print(f"Error fetching {feed_source}: {e}")

        # Sort by date (newest first)
        noted_articles.sort(key=lambda x: x['date'], reverse=True)

        # Add to tree
        for article in noted_articles:
            tree.insert("", "end", values=(
                article['date'],
                article['source'],
                article['title'],
                article['note']
            ), tags=(article['url'],))
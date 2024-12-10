import tkinter as tk
from tkinter import ttk, scrolledtext, PanedWindow
import feedparser
import webbrowser
import json
import datetime
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup

class NewsletterReader:
    def __init__(self, root):
        self.root = root
        self.root.title("Marketing Newsletter Reader")
        self.root.geometry("1200x800")
        
        # Create main layout with PanedWindow
        self.main_paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_paned)
        
        # Create tabs
        self.news_tab = ttk.Frame(self.notebook)
        self.newsletter_tab = ttk.Frame(self.notebook)
        self.saved_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.news_tab, text="News")
        self.notebook.add(self.newsletter_tab, text="Newsletters")
        self.notebook.add(self.saved_tab, text="Saved Items")
        
        # Add notebook to the left pane
        self.main_paned.add(self.notebook, weight=1)
        
        # Initialize tabs
        self.setup_news_tab()
        self.setup_newsletter_tab()
        self.setup_saved_tab()
        
        # Setup article reader pane
        self.setup_reader_pane()
        self.main_paned.add(self.reader_frame, weight=2)
        
        # Load saved content
        self.saved_content_file = "saved_content.json"
        self.load_saved_content()
        
        # Sources
        self.feeds = {
            "Search Engine Land": "https://searchengineland.com/feed",
            "Search Engine Journal": "https://www.searchenginejournal.com/feed",
            "Frankwatching": "https://www.frankwatching.com/feed/",
        }
        
        self.newsletter_sources = {
            "PPC Mastery": {
                "url": "https://www.ppcmastery.com/blog",
                "type": "ppc"
            }
        }
        
        # Initial load
        self.refresh_all_content()

    def setup_news_tab(self):
        source_frame = ttk.LabelFrame(self.news_tab, text="News Sources")
        source_frame.pack(fill=tk.X, padx=5, pady=5)
        
        refresh_btn = ttk.Button(source_frame, text="Refresh News", 
                               command=lambda: self.refresh_content("news"))
        refresh_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.news_tree = self.create_content_tree(self.news_tab)

    def setup_newsletter_tab(self):
        control_frame = ttk.LabelFrame(self.newsletter_tab, text="Newsletter Controls")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        refresh_btn = ttk.Button(control_frame, text="Refresh Newsletters",
                               command=lambda: self.refresh_content("newsletter"))
        refresh_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.newsletter_source_var = tk.StringVar(value="All Sources")
        source_filter = ttk.Combobox(control_frame, textvariable=self.newsletter_source_var)
        source_filter['values'] = ['All Sources'] + list(self.newsletter_sources.keys())
        source_filter.pack(side=tk.LEFT, padx=5, pady=5)
        source_filter.bind('<<ComboboxSelected>>', 
                         lambda e: self.refresh_content("newsletter"))
        
        self.newsletter_tree = self.create_content_tree(self.newsletter_tab)

    def setup_saved_tab(self):
        control_frame = ttk.LabelFrame(self.saved_tab, text="Saved Items")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        refresh_btn = ttk.Button(control_frame, text="Refresh Saved",
                               command=self.show_saved_content)
        refresh_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        delete_btn = ttk.Button(control_frame, text="Delete Selected",
                              command=self.delete_saved_content)
        delete_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.saved_tree = self.create_content_tree(self.saved_tab)

def main():
    root = tk.Tk()
    app = NewsletterReader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
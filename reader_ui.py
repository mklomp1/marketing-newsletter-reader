import tkinter as tk
from tkinter import ttk
import webbrowser

class ReaderUI:
    def __init__(self, parent, content_manager, article_manager):
        self.parent = parent
        self.content_manager = content_manager
        self.article_manager = article_manager
        self.current_article = None
        self.setup_reader_pane()

    def setup_reader_pane(self):
        self.reader_frame = ttk.LabelFrame(self.parent, text="Article Reader")
        
        # Setup controls
        self.setup_search_controls()
        self.setup_article_controls()
        
        # Setup text area
        self.setup_text_area()

    def setup_search_controls(self):
        search_frame = ttk.Frame(self.reader_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Search entry
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Search navigation
        self.prev_btn = ttk.Button(search_frame, text="↑", width=3,
                                command=lambda: self.navigate_search('prev'))
        self.next_btn = ttk.Button(search_frame, text="↓", width=3,
                                command=lambda: self.navigate_search('next'))
        
        self.prev_btn.pack(side=tk.LEFT)
        self.next_btn.pack(side=tk.LEFT)
        
        self.match_label = ttk.Label(search_frame, text="")
        self.match_label.pack(side=tk.LEFT, padx=5)

    def setup_article_controls(self):
        control_frame = ttk.Frame(self.reader_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Article management buttons
        self.read_btn = ttk.Button(control_frame, text="Mark as Read",
                                command=self.mark_current_as_read)
        self.save_btn = ttk.Button(control_frame, text="Save Article",
                                command=self.save_current_article)
        self.open_btn = ttk.Button(control_frame, text="Open in Browser",
                                command=self.open_in_browser)
        
        self.read_btn.pack(side=tk.LEFT, padx=2)
        self.save_btn.pack(side=tk.LEFT, padx=2)
        self.open_btn.pack(side=tk.LEFT, padx=2)

    def setup_text_area(self):
        self.text = tk.Text(self.reader_frame, wrap=tk.WORD, padx=20, pady=20)
        scrollbar = ttk.Scrollbar(self.reader_frame, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)
        
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure text tags
        self.text.tag_configure('title', font=('Arial', 14, 'bold'))
        self.text.tag_configure('metadata', font=('Arial', 10, 'italic'))
        self.text.tag_configure('content', font=('Arial', 11))

    def display_article(self, article_data):
        self.current_article = article_data
        self.text.delete('1.0', tk.END)
        
        # Display article content
        self.text.insert(tk.END, article_data['title'] + '\n\n', 'title')
        self.text.insert(tk.END, f"{article_data['date']} | {article_data['source']}\n\n", 'metadata')
        self.text.insert(tk.END, article_data['content'], 'content')
        
        # Update button states
        self.update_button_states()

    def update_button_states(self):
        if self.current_article:
            state = 'normal'
            # Update read button text based on status
            if self.article_manager.is_read(self.current_article['url']):
                self.read_btn.configure(text="Mark as Unread")
            else:
                self.read_btn.configure(text="Mark as Read")
        else:
            state = 'disabled'
        
        self.read_btn.configure(state=state)
        self.save_btn.configure(state=state)
        self.open_btn.configure(state=state)

    def mark_current_as_read(self):
        if self.current_article:
            self.article_manager.mark_as_read(self.current_article['url'])
            self.update_button_states()

    def save_current_article(self):
        if self.current_article:
            if self.article_manager.save_article(self.current_article):
                tk.messagebox.showinfo("Success", "Article saved successfully!")
            else:
                tk.messagebox.showinfo("Info", "Article already saved")

    def open_in_browser(self):
        if self.current_article:
            webbrowser.open(self.current_article['url'])
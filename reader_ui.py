import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

class ReaderUI:
    def __init__(self, parent, content_manager, article_manager, notes_manager):
        self.parent = parent
        self.content_manager = content_manager
        self.article_manager = article_manager
        self.notes_manager = notes_manager
        self.current_article = None
        self.notes_visible = False
        self.setup_reader_pane()

    def setup_reader_pane(self):
        self.reader_frame = ttk.Frame(self.parent)
        
        # Top controls
        self.control_frame = ttk.Frame(self.reader_frame)
        self.control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Back button
        self.back_btn = ttk.Button(self.control_frame, text=\"← Back\",
                                command=self.go_back)
        self.back_btn.pack(side=tk.LEFT, padx=5)
        
        # Right-side controls
        right_controls = ttk.Frame(self.control_frame)
        right_controls.pack(side=tk.RIGHT, padx=5)
        
        self.save_btn = ttk.Button(right_controls, text=\"Save\",
                                command=self.save_current_article)
        self.open_btn = ttk.Button(right_controls, text=\"Open in Browser\",
                                command=self.open_in_browser)
        self.toggle_notes_btn = ttk.Button(right_controls, text=\"Show Notes\",
                                       command=self.toggle_notes)
        
        self.save_btn.pack(side=tk.LEFT, padx=2)
        self.open_btn.pack(side=tk.LEFT, padx=2)
        self.toggle_notes_btn.pack(side=tk.LEFT, padx=2)
        
        # Content area
        self.content_frame = ttk.PanedWindow(self.reader_frame, orient=tk.HORIZONTAL)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Article text area
        self.article_frame = ttk.Frame(self.content_frame)
        self.text = tk.Text(self.article_frame, wrap=tk.WORD, padx=20, pady=20)
        text_scroll = ttk.Scrollbar(self.article_frame, command=self.text.yview)
        self.text.configure(yscrollcommand=text_scroll.set)
        
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.content_frame.add(self.article_frame, weight=1)
        
        # Notes panel (initially hidden)
        self.setup_notes_panel()
        
        # Configure text tags
        self.text.tag_configure('title', font=('Arial', 14, 'bold'))
        self.text.tag_configure('metadata', font=('Arial', 10, 'italic'))
        self.text.tag_configure('content', font=('Arial', 11))

    def setup_notes_panel(self):
        self.notes_frame = ttk.Frame(self.content_frame)
        
        # Notes header
        notes_header = ttk.Frame(self.notes_frame)
        notes_header.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(notes_header, text=\"Notes\").pack(side=tk.LEFT)
        self.delete_note_btn = ttk.Button(notes_header, text=\"Delete\",
                                       command=self.delete_current_note)
        self.delete_note_btn.pack(side=tk.RIGHT)
        
        # Notes text area
        self.notes_text = tk.Text(self.notes_frame, wrap=tk.WORD, width=40)
        notes_scroll = ttk.Scrollbar(self.notes_frame, command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scroll.set)
        
        self.notes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        notes_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind note changes
        self.notes_text.bind('<<Modified>>', self.on_note_changed)

    def toggle_notes(self):
        if self.notes_visible:
            self.content_frame.forget(self.notes_frame)
            self.toggle_notes_btn.configure(text=\"Show Notes\")
            self.notes_visible = False
        else:
            self.content_frame.add(self.notes_frame, weight=0)
            self.toggle_notes_btn.configure(text=\"Hide Notes\")
            self.notes_visible = True

    def display_article(self, article_data):
        self.current_article = article_data
        self.text.delete('1.0', tk.END)
        
        # Display article
        self.text.insert(tk.END, article_data['title'] + '\\n\\n', 'title')
        self.text.insert(tk.END, f\"{article_data['date']} | {article_data['source']}\\n\\n\", 'metadata')
        self.text.insert(tk.END, article_data['content'], 'content')
        
        # Handle notes
        self.notes_text.delete('1.0', tk.END)
        if self.notes_manager.has_note(article_data['url']):
            self.notes_text.insert('1.0', self.notes_manager.get_note(article_data['url']))
            if not self.notes_visible:
                self.toggle_notes()  # Show notes if they exist
        else:
            if self.notes_visible:
                self.toggle_notes()  # Hide notes if none exist
        
        self.update_button_states()

    def go_back(self):
        # Clear current article and hide notes
        self.current_article = None
        if self.notes_visible:
            self.toggle_notes()
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', 'Select an article to read')
        self.update_button_states()
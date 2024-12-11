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
        
        # Set minimum window size
        self.parent.minsize(1000, 600)  # Minimum width for comfortable reading
        self.setup_reader_pane()

    def setup_reader_pane(self):
        self.reader_frame = ttk.Frame(self.parent)
        self.reader_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top controls
        self.setup_controls()
        
        # Content area with PanedWindow for resizable split
        self.content_frame = ttk.PanedWindow(self.reader_frame, orient=tk.HORIZONTAL)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Article text area (75% width)
        self.setup_article_area()
        
        # Notes panel (25% width, initially hidden)
        self.setup_notes_panel()

    def setup_controls(self):
        self.control_frame = ttk.Frame(self.reader_frame)
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Back button
        self.back_btn = ttk.Button(self.control_frame, text="← Back",
                                command=self.go_back)
        self.back_btn.pack(side=tk.LEFT)
        
        # Right-side controls
        right_controls = ttk.Frame(self.control_frame)
        right_controls.pack(side=tk.RIGHT)
        
        self.save_btn = ttk.Button(right_controls, text="Save",
                                command=self.save_current_article)
        self.open_btn = ttk.Button(right_controls, text="Open in Browser",
                                command=self.open_in_browser)
        self.toggle_notes_btn = ttk.Button(right_controls, text="Show Notes",
                                       command=self.toggle_notes)
        
        self.save_btn.pack(side=tk.LEFT, padx=2)
        self.open_btn.pack(side=tk.LEFT, padx=2)
        self.toggle_notes_btn.pack(side=tk.LEFT, padx=2)

    def setup_article_area(self):
        self.article_frame = ttk.Frame(self.content_frame)
        
        # Article content
        self.text = tk.Text(self.article_frame, wrap=tk.WORD, padx=20, pady=20)
        article_scroll = ttk.Scrollbar(self.article_frame, command=self.text.yview)
        self.text.configure(yscrollcommand=article_scroll.set)
        
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        article_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add to PanedWindow with 75% weight
        self.content_frame.add(self.article_frame, weight=75)
        
        # Configure text styles
        self.text.tag_configure('title', font=('Arial', 14, 'bold'))
        self.text.tag_configure('metadata', font=('Arial', 10, 'italic'))
        self.text.tag_configure('content', font=('Arial', 11))

    def setup_notes_panel(self):
        self.notes_frame = ttk.Frame(self.content_frame)
        
        # Notes header
        notes_header = ttk.Frame(self.notes_frame)
        notes_header.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(notes_header, text="Notes").pack(side=tk.LEFT)
        self.delete_note_btn = ttk.Button(notes_header, text="Delete",
                                       command=self.delete_current_note)
        self.delete_note_btn.pack(side=tk.RIGHT)
        
        # Notes text area
        self.notes_text = tk.Text(self.notes_frame, wrap=tk.WORD)
        notes_scroll = ttk.Scrollbar(self.notes_frame, command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scroll.set)
        
        self.notes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        notes_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def toggle_notes(self):
        if self.notes_visible:
            self.content_frame.forget(self.notes_frame)
            self.toggle_notes_btn.configure(text="Show Notes")
            self.notes_visible = False
        else:
            # Add notes panel with 25% weight
            self.content_frame.add(self.notes_frame, weight=25)
            self.toggle_notes_btn.configure(text="Hide Notes")
            self.notes_visible = True

    def display_article(self, article_data):
        self.current_article = article_data
        self.text.delete('1.0', tk.END)
        
        # Display article with proper padding and margins
        self.text.insert(tk.END, article_data['title'] + '\n\n', 'title')
        self.text.insert(tk.END, f"{article_data['date']} • {article_data['source']}\n\n", 'metadata')
        self.text.insert(tk.END, article_data['content'] + '\n\n', 'content')
        
        # Handle notes
        self.notes_text.delete('1.0', tk.END)
        if self.notes_manager.has_note(article_data['url']):
            self.notes_text.insert('1.0', self.notes_manager.get_note(article_data['url']))
            if not self.notes_visible:
                self.toggle_notes()
        
        # Scroll to top
        self.text.see('1.0')
        self.update_button_states()
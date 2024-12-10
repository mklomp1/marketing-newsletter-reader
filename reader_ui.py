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
        self.setup_reader_pane()

    def setup_reader_pane(self):
        self.reader_frame = ttk.LabelFrame(self.parent, text="Article Reader")
        
        # Content area (left side)
        self.content_frame = ttk.Frame(self.reader_frame)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Controls
        self.setup_article_controls()
        
        # Article text area
        self.setup_text_area()
        
        # Notes area (right side)
        self.setup_notes_area()

    def setup_article_controls(self):
        control_frame = ttk.Frame(self.content_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
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
        self.text = tk.Text(self.content_frame, wrap=tk.WORD, padx=20, pady=20)
        scrollbar = ttk.Scrollbar(self.content_frame, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)
        
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text.tag_configure('title', font=('Arial', 14, 'bold'))
        self.text.tag_configure('metadata', font=('Arial', 10, 'italic'))
        self.text.tag_configure('content', font=('Arial', 11))

    def setup_notes_area(self):
        self.notes_frame = ttk.LabelFrame(self.reader_frame, text="Notes")
        self.notes_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)

        # Note controls
        note_controls = ttk.Frame(self.notes_frame)
        note_controls.pack(fill=tk.X, padx=5, pady=5)

        self.delete_note_btn = ttk.Button(note_controls, text="Delete Note",
                                       command=self.delete_current_note)
        self.delete_note_btn.pack(side=tk.RIGHT)

        # Notes text area
        self.notes_text = tk.Text(self.notes_frame, wrap=tk.WORD, width=30, height=20)
        notes_scroll = ttk.Scrollbar(self.notes_frame, command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scroll.set)

        self.notes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        notes_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind note changes
        self.notes_text.bind('<<Modified>>', self.on_note_changed)

    def display_article(self, article_data):
        self.current_article = article_data
        self.text.delete('1.0', tk.END)
        
        # Display article
        self.text.insert(tk.END, article_data['title'] + '\n\n', 'title')
        self.text.insert(tk.END, f"{article_data['date']} | {article_data['source']}\n\n", 'metadata')
        self.text.insert(tk.END, article_data['content'], 'content')
        
        # Load notes
        self.notes_text.delete('1.0', tk.END)
        if self.notes_manager.has_note(article_data['url']):
            self.notes_text.insert('1.0', self.notes_manager.get_note(article_data['url']))
        
        self.update_button_states()

    def on_note_changed(self, event=None):
        if self.current_article and self.notes_text.edit_modified():
            self.notes_manager.add_or_update_note(
                self.current_article['url'],
                self.notes_text.get('1.0', 'end-1c')
            )
            self.notes_text.edit_modified(False)

    def delete_current_note(self):
        if self.current_article:
            if messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?"):
                self.notes_manager.delete_note(self.current_article['url'])
                self.notes_text.delete('1.0', tk.END)
                self.content_manager.refresh_notes_tab()
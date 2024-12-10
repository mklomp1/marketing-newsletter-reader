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
        # Set minimum window size
        self.parent.minsize(1200, 800)  # Minimum width for comfortable reading
        
        self.reader_frame = ttk.Frame(self.parent)
        self.reader_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top controls
        self.setup_controls()
        
        # Content area
        self.setup_content_area()
        
        # Configure text tags
        self.setup_text_styles()

    def setup_controls(self):
        self.control_frame = ttk.Frame(self.reader_frame)
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Back button with some padding
        self.back_btn = ttk.Button(self.control_frame, text="← Back",
                                command=self.go_back)
        self.back_btn.pack(side=tk.LEFT, padx=5)
        
        # Right-side controls
        right_controls = ttk.Frame(self.control_frame)
        right_controls.pack(side=tk.RIGHT, padx=5)
        
        # Controls with consistent spacing
        self.save_btn = ttk.Button(right_controls, text="Save",
                                command=self.save_current_article)
        self.open_btn = ttk.Button(right_controls, text="Open in Browser",
                                command=self.open_in_browser)
        self.toggle_notes_btn = ttk.Button(right_controls, text="Show Notes",
                                       command=self.toggle_notes)
        
        self.save_btn.pack(side=tk.LEFT, padx=5)
        self.open_btn.pack(side=tk.LEFT, padx=5)
        self.toggle_notes_btn.pack(side=tk.LEFT, padx=5)

    def setup_content_area(self):
        # Main content frame using PanedWindow for resizable split
        self.content_frame = ttk.PanedWindow(self.reader_frame, orient=tk.HORIZONTAL)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Article frame with proper weighting
        self.article_frame = ttk.Frame(self.content_frame)
        self.text = tk.Text(self.article_frame, wrap=tk.WORD, padx=30, pady=20)
        text_scroll = ttk.Scrollbar(self.article_frame, command=self.text.yview)
        self.text.configure(yscrollcommand=text_scroll.set)
        
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add article frame with 75% weight
        self.content_frame.add(self.article_frame, weight=75)
        
        # Setup notes panel but don't add it yet
        self.setup_notes_panel()

    def setup_notes_panel(self):
        self.notes_frame = ttk.Frame(self.content_frame)
        
        # Notes header with better spacing
        notes_header = ttk.Frame(self.notes_frame)
        notes_header.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(notes_header, text="Notes", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.delete_note_btn = ttk.Button(notes_header, text="Delete",
                                       command=self.delete_current_note)
        self.delete_note_btn.pack(side=tk.RIGHT)
        
        # Notes text area with fixed width ratio
        self.notes_text = tk.Text(self.notes_frame, wrap=tk.WORD)
        notes_scroll = ttk.Scrollbar(self.notes_frame, command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scroll.set)
        
        self.notes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        notes_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_text_styles(self):
        self.text.tag_configure('title', font=('Arial', 16, 'bold'))
        self.text.tag_configure('metadata', font=('Arial', 10, 'italic'))
        self.text.tag_configure('content', font=('Arial', 11))

    def toggle_notes(self):
        if self.notes_visible:
            self.content_frame.forget(self.notes_frame)
            self.toggle_notes_btn.configure(text="Show Notes")
            self.notes_visible = False
            # Adjust the article frame to take full width
            self.content_frame.update()
        else:
            # Add notes panel with 25% weight
            self.content_frame.add(self.notes_frame, weight=25)
            self.toggle_notes_btn.configure(text="Hide Notes")
            self.notes_visible = True
            # Ensure proper ratio
            self.content_frame.update()

    def display_article(self, article_data):
        self.current_article = article_data
        self.text.delete('1.0', tk.END)
        
        # Display article with proper spacing
        self.text.insert(tk.END, article_data['title'] + '\n\n', 'title')
        self.text.insert(tk.END, f"{article_data['date']} • {article_data['source']}\n\n", 'metadata')
        self.text.insert(tk.END, article_data['content'], 'content')
        
        # Handle notes
        self.notes_text.delete('1.0', tk.END)
        if self.notes_manager.has_note(article_data['url']):
            self.notes_text.insert('1.0', self.notes_manager.get_note(article_data['url']))
        
        # Update UI state
        self.update_button_states()

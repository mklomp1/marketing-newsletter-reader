import tkinter as tk
from tkinter import ttk

class ReaderUI:
    def __init__(self, parent, content_manager):
        self.parent = parent
        self.content_manager = content_manager
        self.setup_reader_pane()

    def setup_reader_pane(self):
        self.reader_frame = ttk.LabelFrame(self.parent, text="Article Reader")
        
        # Search functionality
        self.setup_search_frame()
        
        # Toolbar
        self.setup_toolbar()
        
        # Article text area
        self.setup_text_area()
        
        return self.reader_frame

    def setup_search_frame(self):
        search_frame = ttk.Frame(self.reader_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.prev_btn = ttk.Button(search_frame, text="↑", width=3)
        self.prev_btn.pack(side=tk.LEFT)
        
        self.next_btn = ttk.Button(search_frame, text="↓", width=3)
        self.next_btn.pack(side=tk.LEFT)
        
        self.match_label = ttk.Label(search_frame, text="")
        self.match_label.pack(side=tk.LEFT, padx=5)

    def setup_toolbar(self):
        toolbar = ttk.Frame(self.reader_frame)
        toolbar.pack(fill=tk.X, padx=5)
        
        # Regular buttons
        self.browser_btn = ttk.Button(toolbar, text="Open in Browser")
        self.browser_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(toolbar, text="Save for Later")
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Mark as read button
        self.read_btn = ttk.Button(toolbar, text="Mark as Read")
        self.read_btn.pack(side=tk.LEFT, padx=5)
        
        # Zoom controls
        self.zoom_in_btn = ttk.Button(toolbar, text="Zoom In")
        self.zoom_in_btn.pack(side=tk.RIGHT, padx=5)
        
        self.zoom_out_btn = ttk.Button(toolbar, text="Zoom Out")
        self.zoom_out_btn.pack(side=tk.RIGHT, padx=5)

    def setup_text_area(self):
        self.text = tk.Text(
            self.reader_frame,
            wrap=tk.WORD,
            padx=20,
            pady=20,
            spacing1=2,
            spacing2=2
        )
        
        scrollbar = ttk.Scrollbar(self.reader_frame, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)
        
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure tags
        self.text.tag_configure('title', font=('Arial', 14, 'bold'))
        self.text.tag_configure('metadata', font=('Arial', 10, 'italic'))
        self.text.tag_configure('content', font=('Arial', 11))
        self.text.tag_configure('read', foreground='gray')

    def create_content_tree(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tree with read status column
        columns = ("status", "date", "source", "title")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        tree.heading("status", text="")
        tree.heading("date", text="Date")
        tree.heading("source", text="Source")
        tree.heading("title", text="Title")
        
        tree.column("status", width=30)
        tree.column("date", width=100)
        tree.column("source", width=150)
        tree.column("title", width=400)
        
        # Configure tag for read items
        tree.tag_configure('read', foreground='gray')
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        return tree

    def update_read_status(self, tree_item):
        """Update the visual appearance of a read item"""
        tree = tree_item.widget
        item_id = tree_item.selection()[0]
        url = tree.item(item_id)['tags'][1]
        
        if self.content_manager.is_read(url):
            tree.item(item_id, tags=('read',))
            tree.set(item_id, 'status', '✓')
        else:
            tree.item(item_id, tags=())
            tree.set(item_id, 'status', '')
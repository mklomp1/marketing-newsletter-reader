import tkinter as tk
from tkinter import ttk

def setup_reader_pane(parent):
    reader_frame = ttk.LabelFrame(parent, text="Article Reader")
    
    # Search functionality
    search_frame = create_search_frame(reader_frame)
    search_frame.pack(fill=tk.X, padx=5, pady=5)
    
    # Toolbar
    toolbar = create_toolbar(reader_frame)
    toolbar.pack(fill=tk.X, padx=5)
    
    # Article text area
    text_area = create_text_area(reader_frame)
    text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    return reader_frame

def create_search_frame(parent):
    frame = ttk.Frame(parent)
    
    ttk.Label(frame, text="Search:").pack(side=tk.LEFT, padx=5)
    ttk.Entry(frame).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    ttk.Button(frame, text="↑", width=3).pack(side=tk.LEFT)
    ttk.Button(frame, text="↓", width=3).pack(side=tk.LEFT)
    
    return frame

def create_toolbar(parent):
    frame = ttk.Frame(parent)
    
    ttk.Button(frame, text="Open in Browser").pack(side=tk.LEFT, padx=5)
    ttk.Button(frame, text="Save for Later").pack(side=tk.LEFT, padx=5)
    ttk.Button(frame, text="Zoom In").pack(side=tk.RIGHT, padx=5)
    ttk.Button(frame, text="Zoom Out").pack(side=tk.RIGHT, padx=5)
    
    return frame

def create_text_area(parent):
    text = tk.Text(parent, wrap=tk.WORD, padx=20, pady=20)
    scrollbar = ttk.Scrollbar(parent, command=text.yview)
    text.configure(yscrollcommand=scrollbar.set)
    
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    return text
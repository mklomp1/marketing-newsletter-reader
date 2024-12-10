import tkinter as tk
from tkinter import ttk
from reader_ui import setup_reader_pane
from content_manager import ContentManager

class NewsletterReader:
    def __init__(self, root):
        self.root = root
        self.root.title("Marketing Newsletter Reader")
        self.root.geometry("1200x800")
        self.content_manager = ContentManager()
        self.setup_ui()

    def setup_ui(self):
        # Create main layout
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Setup tabs and reader
        self.setup_tabs()
        self.setup_reader()
        
        # Initial content load
        self.content_manager.refresh_all_content()

    def setup_tabs(self):
        self.notebook = ttk.Notebook(self.main_paned)
        self.main_paned.add(self.notebook, weight=1)
        
        # Create and add tabs
        self.tabs = {
            "news": ttk.Frame(self.notebook),
            "newsletters": ttk.Frame(self.notebook),
            "saved": ttk.Frame(self.notebook)
        }
        
        for name, frame in self.tabs.items():
            self.notebook.add(frame, text=name.capitalize())

    def setup_reader(self):
        self.reader_frame = setup_reader_pane(self.main_paned)
        self.main_paned.add(self.reader_frame, weight=2)

def main():
    root = tk.Tk()
    app = NewsletterReader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
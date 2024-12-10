import tkinter as tk
from tkinter import ttk
from article_manager import ArticleManager
from content_manager import ContentManager
from notes_manager import NotesManager
from reader_ui import ReaderUI

class NewsletterReader:
    def __init__(self, root):
        self.root = root
        self.root.title("Marketing Newsletter Reader")
        self.root.geometry("1200x800")
        
        # Initialize managers
        self.notes_manager = NotesManager()
        self.article_manager = ArticleManager()
        self.content_manager = ContentManager(self.article_manager, self.notes_manager)
        
        # Setup UI
        self.setup_main_interface()

    def setup_main_interface(self):
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_paned)
        
        # Create tabs
        self.tabs = {
            'news': self.create_tab('News'),
            'newsletters': self.create_tab('Newsletters'),
            'notes': self.create_tab('Notes'),
            'saved': self.create_tab('Saved Articles')
        }
        
        self.main_paned.add(self.notebook, weight=1)
        
        # Create reader UI
        self.reader_ui = ReaderUI(
            self.main_paned,
            self.content_manager,
            self.article_manager,
            self.notes_manager
        )
        self.main_paned.add(self.reader_ui.reader_frame, weight=2)
        
        # Initial content load
        self.refresh_all_content()

    def create_tab(self, title):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        
        refresh_frame = ttk.Frame(frame)
        refresh_frame.pack(fill=tk.X, padx=5, pady=5)
        
        refresh_btn = ttk.Button(
            refresh_frame,
            text=f"Refresh {title}",
            command=lambda: self.refresh_content(title.lower())
        )
        refresh_btn.pack(side=tk.RIGHT)
        
        tree = self.content_manager.create_content_tree(frame)
        return {'frame': frame, 'tree': tree}

    def refresh_all_content(self):
        for tab_name in self.tabs:
            self.refresh_content(tab_name)

    def refresh_content(self, tab_name):
        if tab_name == 'notes':
            self.content_manager.refresh_notes_tab(self.tabs[tab_name]['tree'])
        else:
            self.content_manager.refresh_content(tab_name, self.tabs[tab_name]['tree'])

def main():
    root = tk.Tk()
    app = NewsletterReader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable, Optional
import os
import json


class FileLoaderWidget(ttk.Frame):
    def __init__(self, parent, on_load_callback: Callable[[dict], None], theme_manager=None):
        super().__init__(parent)
        self.on_load_callback = on_load_callback
        self.theme_manager = theme_manager
        self.drag_active = False
        self.file_loaded = False
        
        self._create_widgets()
        self._setup_drag_drop()

    def _create_widgets(self):
        self.container = ttk.Frame(self, padding=20)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.drop_zone = tk.Canvas(
            self.container, 
            width=400, 
            height=200, 
            highlightthickness=2,
            highlightbackground='#4a9eff' if self.theme_manager else 'gray',
            bg='#1e1e1e' if self.theme_manager and self.theme_manager.is_dark else '#f5f5f5'
        )
        self.drop_zone.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.drop_text = self.drop_zone.create_text(
            200, 80,
            text="📁 Drop JSON file here\nor click to browse",
            font=('Segoe UI', 12),
            fill='#ffffff' if self.theme_manager and self.theme_manager.is_dark else '#333333',
            justify=tk.CENTER
        )

        self.drop_zone.bind('<Button-1>', self._browse_file)
        self.drop_zone.bind('<Enter>', self._on_enter)
        self.drop_zone.bind('<Leave>', self._on_leave)

        self.info_label = ttk.Label(
            self.container,
            text="Supported: Telegram JSON export files",
            font=('Segoe UI', 9)
        )
        self.info_label.pack(pady=(5, 10))

        self.browse_btn = ttk.Button(
            self.container,
            text="Browse Files",
            command=self._browse_file
        )
        self.browse_btn.pack(pady=5)

        self.status_var = tk.StringVar(value="No file loaded")
        self.status_label = ttk.Label(
            self.container,
            textvariable=self.status_var,
            font=('Segoe UI', 9)
        )
        self.status_label.pack(pady=5)

    def _setup_drag_drop(self):
        try:
            self.drop_zone.drop_target_register = lambda *args: None
            self.drop_zone.dnd_bind = lambda *args, **kwargs: None
        except:
            pass

    def _on_enter(self, event):
        self.drop_zone.config(highlightbackground='#00ff00')
        self.drop_zone.itemconfig(self.drop_text, text="📁 Drop file here")

    def _on_leave(self, event):
        color = '#4a9eff' if self.theme_manager and self.theme_manager.is_dark else 'gray'
        self.drop_zone.config(highlightbackground=color)
        self.drop_zone.itemconfig(self.drop_text, text="📁 Drop JSON file here\nor click to browse")

    def _browse_file(self, event=None):
        filepath = filedialog.askopenfilename(
            title="Select Chat JSON File",
            filetypes=[
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if filepath:
            self._load_file(filepath)

    def _load_file(self, filepath: str):
        try:
            self.status_var.set(f"Loading: {os.path.basename(filepath)}...")
            self.update()

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if 'messages' not in data:
                messagebox.showerror("Error", "Invalid chat file format. Missing 'messages' key.")
                self.status_var.set("Error: Invalid format")
                return

            self.file_loaded = True
            self.status_var.set(f"✓ Loaded: {os.path.basename(filepath)}")
            self._update_drop_zone_success()
            
            if self.on_load_callback:
                self.on_load_callback(data)

        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON file. Please check the file format.")
            self.status_var.set("Error: Invalid JSON")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
            self.status_var.set("Error: Load failed")

    def _update_drop_zone_success(self):
        self.drop_zone.config(highlightbackground='#00ff00')
        self.drop_zone.itemconfig(
            self.drop_text,
            text="✓ File loaded successfully!\nClick to load another file"
        )

    def update_theme(self):
        if not self.theme_manager:
            return
        
        bg_color = '#1e1e1e' if self.theme_manager.is_dark else '#f5f5f5'
        text_color = '#ffffff' if self.theme_manager.is_dark else '#333333'
        
        self.drop_zone.config(bg=bg_color)
        self.drop_zone.itemconfig(self.drop_text, fill=text_color)

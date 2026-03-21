import tkinter as tk
from tkinter import ttk
from typing import Dict, Any


class ThemeManager:
    DARK_THEME = {
        'bg': '#1e1e1e',
        'fg': '#ffffff',
        'accent': '#4a9eff',
        'accent_hover': '#3a8eef',
        'card_bg': '#2d2d2d',
        'card_border': '#3d3d3d',
        'success': '#4caf50',
        'warning': '#ff9800',
        'error': '#f44336',
        'chart_colors': ['#4a9eff', '#ff6b6b', '#51cf66', '#ffd43b', '#845ef7', '#f06595'],
    }

    LIGHT_THEME = {
        'bg': '#f5f5f5',
        'fg': '#333333',
        'accent': '#2196F3',
        'accent_hover': '#1976D2',
        'card_bg': '#ffffff',
        'card_border': '#e0e0e0',
        'success': '#4caf50',
        'warning': '#ff9800',
        'error': '#f44336',
        'chart_colors': ['#2196F3', '#f44336', '#4caf50', '#ff9800', '#9c27b0', '#e91e63'],
    }

    def __init__(self, root: tk.Tk, initial_dark: bool = True):
        self.root = root
        self.is_dark = initial_dark
        self._callbacks = []
        self._setup_styles()

    def _setup_styles(self):
        self.style = ttk.Style()
        self._apply_theme()

    def _apply_theme(self):
        theme = self.DARK_THEME if self.is_dark else self.LIGHT_THEME

        self.root.configure(bg=theme['bg'])

        self.style.theme_use('clam')

        self.style.configure('TFrame', background=theme['bg'])
        self.style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TButton', background=theme['accent'], foreground='white')
        self.style.map('TButton', background=[('active', theme['accent_hover'])])
        self.style.configure('TNotebook', background=theme['bg'])
        self.style.configure('TNotebook.Tab', background=theme['card_bg'], foreground=theme['fg'], padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', theme['accent'])], foreground=[('selected', 'white')])
        self.style.configure('Treeview', background=theme['card_bg'], foreground=theme['fg'], fieldbackground=theme['card_bg'])
        self.style.configure('Treeview.Heading', background=theme['card_bg'], foreground=theme['fg'])
        self.style.map('Treeview', background=[('selected', theme['accent'])], foreground=[('selected', 'white')])
        self.style.configure('TProgressbar', background=theme['accent'], troughcolor=theme['card_bg'])
        self.style.configure('Horizontal.TScrollbar', background=theme['card_bg'], troughcolor=theme['bg'])
        self.style.configure('Vertical.TScrollbar', background=theme['card_bg'], troughcolor=theme['bg'])
        self.style.configure('TLabelframe', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TLabelframe.Label', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TCombobox', background=theme['card_bg'], foreground=theme['fg'], fieldbackground=theme['card_bg'])
        self.style.configure('TCheckbutton', background=theme['bg'], foreground=theme['fg'])
        self.style.configure('TRadiobutton', background=theme['bg'], foreground=theme['fg'])

        for callback in self._callbacks:
            callback()

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self._apply_theme()

    def set_dark_mode(self, dark: bool):
        self.is_dark = dark
        self._apply_theme()

    def get_colors(self) -> Dict[str, str]:
        return self.DARK_THEME if self.is_dark else self.LIGHT_THEME

    def get_chart_colors(self) -> list:
        return self.get_colors()['chart_colors']

    def register_callback(self, callback):
        self._callbacks.append(callback)

    def unregister_callback(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

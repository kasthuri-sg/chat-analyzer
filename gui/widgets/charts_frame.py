import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import warnings
from typing import Optional, Dict, Any, List, Tuple

warnings.filterwarnings('ignore', category=UserWarning)


class ScrollableChartsFrame(ttk.Frame):
    def __init__(self, parent, theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.figures = []
        self.canvases = []
        
        self._create_scrollable_container()
        self._apply_theme()

    def _create_scrollable_container(self):
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all"),
                height=self.canvas.bbox("all")[3] if self.canvas.bbox("all") else 0
            )
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
        
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def _apply_theme(self):
        if self.theme_manager:
            plt_style = 'dark_background' if self.theme_manager.is_dark else 'seaborn-v0_8-whitegrid'
            try:
                plt.style.use(plt_style)
            except:
                pass

    def clear(self):
        for canvas in self.canvases:
            canvas.get_tk_widget().destroy()
        for fig in self.figures:
            plt.close(fig)
        self.figures = []
        self.canvases = []

    def create_figure(self, figsize=(8, 5)) -> Figure:
        fig = Figure(figsize=figsize, dpi=100)
        self.figures.append(fig)
        return fig

    def embed_figure(self, fig: Figure, row: int = 0, column: int = 0, colspan: int = 1, rowspan: int = 1):
        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=column, columnspan=colspan, rowspan=rowspan, padx=10, pady=10, sticky='nsew')
        self.canvases.append(canvas)
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        return canvas

    def _get_emoji_label(self, emoji_char: str) -> str:
        emoji_names = {
            "😂": "Tears of Joy",
            "❤️": "Red Heart",
            "🔥": "Fire",
            "😍": "Heart Eyes",
            "😭": "Crying",
            "😊": "Smile",
            "🙏": "Pray",
            "👍": "Thumbs Up",
            "💀": "Skull",
            "✨": "Sparkles",
            "🎉": "Party",
            "😎": "Cool",
            "💖": "Sparkle Heart",
            "🥺": "Pleading",
            "🤣": "ROFL",
            "😘": "Kiss",
            "🥰": "Smiling Hearts",
            "😢": "Sad",
            "💔": "Broken Heart",
            "🤔": "Thinking",
            "😅": "Sweat Smile",
            "😔": "Pensive",
            "👀": "Eyes",
            "💯": "100",
            "🙌": "Raising Hands",
            "💕": "Two Hearts",
            "😌": "Relieved",
            "🙃": "Upside Down",
            "😜": "Wink Tongue",
            "😏": "Smirk",
            "☺️": "Smiling",
            "🙂": "Slight Smile",
            "🤗": "Hugging",
            "🤩": "Star Struck",
            "🤫": "Shushing",
            "🤭": "Hand Mouth",
            "🤐": "Zipper Mouth",
            "🤨": "Eyebrow",
            "😐": "Neutral",
            "😑": "Expressionless",
            "😶": "No Mouth",
            "🙄": "Eye Roll",
            "😣": "Persevering",
            "😥": "Disappointed",
            "😮": "Open Mouth",
            "😯": "Hushed",
            "😪": "Sleepy",
            "😫": "Tired",
            "😴": "Sleeping",
            "😛": "Tongue",
            "😝": "Squint Tongue",
            "🤤": "Drooling",
            "😒": "Unamused",
            "😓": "Downcast",
            "😕": "Confused",
            "🫠": "Melting",
            "🫡": "Saluting",
            "🫢": "Peeking Hand",
            "🫣": "Peeking Eye",
            "🫤": "Diagonal Mouth",
            "🫥": "Dotted Line",
            "🫦": "Biting Lip",
            "🍕": "Pizza",
            "☕": "Coffee",
            "🏀": "Basketball",
            "🎬": "Clapper",
            "🌙": "Moon",
            "💤": "Sleep",
            "🎯": "Bullseye",
            "🎊": "Confetti",
            "🥳": "Partying",
            "🎂": "Cake",
            "🎁": "Gift",
            "🌟": "Star",
            "⭐": "Star",
            "💪": "Flex",
            "👏": "Clapping",
            "🙏": "Prayer",
            "😌": "Relieved",
            "😚": "Kissing Closed",
            "😙": "Kissing Eyes",
            "😽": "Kissing Cat",
            "😼": "Cat Smile",
            "😾": "Pouting Cat",
            "🙀": "Weary Cat",
            "😹": "Cat Joy",
            "😿": "Crying Cat",
            "🙈": "See No Evil",
            "🙉": "Hear No Evil",
            "🙊": "Speak No Evil",
            "💋": "Kiss Mark",
            "💌": "Love Letter",
            "💘": "Heart Arrow",
            "💝": "Heart Ribbon",
            "💗": "Growing Heart",
            "💓": "Beating Heart",
            "💞": "Revolving Hearts",
            "💟": "Heart Decoration",
            "❣️": "Heart Exclamation",
            "🙂": "Slightly Smiling",
            "🙃": "Upside-Down",
            "😉": "Winking",
            "😌": "Relieved",
            "😍": "Heart-Eyes",
            "🥰": "Smiling Face with Hearts",
            "😘": "Face Blowing a Kiss",
            "😗": "Kissing",
            "😙": "Kissing with Eyes Closed",
            "😚": "Kissing with Smiling Eyes",
            "😋": "Savoring Food",
            "😜": "Winking with Tongue",
            "🤪": "Zany",
            "😝": "Squinting with Tongue",
            "🤑": "Money-Mouth",
            "🤗": "Hugging",
            "🤭": "Hand Over Mouth",
            "🤫": "Shushing",
            "🤔": "Thinking",
            "🤐": "Zipper-Mouth",
            "🤨": "Face with Raised Eyebrow",
            "😐": "Neutral",
            "😑": "Expressionless",
            "😶": "Face Without Mouth",
            "😏": "Smirking",
            "😒": "Unamused",
            "🙄": "Face with Rolling Eyes",
            "😬": "Grimacing",
            "🤥": "Lying",
            "😌": "Relieved",
            "😔": "Pensive",
            "😪": "Sleepy",
            "🤤": "Drooling",
            "😴": "Sleeping",
            "😷": "Face with Medical Mask",
            "🤒": "Face with Thermometer",
            "🤕": "Face with Head-Bandage",
        }
        return emoji_names.get(emoji_char, f"Emoji")

    def create_bar_chart(self, data: Dict[str, Any], title: str, xlabel: str = '', ylabel: str = 'Count', 
                         color: str = None, figsize=(8, 5), horizontal: bool = False) -> Figure:
        fig = self.create_figure(figsize)
        ax = fig.add_subplot(111)
        
        labels = list(data.keys())
        values = list(data.values())
        
        has_emoji = any(ord(c) > 127 for label in labels for c in str(label))
        if has_emoji:
            labels = [self._get_emoji_label(str(l)) if any(ord(c) > 127 for c in str(l)) else str(l) for l in labels]
        
        if color is None:
            color = '#4a9eff' if self.theme_manager and self.theme_manager.is_dark else '#2196F3'
        
        if horizontal:
            bars = ax.barh(labels, values, color=color)
            ax.set_xlabel(ylabel)
            ax.set_ylabel(xlabel)
        else:
            x_pos = np.arange(len(labels))
            bars = ax.bar(x_pos, values, color=color)
            ax.set_xticks(x_pos)
            ax.set_xticklabels(labels, rotation=45, ha='right')
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
        
        ax.set_title(title)
        
        if self.theme_manager:
            text_color = 'white' if self.theme_manager.is_dark else 'black'
            ax.tick_params(colors=text_color)
            ax.xaxis.label.set_color(text_color)
            ax.yaxis.label.set_color(text_color)
            ax.title.set_color(text_color)
            for spine in ax.spines.values():
                spine.set_color(text_color)
        
        fig.tight_layout()
        return fig

    def create_line_chart(self, x_data: List, y_data: List, title: str, xlabel: str = '', ylabel: str = '',
                          color: str = None, figsize=(10, 4)) -> Figure:
        fig = self.create_figure(figsize)
        ax = fig.add_subplot(111)
        
        if color is None:
            color = '#4a9eff' if self.theme_manager and self.theme_manager.is_dark else '#2196F3'
        
        ax.plot(x_data, y_data, color=color, linewidth=2, marker='o', markersize=3)
        ax.fill_between(range(len(y_data)), y_data, alpha=0.3, color=color)
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        if self.theme_manager:
            text_color = 'white' if self.theme_manager.is_dark else 'black'
            ax.tick_params(colors=text_color)
            ax.xaxis.label.set_color(text_color)
            ax.yaxis.label.set_color(text_color)
            ax.title.set_color(text_color)
            for spine in ax.spines.values():
                spine.set_color(text_color)
        
        fig.tight_layout()
        return fig

    def create_pie_chart(self, data: Dict[str, Any], title: str, figsize=(6, 6)) -> Figure:
        fig = self.create_figure(figsize)
        ax = fig.add_subplot(111)
        
        raw_labels = list(data.keys())
        values = list(data.values())
        
        has_emoji = any(ord(c) > 127 for label in raw_labels for c in str(label))
        if has_emoji:
            labels = [self._get_emoji_label(str(l)) if any(ord(c) > 127 for c in str(l)) else str(l) for l in raw_labels]
        else:
            labels = raw_labels
        
        colors = plt.cm.tab20(np.linspace(0, 1, len(labels)))
        
        wedges, texts, autotexts = ax.pie(
            values, labels=labels, autopct='%1.1f%%',
            colors=colors, startangle=90
        )
        
        ax.set_title(title)
        
        if self.theme_manager:
            text_color = 'white' if self.theme_manager.is_dark else 'black'
            for text in texts:
                text.set_color(text_color)
            for autotext in autotexts:
                autotext.set_color('white' if self.theme_manager.is_dark else 'black')
            ax.title.set_color(text_color)
        
        fig.tight_layout()
        return fig

    def create_heatmap(self, data: List[List[int]], title: str, xlabels: List[str] = None, 
                       ylabels: List[str] = None, figsize=(12, 6)) -> Figure:
        fig = self.create_figure(figsize)
        ax = fig.add_subplot(111)
        
        data_array = np.array(data)
        
        cmap = 'YlOrRd'
        
        im = ax.imshow(data_array, cmap=cmap, aspect='auto')
        
        if xlabels:
            ax.set_xticks(np.arange(len(xlabels)))
            ax.set_xticklabels(xlabels, rotation=45, ha='right')
        if ylabels:
            ax.set_yticks(np.arange(len(ylabels)))
            ax.set_yticklabels(ylabels)
        
        ax.set_title(title)
        
        cbar = fig.colorbar(im, ax=ax)
        
        if self.theme_manager:
            text_color = 'white' if self.theme_manager.is_dark else 'black'
            ax.tick_params(colors=text_color)
            ax.title.set_color(text_color)
            cbar.ax.yaxis.set_tick_params(color=text_color)
            plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=text_color)
        
        fig.tight_layout()
        return fig

    def create_stacked_bar(self, data: Dict[str, Dict[str, int]], title: str, 
                           xlabel: str = '', ylabel: str = 'Count', figsize=(10, 5)) -> Figure:
        fig = self.create_figure(figsize)
        ax = fig.add_subplot(111)
        
        categories = list(data.keys())
        if not categories:
            return fig
        
        subcategories = set()
        for cat_data in data.values():
            subcategories.update(cat_data.keys())
        subcategories = sorted(list(subcategories))
        
        colors = plt.cm.tab20(np.linspace(0, 1, len(subcategories)))
        
        bottom = np.zeros(len(categories))
        
        for i, subcat in enumerate(subcategories):
            values = [data[cat].get(subcat, 0) for cat in categories]
            ax.bar(categories, values, bottom=bottom, label=subcat, color=colors[i])
            bottom += np.array(values)
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend(loc='upper right')
        
        if self.theme_manager:
            text_color = 'white' if self.theme_manager.is_dark else 'black'
            ax.tick_params(colors=text_color)
            ax.xaxis.label.set_color(text_color)
            ax.yaxis.label.set_color(text_color)
            ax.title.set_color(text_color)
            legend = ax.get_legend()
            if legend:
                for text in legend.get_texts():
                    text.set_color(text_color)
        
        fig.tight_layout()
        return fig

    def create_grouped_bar(self, data: Dict[str, Dict[str, int]], title: str,
                           xlabel: str = '', ylabel: str = 'Count', figsize=(10, 5)) -> Figure:
        fig = self.create_figure(figsize)
        ax = fig.add_subplot(111)
        
        categories = list(data.keys())
        if not categories:
            return fig
        
        subcategories = set()
        for cat_data in data.values():
            subcategories.update(cat_data.keys())
        subcategories = sorted(list(subcategories))
        
        x = np.arange(len(categories))
        width = 0.8 / len(subcategories)
        
        colors = plt.cm.tab20(np.linspace(0, 1, len(subcategories)))
        
        for i, subcat in enumerate(subcategories):
            values = [data[cat].get(subcat, 0) for cat in categories]
            offset = width * (i - len(subcategories)/2 + 0.5)
            ax.bar(x + offset, values, width, label=subcat, color=colors[i])
        
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.legend(loc='upper right')
        
        if self.theme_manager:
            text_color = 'white' if self.theme_manager.is_dark else 'black'
            ax.tick_params(colors=text_color)
            ax.xaxis.label.set_color(text_color)
            ax.yaxis.label.set_color(text_color)
            ax.title.set_color(text_color)
            legend = ax.get_legend()
            if legend:
                for text in legend.get_texts():
                    text.set_color(text_color)
        
        fig.tight_layout()
        return fig


ChartsFrame = ScrollableChartsFrame

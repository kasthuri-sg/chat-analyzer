import tkinter as tk
from tkinter import ttk
from typing import Optional


class StatCard(ttk.Frame):
    def __init__(self, parent, title: str, value: str = "0", icon: str = "", theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.title = title
        self.icon = icon
        
        self._create_widgets()
        self.set_value(value)

    def _create_widgets(self):
        style = ttk.Style()
        
        self.container = ttk.Frame(self, padding=10)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        self.icon_label = ttk.Label(
            self.container,
            text=self.icon,
            font=('Segoe UI Emoji', 24)
        )
        self.icon_label.pack(pady=(0, 5))

        self.value_label = ttk.Label(
            self.container,
            text="0",
            font=('Segoe UI', 20, 'bold')
        )
        self.value_label.pack()

        self.title_label = ttk.Label(
            self.container,
            text=self.title,
            font=('Segoe UI', 10)
        )
        self.title_label.pack(pady=(5, 0))

    def set_value(self, value):
        self.value_label.config(text=str(value))

    def update_theme(self):
        pass


class StatCardsRow(ttk.Frame):
    def __init__(self, parent, cards_data: list, theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.cards = []
        
        self._create_cards(cards_data)

    def _create_cards(self, cards_data: list):
        for i, card_info in enumerate(cards_data):
            card = StatCard(
                self,
                title=card_info.get('title', ''),
                value=card_info.get('value', '0'),
                icon=card_info.get('icon', ''),
                theme_manager=self.theme_manager
            )
            card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            self.columnconfigure(i, weight=1)
            self.cards.append(card)

    def update_values(self, values: list):
        for i, value in enumerate(values):
            if i < len(self.cards):
                self.cards[i].set_value(value)

    def update_theme(self):
        for card in self.cards:
            card.update_theme()

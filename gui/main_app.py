import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Dict, Any
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.analyzer import ChatAnalyzer
from core.emoji_parser import EmojiParser
from core.sentiment import SentimentAnalyzer
from core.response_time import ResponseTimeAnalyzer
from core.html_exporter import HTMLExporter
from .theme import ThemeManager
from .widgets.file_loader import FileLoaderWidget
from .widgets.stat_cards import StatCardsRow
from .widgets.charts_frame import ChartsFrame


class ChatAnalyzerApp:
    PERSON_COLORS = ['#6366f1', '#8b5cf6', '#22d3ee', '#10b981', '#f59e0b', '#ef4444', '#ec4899', '#14b8a6']
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Chat Analyzer - Telegram Insights")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)

        self.theme_manager = ThemeManager(root, initial_dark=True)
        
        self.analyzer: Optional[ChatAnalyzer] = None
        self.emoji_parser = EmojiParser()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.response_analyzer = ResponseTimeAnalyzer()
        
        self.current_data = None
        self.current_tab = None
        
        self._create_menu()
        self._create_header()
        self._create_notebook()
        self._create_status_bar()

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File...", command=self._open_file_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Export Report...", command=self._export_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Dark/Light Mode", command=self.theme_manager.toggle_theme)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="How to Export Telegram Chat", command=self._show_help)

    def _create_header(self):
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill=tk.X)

        title_label = ttk.Label(
            header_frame,
            text="📊 Chat Analyzer",
            font=('Segoe UI', 20, 'bold')
        )
        title_label.pack(side=tk.LEFT, padx=10)

        subtitle_label = ttk.Label(
            header_frame,
            text="Decode Your Telegram Chats",
            font=('Segoe UI', 11)
        )
        subtitle_label.pack(side=tk.LEFT, padx=(0, 20))

        self.theme_btn = ttk.Button(
            header_frame,
            text="🌙 Dark",
            command=self._toggle_theme,
            width=10
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=5)

        export_btn = ttk.Button(
            header_frame,
            text="📄 Export",
            command=self._export_report,
            width=10
        )
        export_btn.pack(side=tk.RIGHT, padx=5)

        load_btn = ttk.Button(
            header_frame,
            text="📁 Load File",
            command=self._open_file_dialog,
            width=10
        )
        load_btn.pack(side=tk.RIGHT, padx=5)

    def _create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_change)

        self.dashboard_frame = ttk.Frame(self.notebook)
        self.activity_frame = ttk.Frame(self.notebook)
        self.comparison_frame = ttk.Frame(self.notebook)
        self.words_frame = ttk.Frame(self.notebook)
        self.advanced_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.dashboard_frame, text='📊 Dashboard')
        self.notebook.add(self.activity_frame, text='📈 Activity')
        self.notebook.add(self.comparison_frame, text='👥 Comparison')
        self.notebook.add(self.words_frame, text='📝 Words & Emojis')
        self.notebook.add(self.advanced_frame, text='🔬 Advanced')

        self._setup_dashboard_tab()
        self._setup_activity_tab()
        self._setup_comparison_tab()
        self._setup_words_tab()
        self._setup_advanced_tab()

        for frame in [self.dashboard_frame, self.activity_frame, self.comparison_frame, 
                      self.words_frame, self.advanced_frame]:
            self._show_empty_state(frame)

    def _setup_dashboard_tab(self):
        self.dashboard_content = ttk.Frame(self.dashboard_frame)
        self.dashboard_content.pack(fill=tk.BOTH, expand=True)

        self.file_loader = FileLoaderWidget(
            self.dashboard_content,
            on_load_callback=self._on_file_loaded,
            theme_manager=self.theme_manager
        )
        self.file_loader.pack(fill=tk.BOTH, expand=True, pady=50)

        self.dashboard_stats_frame = ttk.Frame(self.dashboard_content)

        self.dashboard_charts = ChartsFrame(self.dashboard_content, theme_manager=self.theme_manager)

    def _setup_activity_tab(self):
        self.activity_content = ttk.Frame(self.activity_frame)
        self.activity_content.pack(fill=tk.BOTH, expand=True)

        self.activity_charts = ChartsFrame(self.activity_content, theme_manager=self.theme_manager)
        self.activity_charts.pack(fill=tk.BOTH, expand=True)

    def _setup_comparison_tab(self):
        self.comparison_content = ttk.Frame(self.comparison_frame)
        self.comparison_content.pack(fill=tk.BOTH, expand=True)

        self.comparison_charts = ChartsFrame(self.comparison_content, theme_manager=self.theme_manager)
        self.comparison_charts.pack(fill=tk.BOTH, expand=True)

    def _setup_words_tab(self):
        self.words_content = ttk.Frame(self.words_frame)
        self.words_content.pack(fill=tk.BOTH, expand=True)

        self.words_charts = ChartsFrame(self.words_content, theme_manager=self.theme_manager)
        self.words_charts.pack(fill=tk.BOTH, expand=True)

    def _setup_advanced_tab(self):
        self.advanced_content = ttk.Frame(self.advanced_frame)
        self.advanced_content.pack(fill=tk.BOTH, expand=True)

        self.advanced_charts = ChartsFrame(self.advanced_content, theme_manager=self.theme_manager)
        self.advanced_charts.pack(fill=tk.BOTH, expand=True)

    def _show_empty_state(self, frame):
        empty_label = ttk.Label(
            frame,
            text="Load a chat file to see analysis",
            font=('Segoe UI', 14)
        )
        empty_label.pack(expand=True)

    def _on_file_loaded(self, data: Dict[str, Any]):
        self.current_data = data
        self._analyze_data()

    def _analyze_data(self):
        if not self.current_data:
            return

        self.analyzer = ChatAnalyzer(self.current_data)
        
        self.emoji_parser.reset()
        self.sentiment_analyzer.reset()
        self.response_analyzer.reset()

        emoji_stats = self.emoji_parser.analyze_messages(self.analyzer.messages)
        sentiment_stats = self.sentiment_analyzer.analyze_messages(self.analyzer.messages)
        response_stats = self.response_analyzer.analyze_messages(self.analyzer.messages)

        self._update_all_tabs()

    def _get_person_color(self, person: str, index: int = None) -> str:
        if index is not None:
            return self.PERSON_COLORS[index % len(self.PERSON_COLORS)]
        if person in self._person_color_map:
            return self._person_color_map[person]
        return self.PERSON_COLORS[0]

    def _build_color_map(self):
        self._person_color_map = {}
        for i, person in enumerate(self.analyzer.participants.keys()):
            self._person_color_map[person] = self.PERSON_COLORS[i % len(self.PERSON_COLORS)]

    def _update_all_tabs(self):
        self._build_color_map()
        self._update_dashboard()
        self._update_activity_tab()
        self._update_comparison_tab()
        self._update_words_tab()
        self._update_advanced_tab()

    def _update_dashboard(self):
        self.file_loader.pack_forget()
        
        for widget in self.dashboard_stats_frame.winfo_children():
            widget.destroy()
        self.dashboard_stats_frame.pack(fill=tk.X, pady=10)

        summary = self.analyzer.get_summary()
        
        cards_data = [
            {'title': 'Messages', 'value': f"{summary['total_messages']:,}", 'icon': '📨'},
            {'title': 'Words', 'value': f"{summary['total_words']:,}", 'icon': '📝'},
            {'title': 'Characters', 'value': f"{summary['total_characters']:,}", 'icon': '🔤'},
            {'title': 'Participants', 'value': str(summary['total_participants']), 'icon': '👥'},
            {'title': 'Days Active', 'value': str(summary['total_days']), 'icon': '📅'},
        ]
        
        stats_row = StatCardsRow(self.dashboard_stats_frame, cards_data, self.theme_manager)
        stats_row.pack(fill=tk.X, pady=10)

        averages = self.analyzer.get_averages()
        
        avg_frame = ttk.LabelFrame(self.dashboard_stats_frame, text="Averages", padding=10)
        avg_frame.pack(fill=tk.X, pady=10, padx=10)
        
        avg_labels = [
            f"Words/Message: {averages['words_per_message']:.1f}",
            f"Chars/Message: {averages['chars_per_message']:.1f}",
            f"Messages/Day: {averages['messages_per_day']:.1f}",
            f"Words/Day: {averages['words_per_day']:.1f}",
        ]
        
        for i, label_text in enumerate(avg_labels):
            ttk.Label(avg_frame, text=label_text, font=('Segoe UI', 10)).grid(row=0, column=i, padx=20, pady=5)

        date_range = summary['date_range']
        if date_range[0]:
            range_frame = ttk.LabelFrame(self.dashboard_stats_frame, text="Date Range", padding=10)
            range_frame.pack(fill=tk.X, pady=10, padx=10)
            ttk.Label(range_frame, text=f"From: {date_range[0]}  →  To: {date_range[1]}", 
                     font=('Segoe UI', 11)).pack()

        self.dashboard_charts.clear()
        self.dashboard_charts.pack(fill=tk.BOTH, expand=True)

        fig = self.dashboard_charts.create_pie_chart(
            summary['participants'],
            "Messages Distribution",
            figsize=(6, 5)
        )
        self.dashboard_charts.embed_figure(fig, row=0, column=0)

    def _update_activity_tab(self):
        self.activity_charts.clear()
        self.activity_content.pack(fill=tk.BOTH, expand=True)

        heatmap_data = self.analyzer.get_heatmap_data()
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        hours = [f'{h:02d}' for h in range(24)]
        
        fig = self.activity_charts.create_heatmap(
            heatmap_data,
            "Activity Heatmap (Day × Hour)",
            xlabels=hours,
            ylabels=days,
            figsize=(14, 5)
        )
        self.activity_charts.embed_figure(fig, row=0, column=0)

        hourly_data = self.analyzer.get_hourly_activity()
        fig2 = self.activity_charts.create_bar_chart(
            hourly_data,
            "Hourly Activity",
            xlabel="Hour",
            ylabel="Messages",
            figsize=(12, 4)
        )
        self.activity_charts.embed_figure(fig2, row=1, column=0)

        daily_data = self.analyzer.get_daily_activity()
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_ordered = {day: daily_data.get(day, 0) for day in days_order}
        
        fig3 = self.activity_charts.create_bar_chart(
            daily_ordered,
            "Messages by Day of Week",
            xlabel="Day",
            ylabel="Messages",
            figsize=(10, 4)
        )
        self.activity_charts.embed_figure(fig3, row=2, column=0)

    def _update_comparison_tab(self):
        self.comparison_charts.clear()
        self.comparison_content.pack(fill=tk.BOTH, expand=True)
        
        person_colors = {p: self._get_person_color(p, i) for i, p in enumerate(self.analyzer.participants.keys())}

        fig = self.comparison_charts.create_bar_chart(
            self.analyzer.participants,
            "Total Messages by Person",
            xlabel="Person",
            ylabel="Messages",
            figsize=(10, 5)
        )
        self.comparison_charts.embed_figure(fig, row=0, column=0)

        word_counts = dict(self.analyzer.word_count)
        fig2 = self.comparison_charts.create_bar_chart(
            word_counts,
            "Total Words by Person",
            xlabel="Person",
            ylabel="Words",
            figsize=(10, 5)
        )
        self.comparison_charts.embed_figure(fig2, row=1, column=0)

        hourly_by_person = self.analyzer.get_hourly_by_person()
        hourly_comparison = {}
        for hour, persons in hourly_by_person.items():
            hourly_comparison[hour] = dict(persons)

        fig3 = self.comparison_charts.create_grouped_bar(
            hourly_comparison,
            "Hourly Activity Comparison",
            xlabel="Hour",
            ylabel="Messages",
            figsize=(14, 5)
        )
        self.comparison_charts.embed_figure(fig3, row=2, column=0)

        daily_by_person = self.analyzer.get_daily_by_person()
        daily_comparison = {}
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days_order:
            daily_comparison[day] = {}
            for person, stats in daily_by_person.items():
                daily_comparison[day][person] = stats.get(day, 0)
        
        fig4 = self.comparison_charts.create_grouped_bar(
            daily_comparison,
            "Daily Activity Comparison",
            xlabel="Day",
            ylabel="Messages",
            figsize=(12, 5)
        )
        self.comparison_charts.embed_figure(fig4, row=3, column=0)

        char_counts = dict(self.analyzer.char_count)
        fig5 = self.comparison_charts.create_bar_chart(
            char_counts,
            "Total Characters by Person",
            xlabel="Person",
            ylabel="Characters",
            figsize=(10, 5)
        )
        self.comparison_charts.embed_figure(fig5, row=4, column=0)

    def _update_words_tab(self):
        self.words_charts.clear()
        self.words_content.pack(fill=tk.BOTH, expand=True)

        top_words = self.analyzer.get_most_used_words(15)
        words_dict = dict(top_words)

        fig = self.words_charts.create_bar_chart(
            words_dict,
            "Most Used Words",
            xlabel="Word",
            ylabel="Count",
            figsize=(12, 5),
            horizontal=True
        )
        self.words_charts.embed_figure(fig, row=0, column=0)

        emoji_stats = self.emoji_parser.get_stats()
        if emoji_stats['top_emojis']:
            emoji_dict = {e[0]: e[1] for e in emoji_stats['top_emojis'][:10]}

            fig2 = self.words_charts.create_pie_chart(
                emoji_dict,
                "Top Emojis",
                figsize=(7, 7)
            )
            self.words_charts.embed_figure(fig2, row=1, column=0)

        emoji_by_person = emoji_stats.get('by_person', {})
        if emoji_by_person:
            emoji_counts = {}
            for person, emojis in emoji_by_person.items():
                emoji_counts[person] = sum(count for _, count in emojis)
            
            fig_emoji = self.words_charts.create_bar_chart(
                emoji_counts,
                "Emoji Usage by Person",
                xlabel="Person",
                ylabel="Total Emojis",
                figsize=(10, 4)
            )
            self.words_charts.embed_figure(fig_emoji, row=2, column=0)

        for i, person in enumerate(self.analyzer.participants.keys()):
            person_words = self.analyzer.get_words_by_person(person, 10)
            if person_words:
                person_words_dict = dict(person_words)
                fig3 = self.words_charts.create_bar_chart(
                    person_words_dict,
                    f"Top Words by {person}",
                    figsize=(10, 4),
                    horizontal=True
                )
                self.words_charts.embed_figure(fig3, row=3 + i, column=0)

    def _update_advanced_tab(self):
        self.advanced_charts.clear()
        self.advanced_content.pack(fill=tk.BOTH, expand=True)

        sentiment_stats = self.sentiment_analyzer.get_stats()
        overall = sentiment_stats['overall']
        
        sentiment_data = {
            'Positive': overall['positive'],
            'Negative': overall['negative'],
        }
        
        fig = self.advanced_charts.create_pie_chart(
            sentiment_data,
            f"Overall Sentiment (Positive: {overall['positive_ratio']*100:.1f}%)",
            figsize=(6, 6)
        )
        self.advanced_charts.embed_figure(fig, row=0, column=0)

        slang_stats = self.sentiment_analyzer.get_top_slang(10)
        if slang_stats:
            slang_dict = {f"{s[0]} ({s[2]})": s[1] for s in slang_stats}
            fig2 = self.advanced_charts.create_bar_chart(
                slang_dict,
                "Most Used Slang Terms",
                figsize=(10, 5),
                horizontal=True
            )
            self.advanced_charts.embed_figure(fig2, row=1, column=0)

        response_stats = self.response_analyzer.get_stats()
        by_person = response_stats.get('by_person', {})
        
        if by_person:
            response_times = {
                person: stats['average'] 
                for person, stats in by_person.items() 
                if stats['average'] > 0
            }
            if response_times:
                for person in response_times:
                    response_times[person] = response_times[person] / 60
                
                fig3 = self.advanced_charts.create_bar_chart(
                    response_times,
                    "Average Response Time (minutes)",
                    figsize=(10, 5),
                    horizontal=True
                )
                self.advanced_charts.embed_figure(fig3, row=2, column=0)

        starters = response_stats.get('conversation_starters', {})
        if starters:
            fig4 = self.advanced_charts.create_bar_chart(
                starters,
                "Conversation Starters",
                ylabel="Times Started",
                figsize=(8, 4)
            )
            self.advanced_charts.embed_figure(fig4, row=3, column=0)

    def _on_tab_change(self, event):
        pass

    def _toggle_theme(self):
        self.theme_manager.toggle_theme()
        self.theme_btn.config(text="☀️ Light" if self.theme_manager.is_dark else "🌙 Dark")
        
        if self.analyzer:
            self._update_all_tabs()

    def _open_file_dialog(self):
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(
            title="Select Chat JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            self.analyzer = ChatAnalyzer()
            if self.analyzer.load_from_file(filepath):
                self.current_data = self.analyzer.data
                self._analyze_data()

    def _export_report(self):
        if not self.analyzer:
            messagebox.showinfo("Info", "Please load a chat file first.")
            return
        
        default_filename = f"chat_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = filedialog.asksaveasfilename(
            title="Export HTML Report",
            defaultextension=".html",
            initialfile=default_filename,
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        self.status_var.set("Exporting report...")
        self.root.update()
        
        try:
            exporter = HTMLExporter()
            success = exporter.export(
                self.analyzer,
                self.emoji_parser,
                self.sentiment_analyzer,
                self.response_analyzer,
                filepath
            )
            
            if success:
                self.status_var.set(f"Report exported: {os.path.basename(filepath)}")
                messagebox.showinfo(
                    "Export Successful",
                    f"Report saved to:\n{filepath}\n\nOpen it in your browser to view the full analysis!"
                )
            else:
                self.status_var.set("Export failed")
                messagebox.showerror("Export Error", "Failed to export report. Please try again.")
        except Exception as e:
            self.status_var.set("Export failed")
            messagebox.showerror("Export Error", f"An error occurred:\n{str(e)}")

    def _show_about(self):
        messagebox.showinfo(
            "About Chat Analyzer",
            "Chat Analyzer v1.0\n\n"
            "A tool for analyzing Telegram chat exports.\n\n"
            "Features:\n"
            "• Message statistics\n"
            "• Activity patterns\n"
            "• Emoji analysis\n"
            "• Sentiment analysis\n"
            "• Response time tracking\n"
            "• Slang detection\n\n"
            "Built with Python & Tkinter"
        )

    def _show_help(self):
        messagebox.showinfo(
            "How to Export Telegram Chat",
            "Steps to get your chat file:\n\n"
            "1. Open Telegram app on your PC\n"
            "2. Go to your preferred chat\n"
            "3. Click on three dots (⋮) on top right\n"
            "4. Click 'Export chat history'\n"
            "5. Select JSON format\n"
            "6. Save and load in this app"
        )

    def _create_status_bar(self):
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)


def run_app():
    root = tk.Tk()
    app = ChatAnalyzerApp(root)
    root.mainloop()


if __name__ == '__main__':
    run_app()

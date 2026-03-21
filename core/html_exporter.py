"""
HTML Export Module for Chat Analyzer
Generates a beautiful single-file HTML report with dark glassmorphism design
All charts from desktop app included
"""

import json
from datetime import datetime
from typing import Dict, Any, List


class HTMLExporter:
    def __init__(self):
        self.chart_colors = [
            '#6366f1', '#8b5cf6', '#22d3ee', '#10b981', '#f59e0b', '#ef4444',
            '#ec4899', '#14b8a6', '#f97316', '#a855f7', '#06b6d4', '#84cc16'
        ]

    def export(self, analyzer, emoji_parser, sentiment_analyzer, response_analyzer, output_path: str) -> bool:
        try:
            html_content = self._generate_html(
                analyzer, emoji_parser, sentiment_analyzer, response_analyzer
            )
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _generate_html(self, analyzer, emoji_parser, sentiment_analyzer, response_analyzer) -> str:
        summary = analyzer.get_summary()
        averages = analyzer.get_averages()
        emoji_stats = emoji_parser.get_stats()
        sentiment_stats = sentiment_analyzer.get_stats()
        response_stats = response_analyzer.get_stats()

        participants = dict(analyzer.participants)
        person_names = list(participants.keys())
        hourly = dict(analyzer.get_hourly_activity())
        daily = dict(analyzer.get_daily_activity())
        daily_by_person = analyzer.get_daily_by_person()
        hourly_by_person = analyzer.get_hourly_by_person()
        words = analyzer.get_most_used_words(15)
        top_emojis = emoji_stats['top_emojis'][:10]
        emoji_by_person = emoji_stats.get('by_person', {})
        slang = sentiment_analyzer.get_top_slang(10)
        
        response_by_person = response_stats.get('by_person', {})
        response_times = [v.get('average', 0)/60 for v in response_by_person.values()]
        starters = response_stats.get('conversation_starters', {})
        
        word_count = dict(analyzer.word_count)
        char_count = dict(analyzer.char_count)
        
        words_by_person = {}
        for person in participants.keys():
            words_by_person[person] = dict(analyzer.get_words_by_person(person, 10))
        
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        emoji_counts_by_person = {}
        for person, emojis in emoji_by_person.items():
            emoji_counts_by_person[person] = sum(count for _, count in emojis)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Analysis Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%);
            min-height: 100vh;
            color: #e2e8f0;
            line-height: 1.6;
        }}

        .bg-pattern {{
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 80%, rgba(34, 211, 238, 0.08) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }}

        .header {{
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 40px;
        }}

        .header h1 {{
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #6366f1, #8b5cf6, #22d3ee);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }}

        .header .subtitle {{ color: #94a3b8; font-size: 1.1rem; }}
        .header .date {{ color: #64748b; font-size: 0.9rem; margin-top: 10px; }}

        .glass-card {{
            background: rgba(30, 30, 60, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}

        .glass-card:hover {{
            border-color: rgba(99, 102, 241, 0.3);
        }}

        .card-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: #f1f5f9;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(99, 102, 241, 0.2);
        }}

        .stat-card .icon {{ font-size: 1.8rem; margin-bottom: 8px; }}
        .stat-card .value {{ font-size: 1.8rem; font-weight: 700; color: #22d3ee; margin-bottom: 5px; }}
        .stat-card .label {{ font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }}

        .chart-container {{ position: relative; height: 280px; }}
        .chart-container.medium {{ height: 320px; }}
        .chart-container.large {{ height: 400px; }}

        .section {{ margin-bottom: 40px; }}

        .section-title {{
            font-size: 1.6rem;
            font-weight: 600;
            color: #f1f5f9;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(99, 102, 241, 0.3);
        }}

        .two-cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }}
        .three-cols {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }}

        @media (max-width: 1000px) {{
            .two-cols, .three-cols {{ grid-template-columns: 1fr; }}
            .header h1 {{ font-size: 2rem; }}
        }}

        .insight-card {{
            background: rgba(34, 211, 238, 0.1);
            border-left: 4px solid #22d3ee;
            padding: 15px 20px;
            margin: 10px 0;
            border-radius: 0 10px 10px 0;
        }}

        .insight-card strong {{ color: #22d3ee; }}

        .person-legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin: 15px 0;
        }}

        .person-legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .person-color {{
            width: 16px;
            height: 16px;
            border-radius: 4px;
        }}

        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #64748b;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 40px;
        }}

        .person-color-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-bottom: 20px;
        }}

        .person-color-card {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }}

        .person-color-card .color-box {{
            width: 24px;
            height: 24px;
            border-radius: 6px;
        }}

        .person-color-card .name {{
            font-weight: 600;
            color: #f1f5f9;
        }}
    </style>
</head>
<body>
    <div class="bg-pattern"></div>
    
    <div class="container">
        <header class="header">
            <h1>📊 Chat Analysis Report</h1>
            <p class="subtitle">Complete insights into your Telegram conversations</p>
            <p class="date">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </header>

        <section class="section">
            <h2 class="section-title">📈 Overview</h2>
            <div class="stats-grid">
                <div class="stat-card"><div class="icon">📨</div><div class="value">{summary['total_messages']:,}</div><div class="label">Messages</div></div>
                <div class="stat-card"><div class="icon">📝</div><div class="value">{summary['total_words']:,}</div><div class="label">Words</div></div>
                <div class="stat-card"><div class="icon">🔤</div><div class="value">{summary['total_characters']:,}</div><div class="label">Characters</div></div>
                <div class="stat-card"><div class="icon">👥</div><div class="value">{summary['total_participants']}</div><div class="label">Participants</div></div>
                <div class="stat-card"><div class="icon">📅</div><div class="value">{summary['total_days']}</div><div class="label">Days Active</div></div>
                <div class="stat-card"><div class="icon">⚡</div><div class="value">{averages['messages_per_day']:.1f}</div><div class="label">Msgs/Day</div></div>
                <div class="stat-card"><div class="icon">📊</div><div class="value">{averages['words_per_message']:.1f}</div><div class="label">Words/Msg</div></div>
                <div class="stat-card"><div class="icon">🔤</div><div class="value">{averages['chars_per_message']:.0f}</div><div class="label">Chars/Msg</div></div>
            </div>
        </section>

        <section class="section">
            <div class="glass-card">
                <h3 class="card-title"><span>🗓️</span> Conversation Period</h3>
                <p style="font-size: 1.5rem; text-align: center; margin: 20px 0;">
                    <strong style="color: #6366f1;">{summary['date_range'][0]}</strong>
                    <span style="color: #64748b; margin: 0 20px;">→</span>
                    <strong style="color: #8b5cf6;">{summary['date_range'][1]}</strong>
                </p>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">👥 Participants</h2>
            <div class="glass-card">
                <h3 class="card-title"><span>🎨</span> Person Colors (used throughout report)</h3>
                <div class="person-color-grid">
                    {self._generate_person_color_legend(list(participants.keys()))}
                </div>
            </div>
            <div class="glass-card">
                <h3 class="card-title"><span>📊</span> Message Distribution</h3>
                <div class="chart-container medium"><canvas id="participantsChart"></canvas></div>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">📈 Activity Patterns</h2>
            
            <div class="glass-card">
                <h3 class="card-title"><span>🔥</span> Activity Heatmap (Day × Hour)</h3>
                <div class="chart-container large"><canvas id="heatmapChart"></canvas></div>
            </div>
            
            <div class="two-cols">
                <div class="glass-card">
                    <h3 class="card-title"><span>🕐</span> Hourly Activity (Total)</h3>
                    <div class="chart-container"><canvas id="hourlyChart"></canvas></div>
                </div>
                <div class="glass-card">
                    <h3 class="card-title"><span>📆</span> Daily Activity (Total)</h3>
                    <div class="chart-container"><canvas id="dailyChart"></canvas></div>
                </div>
            </div>

            <div class="glass-card">
                <h3 class="card-title"><span>👤</span> Hourly Activity by Person</h3>
                <div class="chart-container medium"><canvas id="hourlyByPersonChart"></canvas></div>
            </div>

            <div class="glass-card">
                <h3 class="card-title"><span>👤</span> Daily Activity by Person</h3>
                <div class="chart-container medium"><canvas id="dailyByPersonChart"></canvas></div>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">📊 Comparison</h2>
            
            <div class="three-cols">
                <div class="glass-card">
                    <h3 class="card-title"><span>📨</span> Messages by Person</h3>
                    <div class="chart-container"><canvas id="messagesChart"></canvas></div>
                </div>
                <div class="glass-card">
                    <h3 class="card-title"><span>📝</span> Words by Person</h3>
                    <div class="chart-container"><canvas id="wordsByPersonChart"></canvas></div>
                </div>
                <div class="glass-card">
                    <h3 class="card-title"><span>🔤</span> Characters by Person</h3>
                    <div class="chart-container"><canvas id="charsByPersonChart"></canvas></div>
                </div>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">📝 Word Analysis</h2>
            
            <div class="glass-card">
                <h3 class="card-title"><span>🔤</span> Most Used Words (Overall)</h3>
                <div class="chart-container medium"><canvas id="topWordsChart"></canvas></div>
            </div>

            {self._generate_words_by_person_section(words_by_person)}
        </section>

        <section class="section">
            <h2 class="section-title">😀 Emoji Analysis</h2>
            
            <div class="two-cols">
                <div class="glass-card">
                    <h3 class="card-title"><span>😊</span> Top Emojis</h3>
                    <div class="chart-container medium"><canvas id="emojiChart"></canvas></div>
                </div>
                <div class="glass-card">
                    <h3 class="card-title"><span>📊</span> Emoji Usage by Person</h3>
                    <div class="chart-container"><canvas id="emojiByPersonChart"></canvas></div>
                </div>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">🎭 Sentiment & Slang</h2>
            
            <div class="two-cols">
                <div class="glass-card">
                    <h3 class="card-title"><span>💭</span> Sentiment Distribution</h3>
                    <div class="chart-container"><canvas id="sentimentChart"></canvas></div>
                </div>
                <div class="glass-card">
                    <h3 class="card-title"><span>💬</span> Slang Usage</h3>
                    <div class="chart-container"><canvas id="slangChart"></canvas></div>
                </div>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">⏱️ Response Time</h2>
            
            <div class="two-cols">
                <div class="glass-card">
                    <h3 class="card-title"><span>⚡</span> Avg Response Time (minutes)</h3>
                    <div class="chart-container"><canvas id="responseChart"></canvas></div>
                </div>
                <div class="glass-card">
                    <h3 class="card-title"><span>🚀</span> Conversation Starters</h3>
                    <div class="chart-container"><canvas id="startersChart"></canvas></div>
                </div>
            </div>
        </section>

        <section class="section">
            <h2 class="section-title">💡 Key Insights</h2>
            <div class="glass-card">
                {self._generate_insights(analyzer, emoji_parser, sentiment_analyzer, response_analyzer)}
            </div>
        </section>

        <footer class="footer">
            <p>Generated by <strong>Chat Analyzer v1.0</strong> • Privacy-first analysis tool</p>
            <p style="margin-top: 10px;">Your data never leaves your computer 💻</p>
            <p style="margin-top: 15px;">
                <a href="https://github.com/kasthuri-sg/chat-analyzer" target="_blank" style="color: #6366f1; text-decoration: none;">
                    ⭐ Star on GitHub
                </a>
            </p>
        </footer>
    </div>

    <script>
        const colors = {json.dumps(self.chart_colors)};
        const personColors = {json.dumps([self.chart_colors[i % len(self.chart_colors)] for i in range(len(participants))])};
        const personNames = {json.dumps(list(participants.keys()))};
        const gridColor = 'rgba(255, 255, 255, 0.1)';
        const textColor = '#e2e8f0';
        
        Chart.defaults.color = textColor;
        Chart.defaults.borderColor = gridColor;

        // Helper for person-colored datasets
        function getPersonDatasets(groupedData, isTimeData = false) {{
            return personNames.map((name, i) => ({{
                label: name,
                data: Object.values(groupedData).map(d => d[name] || 0),
                backgroundColor: personColors[i],
                borderColor: personColors[i],
                borderWidth: 1,
                borderRadius: 4
            }}));
        }}

        // Participants Distribution
        new Chart(document.getElementById('participantsChart'), {{
            type: 'doughnut',
            data: {{
                labels: personNames,
                datasets: [{{ data: {json.dumps(list(participants.values()))}, backgroundColor: personColors, borderWidth: 0 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ position: 'bottom' }} }} }}
        }});

        // Heatmap-style chart (Daily totals by day)
        new Chart(document.getElementById('heatmapChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(days_order)},
                datasets: [{{ label: 'Messages', data: {json.dumps([daily.get(d, 0) for d in days_order])}, backgroundColor: colors[0], borderRadius: 5 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // Hourly Total
        new Chart(document.getElementById('hourlyChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(list(hourly.keys()))},
                datasets: [{{ label: 'Messages', data: {json.dumps(list(hourly.values()))}, backgroundColor: colors[1], borderRadius: 5 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // Daily Total
        new Chart(document.getElementById('dailyChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(days_order)},
                datasets: [{{ label: 'Messages', data: {json.dumps([daily.get(d, 0) for d in days_order])}, backgroundColor: colors[2], borderRadius: 5 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // Hourly by Person
        const hourlyByPerson = {json.dumps({k: dict(v) for k, v in hourly_by_person.items()})};
        new Chart(document.getElementById('hourlyByPersonChart'), {{
            type: 'bar',
            data: {{
                labels: Object.keys(hourlyByPerson),
                datasets: getPersonDatasets(hourlyByPerson)
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ position: 'top' }} }}, scales: {{ y: {{ beginAtZero: true, stacked: false, grid: {{ color: gridColor }} }}, x: {{ stacked: false, grid: {{ display: false }} }} }} }}
        }});

        // Daily by Person
        const dailyByPerson = {json.dumps(daily_by_person)};
        new Chart(document.getElementById('dailyByPersonChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(days_order)},
                datasets: personNames.map((name, i) => ({{
                    label: name,
                    data: {json.dumps(days_order)}.map(d => dailyByPerson[name] ? dailyByPerson[name][d] || 0 : 0),
                    backgroundColor: personColors[i],
                    borderRadius: 4
                }}))
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ position: 'top' }} }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // Messages by Person
        new Chart(document.getElementById('messagesChart'), {{
            type: 'bar',
            data: {{
                labels: personNames,
                datasets: [{{ data: {json.dumps(list(participants.values()))}, backgroundColor: personColors, borderRadius: 5 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // Words by Person
        new Chart(document.getElementById('wordsByPersonChart'), {{
            type: 'bar',
            data: {{
                labels: personNames,
                datasets: [{{ data: {json.dumps(list(word_count.values()))}, backgroundColor: personColors, borderRadius: 5 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // Characters by Person
        new Chart(document.getElementById('charsByPersonChart'), {{
            type: 'bar',
            data: {{
                labels: personNames,
                datasets: [{{ data: {json.dumps(list(char_count.values()))}, backgroundColor: personColors, borderRadius: 5 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // Top Words
        new Chart(document.getElementById('topWordsChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps([w[0] for w in words])},
                datasets: [{{ data: {json.dumps([w[1] for w in words])}, backgroundColor: colors[3], borderRadius: 5 }}]
            }},
            options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, y: {{ grid: {{ display: false }} }} }} }}
        }});

        // Top Emojis
        new Chart(document.getElementById('emojiChart'), {{
            type: 'pie',
            data: {{
                labels: {json.dumps(['Top ' + str(i+1) for i in range(len(top_emojis))])},
                datasets: [{{ data: {json.dumps([e[1] for e in top_emojis])}, backgroundColor: colors, borderWidth: 0 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ position: 'right' }} }} }}
        }});

        // Emoji by Person
        new Chart(document.getElementById('emojiByPersonChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(person_names)},
                datasets: [{{ data: {json.dumps([emoji_counts_by_person.get(p, 0) for p in person_names])}, backgroundColor: personColors, borderRadius: 5 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // Sentiment
        new Chart(document.getElementById('sentimentChart'), {{
            type: 'doughnut',
            data: {{
                labels: ['Positive', 'Negative'],
                datasets: [{{ data: [{sentiment_stats['overall']['positive']}, {sentiment_stats['overall']['negative']}], backgroundColor: ['#10b981', '#ef4444'], borderWidth: 0 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, cutout: '60%', plugins: {{ legend: {{ position: 'bottom' }} }} }}
        }});

        // Slang
        new Chart(document.getElementById('slangChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps([s[0] for s in slang])},
                datasets: [{{ data: {json.dumps([s[1] for s in slang])}, backgroundColor: colors[4], borderRadius: 5 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // Response Time
        new Chart(document.getElementById('responseChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(list(response_by_person.keys()))},
                datasets: [{{ data: {json.dumps(response_times)}, backgroundColor: personColors, borderRadius: 5 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // Starters
        new Chart(document.getElementById('startersChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(list(starters.keys()))},
                datasets: [{{ data: {json.dumps(list(starters.values()))}, backgroundColor: personColors, borderRadius: 5 }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, x: {{ grid: {{ display: false }} }} }} }}
        }});

        // Words by Person Charts
        {self._generate_words_by_person_js(words_by_person)}
    </script>
</body>
</html>"""

    def _generate_person_color_legend(self, person_names: List[str]) -> str:
        html = ""
        for i, name in enumerate(person_names):
            color = self.chart_colors[i % len(self.chart_colors)]
            html += f"""
            <div class="person-color-card">
                <div class="color-box" style="background: {color};"></div>
                <span class="name">{name}</span>
            </div>"""
        return html

    def _generate_words_by_person_section(self, words_by_person: Dict[str, Dict[str, int]]) -> str:
        html = ""
        for i, (person, words) in enumerate(words_by_person.items()):
            if words:
                color = self.chart_colors[i % len(self.chart_colors)]
                html += f"""
            <div class="glass-card">
                <h3 class="card-title"><span>📝</span> Top Words by {person}</h3>
                <div class="chart-container"><canvas id="wordsBy{i}Chart"></canvas></div>
            </div>"""
        return html

    def _generate_words_by_person_js(self, words_by_person: Dict[str, Dict[str, int]]) -> str:
        js = ""
        for i, (person, words) in enumerate(words_by_person.items()):
            if words:
                color = self.chart_colors[i % len(self.chart_colors)]
                labels = list(words.keys())[:10]
                values = list(words.values())[:10]
                js += f"""
        new Chart(document.getElementById('wordsBy{i}Chart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{ data: {json.dumps(values)}, backgroundColor: '{color}', borderRadius: 5 }}]
            }},
            options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ beginAtZero: true, grid: {{ color: gridColor }} }}, y: {{ grid: {{ display: false }} }} }} }}
        }});
"""
        return js

    def _generate_insights(self, analyzer, emoji_parser, sentiment_analyzer, response_analyzer) -> str:
        insights = []
        
        if analyzer.participants:
            top_poster = max(analyzer.participants.items(), key=lambda x: x[1])
            insights.append(f"<strong>{top_poster[0]}</strong> sent the most messages ({top_poster[1]:,})")
        
        hourly = analyzer.get_hourly_activity()
        if hourly:
            peak_hour = max(hourly.items(), key=lambda x: x[1])
            insights.append(f"Peak activity hour is <strong>{peak_hour[0]}:00</strong> with {peak_hour[1]} messages")
        
        daily = analyzer.get_daily_activity()
        if daily:
            peak_day = max(daily.items(), key=lambda x: x[1])
            insights.append(f"Most active day is <strong>{peak_day[0]}</strong> with {peak_day[1]} messages")
        
        response_stats = response_analyzer.get_stats()
        fastest = response_analyzer.get_fastest_responders(1)
        if fastest:
            insights.append(f"<strong>{fastest[0][0]}</strong> has the fastest average response time")
        
        starters = response_stats.get('conversation_starters', {})
        if starters:
            top_starter = max(starters.items(), key=lambda x: x[1])
            insights.append(f"<strong>{top_starter[0]}</strong> starts the most conversations ({top_starter[1]} times)")
        
        emoji_stats = emoji_parser.get_stats()
        if emoji_stats['top_emojis']:
            top_emoji = emoji_stats['top_emojis'][0]
            insights.append(f"Most used emoji: <strong>{top_emoji[0]}</strong> ({top_emoji[1]} times)")
        
        emoji_by_person = emoji_stats.get('by_person', {})
        if emoji_by_person:
            emoji_counts = {p: sum(c for _, c in emojis) for p, emojis in emoji_by_person.items()}
            top_emoji_user = max(emoji_counts.items(), key=lambda x: x[1])
            insights.append(f"<strong>{top_emoji_user[0]}</strong> uses the most emojis ({top_emoji_user[1]} total)")
        
        sentiment_stats = sentiment_analyzer.get_stats()
        pos_ratio = sentiment_stats['overall']['positive_ratio']
        if pos_ratio > 0.6:
            insights.append("Overall conversation tone is <strong>positive</strong> 😊")
        elif pos_ratio > 0.4:
            insights.append("Conversation has a <strong>balanced</strong> emotional tone")
        else:
            insights.append("Conversation tends to be more <strong>neutral/serious</strong>")
        
        return '\n'.join([f'<div class="insight-card">{i}</div>' for i in insights])

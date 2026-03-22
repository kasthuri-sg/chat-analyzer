# Chat Analyzer v1.0

**Privacy-first Telegram chat analysis tool that runs 100% locally on your computer.**

![Version](https://img.shields.io/badge/Version-1.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## Why Chat Analyzer?

Your chat history contains personal conversations, secrets, and sensitive information. Unlike online tools that require uploading your data to remote servers, **Chat Analyzer runs entirely on your machine**. Your data never leaves your computer.

- ✅ **100% Offline** - No internet required after installation
- ✅ **No Data Upload** - Your chats stay on your computer
- ✅ **No Account Needed** - No sign-ups, no tracking
- ✅ **Open Source** - Audit the code yourself

---

## Features

### 📊 Dashboard
- Total messages, words, characters count
- Participant breakdown with visual charts
- Date range of conversation
- Average statistics (messages/day, words/message, characters/message)

### 📈 Activity Analysis
- **Activity Heatmap** - GitHub-style day × hour grid showing when you chat most
- **Hourly Activity** - See which hours are most active (total & by person)
- **Daily Activity** - Compare weekdays vs weekends (total & by person)
- **Activity by Person** - See how each participant's activity varies

### 👥 Comparison
- **Messages by Person** - Total message count per participant
- **Words by Person** - Total word count per participant  
- **Characters by Person** - Total character count per participant
- **Hourly Activity Comparison** - Side-by-side hourly activity
- **Daily Activity Comparison** - Side-by-side daily activity
- **Person-specific Colors** - Each person has a unique color across all charts for easy identification

### 📝 Words & Emojis
- **Most Used Words** - Top 15 most frequently used words
- **Top Words by Person** - Individual word frequency for each participant
- **Emoji Analysis** - Total emoji usage statistics
- **Emoji Usage by Person** - See who uses the most emojis
- **Top Emojis** - Most frequently used emojis

### 🔬 Advanced Analysis
- **Sentiment Analysis** - Overall positive/negative sentiment ratio
- **Slang Detection** - Track slang terms like "lol", "brb", "tbh", "ngl", "fr", "cap", etc.
- **Response Time** - Average response time per person
- **Conversation Starters** - Who initiates conversations more often?
- **Vocabulary Strength** - Unique words ratio per person

### 🎨 User Interface
- Modern dark/light theme toggle
- Tab-based navigation
- Interactive Matplotlib charts
- Scrollable charts with scrollbars
- Drag-and-drop file loading
- Responsive layout

### 📄 HTML Export
- **Beautiful glassmorphism design** - Modern dark theme with glass effects
- **20+ interactive charts** - Using Chart.js for smooth animations
- **Person-specific colors** - Consistent colors for each person across all charts
- **Key Insights section** - Automatically generated insights
- **Single HTML file** - No external dependencies, easy to share
- **Mobile responsive** - Works on all screen sizes

---

## Highlight

- Use **HTML Export** to get the beautiful output.

---

## Installation

### Option 1: Run from Source

```bash
# Clone the repository
git clone https://github.com/kasthuri-sg/chat-analyzer.git
cd chat-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Option 2: Download Executable (No Python Required)

Download the latest release for your platform from the [Releases](https://github.com/kasthuri-sg/chat-analyzer/releases) page.

TBD

---

## How to Export Telegram Chat

1. Open **Telegram Desktop** on your computer
2. Open the chat you want to analyze
3. Click the **three dots (⋮)** in the top right corner
4. Select **Export chat history**
5. Choose **JSON format** (not HTML)
6. Select location and save
7. Load the exported file in Chat Analyzer

---

## Export to HTML

After analyzing your chat:

1. Click the **📄 Export** button in the header
2. Choose where to save the HTML file
3. Open the HTML file in any web browser
4. Share with friends or keep for your records!

The exported HTML includes:
- All 20+ interactive charts
- Person color legend
- Key insights summary
- Responsive design for all devices

---

## System Requirements

- **Python:** 3.8 or higher (only if running from source)
- **OS:** Windows 10+, macOS 10.14+, or Linux
- **RAM:** 512MB minimum (2GB recommended for large chats)
- **Storage:** 100MB for application

---

## Building from Source

### Create Executable with PyInstaller

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build.py

# Executable will be in dist/ folder
```

Or manually:

```bash
pyinstaller chat_analyzer.spec
```

---

## Project Structure

```
chat-analyzer/
├── core/                       # Analysis engine
│   ├── analyzer.py             # Main chat analyzer
│   ├── emoji_parser.py         # Emoji detection & counting
│   ├── sentiment.py            # Sentiment & slang analysis
│   ├── response_time.py        # Response time tracking
│   └── html_exporter.py        # HTML report generator
├── gui/                        # User interface
│   ├── main_app.py             # Main Tkinter application
│   ├── theme.py                # Dark/light theme manager
│   └── widgets/                # UI components
│       ├── file_loader.py      # File upload widget
│       ├── stat_cards.py       # Statistics cards
│       └── charts_frame.py     # Scrollable chart renderer
├── data/                       # Sample data
│   └── sample_chat.json        # Test data
├── screenshots/                # Screenshots for docs
├── main.py                     # Entry point
├── build.py                    # Build script
├── chat_analyzer.spec          # PyInstaller spec
├── requirements.txt            # Dependencies
├── LICENSE                     # MIT License
└── README.md                   # Documentation
```

---

## Dependencies

All dependencies are standard Python packages:

```
matplotlib>=3.7.0    # Chart rendering
wordcloud>=1.9.0    # Word cloud generation (optional)
emoji>=2.8.0        # Emoji detection
numpy>=1.24.0       # Numerical operations
Pillow>=10.0.0      # Image processing
```

No external API calls. No internet required.

---

## Privacy Policy

**TL;DR: Your data never leaves your computer.**

- Chat Analyzer processes all data locally
- No internet connection required
- No telemetry or analytics collected
- No user accounts or registration
- Open source code for transparency

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Changelog

### v1.0 (Initial Release)

**Features:**
- Complete chat analysis with 20+ visualizations
- Desktop GUI with dark/light theme
- HTML export with glassmorphism design
- Person-specific colors across all charts
- Emoji analysis per person
- Sentiment and slang detection
- Response time tracking
- Conversation starter detection
- Scrollable charts window
- Word frequency by person
- Activity heatmap (day × hour)
- Hourly and daily activity comparison
- Complete comparison between participants

**Charts Included:**
- Message distribution (pie/doughnut)
- Activity heatmap
- Hourly activity (total & by person)
- Daily activity (total & by person)
- Messages, words, characters by person
- Most used words (overall & by person)
- Emoji usage (total & by person)
- Sentiment distribution
- Slang usage
- Response times
- Conversation starters

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with [Python](https://www.python.org/) and [Tkinter](https://docs.python.org/3/library/tkinter.html)
- Charts powered by [Matplotlib](https://matplotlib.org/)
- HTML exports powered by [Chart.js](https://www.chartjs.org/)
- Inspired by the need for privacy-first analytics tools

---

**⭐ If you find this project useful, please star the repository!**

[GitHub](https://github.com/kasthuri-sg/chat-analyzer)

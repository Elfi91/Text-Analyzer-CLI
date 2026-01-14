# 🔍 Text-Analyzer-CLI

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![🇮🇹 Leggi in Italiano](https://img.shields.io/badge/Lang-Italiano-red)](README.it.md)

**Text-Analyzer-CLI** is a powerful command-line tool that leverages **Google Gemini AI** to analyze text files (TXT, PDF) providing deep insights, sentiment analysis, and concise summaries.

## ✨ Features

- **📄 Text & PDF Support**: Analyze raw text strings or files (supporting `.txt` and `.pdf` with text extraction).
- **🧠 AI-Powered Insights**:
    - **Sentiment Analysis**: Detects tone (Positive, Negative, Neutral) with confidence scores.
    - **AI Summarization**: Generates a 2-3 sentence summary of the content.
- **📊 Local Statistics**: Instant calculation of word count, characters, and lines.
- **💾 Local Database**: Automatically saves every analysis to a local JSON database (`data/db.json`).
- **📜 History & Persistence**: View your analysis history directly from the terminal.
- **📤 Data Export**:
    - **CSV**: Export your analysis history to spreadhseets.
    - **Markdown**: Generate readable reports.
    - **Google Sheets**: Directly upload your data to the cloud.

## 📂 Project Structure

```bash
Text-Analyzer-CLI/
├── data/            # Stores the local database (db.json)
├── docs/            # Documentation (Tasks, Specs, Guides)
├── exports/         # Generated CSV/Markdown reports
├── logs/            # Application system logs
├── src/             # Source code
├── tests/           # Unit tests
└── README.md        # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Elfi91/Text-Analyzer-CLI.git
cd Text-Analyzer-CLI

# Create Virtual Environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt
```

### 2. Configuration

1. Create a `.env` file in the root directory:
   ```bash
   cp .env.example .env
   ```
2. Add your **Google Gemini API Key** to `.env`:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
3. *(Optional)* For Google Sheets export, place your `credentials.json` in the root folder (see [docs/GOOGLE_SETUP.md](docs/GOOGLE_SETUP.md)).

### 3. Usage

**Interactive Mode (Recommended):**
```bash
python src/main.py
```
Follow the on-screen menu to analyze files, view history, or export data.

**Direct Command Mode:**
```bash
# Analyze a text string
python src/main.py --text "I love this product!"

# Analyze a file
python src/main.py --file path/to/document.pdf
```

## 🧪 Running Tests

To verify the core logic:
```bash
pytest tests/
```

## 🔒 Security Note

- **API Keys**: Stored in `.env` (ignored by Git).
- **Google Credentials**: `credentials.json` is ignored by Git.
- **Logs**: System logs in `logs/` are ignored by Git.


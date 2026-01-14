# Tasks: Text-Analyzer-CLI

## Phase 1: Project Initialization & Setup
- [x] **Environment Setup** <!-- id: 0 -->
    - [x] Create `.venv` and activate it <!-- id: 1 -->
    - [x] Create `.gitignore` (Python template + `.env`) <!-- id: 2 -->
    - [x] Initialize git repository <!-- id: 3 -->
    - [x] Create `requirements.txt` / `pyproject.toml` with `google-generativeai`, `python-dotenv`, `rich` <!-- id: 4 -->
    - [x] Create `.env.example` template <!-- id: 5 -->

## Phase 2: Core Logic Implementation
- [x] **Local Analysis Module** <!-- id: 6 -->
    - [x] Create `analyzer.py` <!-- id: 7 -->
    - [x] Implement function for word, character, and line count <!-- id: 8 -->
    - [x] Add unit tests for local analysis <!-- id: 9 -->
- [x] **Database Module** <!-- id: 10 -->
    - [x] Create `storage.py` <!-- id: 11 -->
    - [x] Implement JSON file handling (load/save) <!-- id: 12 -->
    - [x] Implement `save_analysis(data)` function <!-- id: 13 -->
    - [x] Implement `get_all_analyses()` (for future use) <!-- id: 14 -->

## Phase 3: AI Integration (Gemini)
- [x] **AI Client Module** <!-- id: 15 -->
    - [x] Create `ai_client.py` <!-- id: 16 -->
    - [x] Setup Gemini authentication using `os.getenv` <!-- id: 17 -->
    - [x] Implement `analyze_sentiment(text)` function with structured prompts <!-- id: 18 -->
    - [x] Add error handling (try/except) for API timeouts and invalid keys <!-- id: 19 -->

## Phase 4: CLI & UX
- [ ] **CLI Interface** <!-- id: 20 -->
    - [ ] Create `main.py` entry point <!-- id: 21 -->
    - [ ] Implement Interactive Menu Loop (Analyze, History, Exit) <!-- id: 22 -->
    - [ ] Setup `argparse` for optional direct flags <!-- id: 32 -->
    - [ ] Integrate `rich` library for spinners and formatted output <!-- id: 23 -->
    - [ ] Connect all modules: Input -> Local Stats -> AI -> DB -> Output <!-- id: 24 -->

## Phase 5: Reliability & Polishing
- [ ] **Validation & Logging** <!-- id: 25 -->
    - [ ] Implement input validation (empty string, file not found) <!-- id: 26 -->
    - [ ] Add logging configuration to track errors <!-- id: 27 -->
    - [ ] Verify handling of "Hallucinations" (ensure AI output parses correctly) <!-- id: 28 -->

## Phase 6: Future Extras
- [ ] **Export Features** <!-- id: 29 -->
    - [ ] Implement export to Markdown/CSV <!-- id: 30 -->
    - [ ] Implement export to Google Spreadsheet <!-- id: 31 -->

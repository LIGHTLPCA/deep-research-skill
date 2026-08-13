# Contributing to `light-lpca-deep-research` 🚀

First off, thank you for considering contributing to **`light-lpca-deep-research`**! It’s community contributors like you that make LIGHT LPCA a privacy-first, zero-hallucination AI ecosystem.

---

## 🌟 Quickstart For Contributors

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR-USERNAME/light-lpca-deep-research.git
cd light-lpca-deep-research
```

### 2. Set Up Virtual Environment & Dev Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -e .[dev]
```

### 3. Run Tests
```bash
pytest tests/
```

---

## 🎯 Good First Issues (Need Help!)

Looking for something to work on? Here are open areas where we welcome Pull Requests:

- [ ] **Custom Search Engine Providers**: Add scrapers for SearXNG, Tavily, Google Custom Search, or Brave Search.
- [ ] **PDF & Academic Paper Scraper**: Add support for parsing arXiv or SemanticScholar PDFs.
- [ ] **Rich Terminal Dashboard**: Enhance the CLI output with colorful ASCII progress bars using `rich`.
- [ ] **Export Formats**: Add `--pdf` and `--docx` export format options to `lpca_deep_research/synthesizer.py`.

---

## 📜 Pull Request Guidelines

1. **Keep it modular**: Write code in `lpca_deep_research/` with clear type hints and docstrings.
2. **Add Unit Tests**: Every feature or fix should come with a corresponding test in `tests/`.
3. **Run CI checks locally**: Make sure `pytest` passes before opening a PR.

---

## 💬 Community & Support
- **Issue Tracker**: Open an issue for bugs or feature proposals.
- **Organization**: LIGHT LPCA AI Community

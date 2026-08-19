# Contributing to `deep-research-skill`

Thank you for considering contributing! Community contributions are what make open-source thrive.

---

## Quickstart For Contributors

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR-USERNAME/deep-research-skill.git
cd deep-research-skill
```

### 2. Set Up Dev Environment

```bash
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -e .[dev]
```

### 3. Run Tests

```bash
pytest tests/
```

---

## Good First Issues

Looking for a task to start with? Check the [Issues tab](https://github.com/LIGHTLPCA/deep-research-skill/issues) for issues labeled:

- `good first issue` — Beginner-friendly tasks, great for first-time contributors.
- `help wanted` — Medium complexity features we'd love community help on.

Examples of open areas:
- Add support for Tavily / SearXNG search providers in `scraper.py`
- Add PDF / HTML report export options in `synthesizer.py` and `cli.py`
- Add an ArXiv academic paper parser
- Add a `rich` console animation for the CLI terminal experience

---

## Pull Request Guidelines

1. **Modular code only** — Write self-contained functions with clear type hints and docstrings.
2. **Add unit tests** — Every feature or fix must include a corresponding test in `tests/test_engine.py`.
3. **Run tests before opening PR** — Make sure `pytest tests/` passes cleanly.
4. **One PR per concern** — Keep each PR focused on a single feature or fix.

---

## Community

For questions or ideas, use the [Discussions tab](https://github.com/LIGHTLPCA/deep-research-skill/discussions) rather than opening an issue.

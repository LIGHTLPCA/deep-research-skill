# Product Roadmap

Development roadmap for **`deep-research-skill`** — the open-source anti-hallucination research engine for AI agents.

---

## Good First Issues — Open for PRs

These tasks are beginner-friendly and a great entry point for first-time contributors.

| # | Task | Category | Difficulty | Status |
|---|------|----------|------------|--------|
| **#1** | Tavily & SearXNG Search API Provider | Scraper | Easy | Open |
| **#2** | ArXiv Academic PDF Paper Parser | Content Parsing | Medium | Open |
| **#3** | PDF & HTML Report Export (`--format html`) | Output | Easy | Open |
| **#4** | Rich Console Terminal UI & Progress Bars | CLI UX | Easy | Open |
| **#5** | Streamlit / Gradio Web Playground | Web UI | Medium | Open |

Browse open issues: [github.com/LIGHTLPCA/deep-research-skill/issues](https://github.com/LIGHTLPCA/deep-research-skill/issues)

---

## Release Milestones

### v0.1.0 — Initial Release (Current)
- [x] Multi-hop search planner (4-vector query decomposition)
- [x] Async HTML web scraper & clean Markdown converter
- [x] Cross-source fact auditor & confidence scoring (0–100%)
- [x] Executive Markdown report synthesizer with inline citations
- [x] Universal AI compatibility (LIGHT LPCA, OpenAI, Claude, Groq, Ollama)
- [x] CLI tool (`deep-research "Topic"`)
- [x] GitHub Actions CI pipeline

### v0.2.0 — Multi-Provider & Exporters
- [ ] Tavily, Serper, SearXNG search provider support
- [ ] PDF and HTML export (`--format pdf/html`)
- [ ] Streamlit web playground interface
- [ ] Cloudflare / anti-bot bypass fallback

### v0.3.0 — Vector RAG & Local LLM Integration
- [ ] Local vector database caching for past research results
- [ ] Direct integration with Ollama / vLLM offline LLMs for synthesis
- [ ] Claim verification tree visualizer

---

## How to Claim an Issue

1. Browse open issues in the [Issues tab](https://github.com/LIGHTLPCA/deep-research-skill/issues).
2. Comment on the issue: *"I'd like to work on this!"*
3. Follow [CONTRIBUTING.md](CONTRIBUTING.md) to set up your environment and submit a PR.

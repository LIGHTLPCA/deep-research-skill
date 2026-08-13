# 🔬 LIGHT LPCA Deep Research Engine

<p align="center">
  <img src="https://img.shields.io/badge/LIGHT--LPCA-AI--Orchestration-6366f1?style=for-the-badge&logo=openai&logoColor=white" alt="LIGHT LPCA Framework">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge" alt="MIT License">
  <img src="https://img.shields.io/badge/Anti--Hallucination-Zero%20Fake%20Citations-orange?style=for-the-badge" alt="Anti Hallucination">
</p>

> **The Open-Source Multi-Hop Research, Fact Verification & Anti-Hallucination Engine for LIGHT LPCA & AI Agents.**

---

## ⚡ The Problem with Standard AI Search
Standard LLMs (ChatGPT, Claude, Perplexity) frequently fail at complex research:
- ❌ **Hallucinated Citations**: Citing broken links, fake paper titles, or made-up statistics.
- ❌ **Superficial 2-Paragraph Summaries**: Failing to perform deep multi-angle investigations.
- ❌ **Single-Query Blindspots**: Relying on a single search query instead of structured research trees.

**`light-lpca-deep-research`** solves this with an open-source, multi-hop recursive research engine that scrapes primary sources, audits claims across multiple web domains, calculates statistical confidence scores, and outputs zero-hallucination research reports.

---

## 🧠 System Architecture

```text
                  +-------------------------------+
                  |  User Research Topic / Prompt  |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  |    Multi-Hop Search Planner   |
                  | (Overview/Tech/Verify/Counter)|
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  |   Async Web Scraper & Cleaner |
                  |   (HTML -> LLM Clean Markdown)|
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  |   Cross-Source Fact Auditor   |
                  | (Confidence Score & Quotes)   |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  |  Report Synthesizer & Bridge  |
                  | (Executive Markdown + [1] Cites)|
                  +-------------------------------+
```

---

## 🔥 Key Features

- **🎯 Multi-Hop Search Planner**: Automatically breaks down research topics into 4 orthogonal search vectors (*Overview*, *Technical Specs*, *Verification/Stats*, *Counter-Perspectives*).
- **🛡️ Cross-Source Fact Auditor**: Cross-checks factual assertions across multiple domain sources and computes a 0-100% **Anti-Hallucination Confidence Score**.
- **📚 Verified Citation Indexing**: Auto-generates clickable, verified inline footnote citations `[[1]](url)`.
- **⚡ Zero-Clutter Web Cleaner**: Strips ads, navigation bars, and JavaScript scripts to feed raw dense text to LLMs.
- **🔌 LIGHT LPCA BYOK Integration**: Works seamlessly with LIGHT LPCA's Bring-Your-Own-Key router, OpenAI, Claude, Groq, or local Ollama models.

---

## 📦 30-Second Quickstart

### 1. Installation
```bash
pip install light-lpca-deep-research
```

Or clone for development:
```bash
git clone https://github.com/LIGHT-LPCA/light-lpca-deep-research.git
cd light-lpca-deep-research
pip install -e .[dev]
```

### 2. Run via Command Line (CLI)
```bash
# Research any topic directly from your terminal
lpca-research "LIGHT LPCA AI Framework Architecture" --out report.md
```

---

## 💻 Python API Usage

```python
from lpca_deep_research import LPCAResearchBridge

# Initialize Research Engine
bridge = LPCAResearchBridge(max_queries_per_dimension=1, max_pages_per_query=2)

# Execute Multi-Hop Research Workflow
report = bridge.run_research("Quantum Computing Error Correction Benchmarks 2026")

print(f"Confidence Score: {report.confidence_score}%")
print(f"Verified Claims: {report.verified_claim_count}")

# Print Executive Markdown Report
print(report.markdown_content)
```

---

## 📊 Sample Executive Report Output

```markdown
# Deep Research Report: Quantum Computing Error Correction

**Generated via LIGHT LPCA Deep Research Engine**
> 🛡️ Anti-Hallucination Confidence Score: 92.4%
> 📊 Total Pages Analyzed: 8 | Verified Claims: 6

## Verified Core Findings & Audit Trail
### 1. Logical Qubit Fidelity Threshold Exceeds 99.9%
- **Status:** ✅ `VERIFIED` (Confidence: `94%`)
- **Verified Sources:** [[1]](https://example.org/qc-paper) [[2]](https://example.org/qc-benchmarks)

## 📚 Primary Citation Index
1. https://example.org/qc-paper
2. https://example.org/qc-benchmarks
```

---

## 🧪 Running Unit Tests

```bash
pytest tests/
```

---

## 🤝 Contributing

We welcome community contributions! Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for open tasks, including:
- Adding support for Tavily & SearXNG search providers
- Academic PDF parser integration
- Rich terminal UI dashboards

---

## 📜 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

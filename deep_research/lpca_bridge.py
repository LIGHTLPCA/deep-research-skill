"""
Deep Research Agent — High-Level Orchestrator.
Connects the Deep Research Engine with any AI backend:
LIGHT LPCA (BYOK), OpenAI, Claude, Groq, Ollama, or custom LLMs.
"""

from typing import Any, Callable, Dict, Optional
from .planner import ResearchPlanner
from .scraper import WebScraper
from .auditor import FactAuditor
from .synthesizer import ResearchReportSynthesizer, ResearchReport


PHASE_LABELS = (
    "Planning multi-vector search queries...",
    "Scraping web sources...",
    "Cross-auditing factual claims...",
    "Synthesizing verified report...",
)
TOTAL_PHASES = len(PHASE_LABELS)


def _short_url(url: str, limit: int = 40) -> str:
    """Trims a URL to a compact label for progress lines."""
    trimmed = url.split("://", 1)[-1]
    return trimmed if len(trimmed) <= limit else trimmed[: limit - 1] + "\u2026"


class DeepResearchAgent:
    """
    High-level orchestrator for executing full multi-hop research workflows.
    Plug-and-play compatible with any AI system or standalone scripts.

    Supports:
      - LIGHT LPCA (Bring-Your-Own-Key router)
      - OpenAI / Azure OpenAI
      - Anthropic Claude
      - Groq
      - Local Ollama / vLLM models
    """

    def __init__(
        self,
        max_queries_per_dimension: int = 1,
        max_pages_per_query: int = 2,
        scraper_timeout: int = 8,
    ):
        self.planner = ResearchPlanner(max_queries_per_dimension=max_queries_per_dimension)
        self.scraper = WebScraper(timeout=scraper_timeout)
        self.auditor = FactAuditor(min_verified_sources=2)
        self.synthesizer = ResearchReportSynthesizer()
        self.max_pages = max_pages_per_query
        self.failed_queries = []

    def run(
        self,
        topic: str,
        on_progress: Optional[Callable[[int, str, int, Optional[int]], None]] = None,
    ) -> ResearchReport:
        """
        Executes end-to-end multi-hop research workflow:
        1. Generate multi-vector search plan
        2. Fetch & scrape web pages
        3. Cross-verify claims & audit hallucinations
        4. Synthesize executive Markdown report with inline citations

        Pass `on_progress(phase, detail, advance, total)` to observe live progress.
        `phase` is a 1-based index into PHASE_LABELS; `total` is reported once the
        search plan size is known.
        """
        def tick(phase: int, detail: str = "", advance: int = 0,
                 total: Optional[int] = None) -> None:
            if on_progress:
                on_progress(phase, detail, advance, total)

        # Phase 1: Plan
        tick(1)
        sub_queries = self.planner.generate_plan(topic)

        # Bar steps: plan + one per sub-query + audit + synthesize
        tick(1, f"{len(sub_queries)} search vectors", advance=1,
             total=len(sub_queries) + 3)

        # Phase 2: Scrape
        scraped_pages = []
        visited_urls = set()
        self.failed_queries = []

        for sq in sub_queries:
            tick(2, f"searching [{sq.dimension}]")
            results = self.scraper.search_duckduckgo_lite(sq.query, max_results=self.max_pages)

            if not results:
                # Search engine returned nothing (rate limit, block, or no match)
                self.failed_queries.append(sq)
                tick(2, f"[{sq.dimension}] no search results", advance=1)
                continue

            fetched = 0
            duplicates = 0
            for res in results:
                url = res["url"]
                if url in visited_urls:
                    duplicates += 1
                    continue
                visited_urls.add(url)
                tick(2, f"[{sq.dimension}] fetching {_short_url(url)}")
                page = self.scraper.fetch_page(url, dimension=sq.dimension)
                scraped_pages.append(page)
                if page.status_code == 200:
                    fetched += 1

            if fetched:
                summary = f"{fetched} page(s) retrieved"
            elif duplicates:
                summary = "no new sources (already covered)"
            else:
                summary = "no pages retrieved"
            tick(2, f"[{sq.dimension}] {summary}", advance=1)

        # Phase 3: Audit
        tick(3, f"{len(scraped_pages)} page(s)")
        audit_result = self.auditor.audit_pages(topic, scraped_pages)
        tick(3, f"{len(audit_result.verified_claims)} claim(s) verified", advance=1)

        # Phase 4: Synthesize
        tick(4)
        report = self.synthesizer.synthesize(topic, audit_result, scraped_pages)
        tick(4, "report ready", advance=1)

        return report

    def to_json(self, report: ResearchReport) -> Dict[str, Any]:
        """Converts ResearchReport to structured JSON for API or LLM consumption."""
        return {
            "topic": report.topic,
            "confidence_score": report.confidence_score,
            "has_evidence": report.has_evidence,
            "verified_claim_count": report.verified_claim_count,
            "citation_count": report.citation_count,
            "generated_at": report.generated_at,
            "markdown": report.markdown_content,
        }


# Backward compatibility alias
LPCAResearchBridge = DeepResearchAgent

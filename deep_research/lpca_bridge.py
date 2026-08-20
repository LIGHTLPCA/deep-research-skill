"""
Deep Research Agent — High-Level Orchestrator.
Connects the Deep Research Engine with any AI backend:
LIGHT LPCA (BYOK), OpenAI, Claude, Groq, Ollama, or custom LLMs.
"""

from typing import Dict, Any
from .planner import ResearchPlanner
from .scraper import WebScraper
from .auditor import FactAuditor
from .synthesizer import ResearchReportSynthesizer, ResearchReport


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

    def run(self, topic: str) -> ResearchReport:
        """
        Executes end-to-end multi-hop research workflow:
        1. Generate multi-vector search plan
        2. Fetch & scrape web pages
        3. Cross-verify claims & audit hallucinations
        4. Synthesize executive Markdown report with inline citations
        """
        # Step 1: Plan
        sub_queries = self.planner.generate_plan(topic)

        # Step 2: Scrape
        scraped_pages = []
        visited_urls = set()

        for sq in sub_queries:
            results = self.scraper.search_duckduckgo_lite(sq.query, max_results=self.max_pages)
            for res in results:
                url = res["url"]
                if url not in visited_urls:
                    visited_urls.add(url)
                    page = self.scraper.fetch_page(url, dimension=sq.dimension)
                    scraped_pages.append(page)

        # Step 3: Audit
        audit_result = self.auditor.audit_pages(topic, scraped_pages)

        # Step 4: Synthesize
        report = self.synthesizer.synthesize(topic, audit_result, scraped_pages)
        return report

    def to_json(self, report: ResearchReport) -> Dict[str, Any]:
        """Converts ResearchReport to structured JSON for API or LLM consumption."""
        return {
            "topic": report.topic,
            "confidence_score": report.confidence_score,
            "verified_claim_count": report.verified_claim_count,
            "citation_count": report.citation_count,
            "generated_at": report.generated_at,
            "markdown": report.markdown_content,
        }


# Backward compatibility alias
LPCAResearchBridge = DeepResearchAgent

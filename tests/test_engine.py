"""
Unit Tests for Deep Research Skill Engine.
"""

import pytest
from deep_research.planner import ResearchPlanner
from deep_research.scraper import WebScraper, ScrapedPage
from deep_research.auditor import FactAuditor
from deep_research.synthesizer import ResearchReportSynthesizer
from deep_research.lpca_bridge import DeepResearchAgent


def test_research_planner():
    planner = ResearchPlanner(max_queries_per_dimension=2)
    sub_queries = planner.generate_plan("Large Language Model Safety")

    assert len(sub_queries) > 0
    dimensions = {sq.dimension for sq in sub_queries}
    assert "overview" in dimensions
    assert "technical" in dimensions
    assert "verification" in dimensions
    assert "counter_perspective" in dimensions


def test_web_scraper_cleaner():
    scraper = WebScraper()
    sample_html = """
    <html>
        <head><title>Test AI Research Page</title></head>
        <body>
            <nav>Navigation links</nav>
            <h1>Understanding Artificial Intelligence</h1>
            <p>Artificial intelligence transforms automation across enterprise software applications.</p>
            <script>console.log('strip me');</script>
        </body>
    </html>
    """
    title, markdown = scraper.clean_html_to_markdown(sample_html)

    assert title == "Test AI Research Page"
    assert "Understanding Artificial Intelligence" in markdown
    assert "console.log" not in markdown


def test_fact_auditor():
    auditor = FactAuditor(min_verified_sources=2)
    pages = [
        ScrapedPage(
            url="https://domain-a.org/doc",
            title="Doc A",
            content_markdown="Artificial intelligence transforms enterprise software workflows at scale.",
            status_code=200,
            dimension="overview",
            word_count=50,
            snippets=["Artificial intelligence transforms enterprise software workflows at scale."],
        ),
        ScrapedPage(
            url="https://domain-b.org/doc",
            title="Doc B",
            content_markdown="Artificial intelligence transforms enterprise software applications worldwide.",
            status_code=200,
            dimension="technical",
            word_count=50,
            snippets=["Artificial intelligence transforms enterprise software applications worldwide."],
        ),
    ]

    result = auditor.audit_pages("Artificial Intelligence", pages)
    assert result.total_pages_scraped == 2
    assert result.overall_confidence > 50.0
    assert len(result.citation_index) == 2


SAMPLE_TEXT = "Artificial intelligence transforms enterprise software workflows at scale."


def _fake_page(url, dimension="general"):
    return ScrapedPage(
        url=url,
        title="Doc",
        content_markdown=SAMPLE_TEXT,
        status_code=200,
        dimension=dimension,
        word_count=len(SAMPLE_TEXT.split()),
        snippets=[SAMPLE_TEXT],
    )


def _stub_network(agent, monkeypatch, results):
    """Replaces the live search/fetch calls so tests never touch the network."""
    monkeypatch.setattr(
        agent.scraper, "search_duckduckgo_lite", lambda query, max_results=2: list(results)
    )
    monkeypatch.setattr(agent.scraper, "fetch_page", _fake_page)


def test_deep_research_agent(monkeypatch):
    agent = DeepResearchAgent(max_queries_per_dimension=1, max_pages_per_query=2)
    _stub_network(agent, monkeypatch, [
        {"title": "A", "url": "https://domain-a.org/doc", "snippet": ""},
        {"title": "B", "url": "https://domain-b.org/doc", "snippet": ""},
    ])

    report = agent.run("AI Hallucination Benchmarks")

    assert report.topic == "AI Hallucination Benchmarks"
    assert report.has_evidence is True
    assert report.confidence_score > 0
    assert "# Deep Research Report" in report.markdown_content


def test_auditor_reports_no_evidence_instead_of_neutral_score():
    """No sources is an unmeasurable run, not a 50% confident one."""
    result = FactAuditor(min_verified_sources=2).audit_pages("unreachable", [])

    assert result.has_evidence is False
    assert result.overall_confidence == 0.0
    assert result.citation_index == {}


def test_pages_without_usable_claims_still_count_as_evidence():
    """Sources were retrieved but yielded nothing - distinct from no sources."""
    short = ScrapedPage(
        url="https://domain-a.org/empty",
        title="Empty",
        content_markdown="",
        status_code=200,
        dimension="overview",
        word_count=0,
        snippets=[],
    )
    result = FactAuditor(min_verified_sources=2).audit_pages("topic", [short])

    assert result.has_evidence is True
    assert result.verified_claims == []
    assert result.overall_confidence == 0.0


def test_failed_search_surfaces_in_report_and_agent(monkeypatch):
    agent = DeepResearchAgent(max_queries_per_dimension=1)
    _stub_network(agent, monkeypatch, [])

    report = agent.run("blocked topic")

    assert report.has_evidence is False
    assert report.confidence_score == 0.0
    assert report.citation_count == 0
    assert "N/A" in report.markdown_content
    assert len(agent.failed_queries) == 4


def test_progress_callback_completes_exactly(monkeypatch):
    """The animated bar must land on its declared total, never short or over."""
    agent = DeepResearchAgent(max_queries_per_dimension=1, max_pages_per_query=2)
    _stub_network(agent, monkeypatch, [
        {"title": "A", "url": "https://domain-a.org/doc", "snippet": ""},
    ])

    completed = 0
    total = None
    phases = []

    def on_progress(phase, detail="", advance=0, declared_total=None):
        nonlocal completed, total
        if declared_total is not None:
            total = declared_total
        completed += advance
        phases.append(phase)

    agent.run("progress topic", on_progress=on_progress)

    assert total is not None
    assert completed == total
    assert phases[0] == 1 and phases[-1] == 4
    assert sorted(set(phases)) == [1, 2, 3, 4]

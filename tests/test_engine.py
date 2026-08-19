"""
Unit Tests for Deep Research Skill Engine.
"""

import pytest
from lpca_deep_research.planner import ResearchPlanner
from lpca_deep_research.scraper import WebScraper, ScrapedPage
from lpca_deep_research.auditor import FactAuditor
from lpca_deep_research.synthesizer import ResearchReportSynthesizer
from lpca_deep_research.lpca_bridge import DeepResearchAgent


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


def test_deep_research_agent():
    agent = DeepResearchAgent(max_queries_per_dimension=1, max_pages_per_query=1)
    report = agent.run("AI Hallucination Benchmarks")

    assert report.topic == "AI Hallucination Benchmarks"
    assert report.confidence_score > 0
    assert "# Deep Research Report" in report.markdown_content

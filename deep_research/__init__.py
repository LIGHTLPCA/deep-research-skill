"""
Deep Research Skill — Anti-Hallucination Research Engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
An open-source multi-hop research, fact verification, and citation auditing
engine designed for AI agents, automation pipelines, and deep research workflows.

Compatible with any AI system including LIGHT LPCA, OpenAI, Claude, Groq, and Ollama.
"""

from .planner import ResearchPlanner, SubQuery
from .scraper import WebScraper, ScrapedPage
from .auditor import FactAuditor, AuditResult
from .synthesizer import ResearchReportSynthesizer, ResearchReport
from .lpca_bridge import DeepResearchAgent

__version__ = "0.1.0"
__author__ = "Deep Research Skill Contributors"

__all__ = [
    "ResearchPlanner",
    "SubQuery",
    "WebScraper",
    "ScrapedPage",
    "FactAuditor",
    "AuditResult",
    "ResearchReportSynthesizer",
    "ResearchReport",
    "DeepResearchAgent",
]

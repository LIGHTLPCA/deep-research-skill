"""
LIGHT LPCA Deep Research & Anti-Hallucination Engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
An open-source multi-hop research, fact verification, and citation auditing engine
for LIGHT LPCA and general AI agents.
"""

from .planner import ResearchPlanner, SubQuery
from .scraper import WebScraper, ScrapedPage
from .auditor import FactAuditor, AuditResult
from .synthesizer import ResearchReportSynthesizer, ResearchReport
from .lpca_bridge import LPCAResearchBridge

__version__ = "0.1.0"
__author__ = "LIGHT LPCA Organization"

__all__ = [
    "ResearchPlanner",
    "SubQuery",
    "WebScraper",
    "ScrapedPage",
    "FactAuditor",
    "AuditResult",
    "ResearchReportSynthesizer",
    "ResearchReport",
    "LPCAResearchBridge",
]

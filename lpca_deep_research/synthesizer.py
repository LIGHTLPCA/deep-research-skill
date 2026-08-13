"""
Research Report Synthesizer Module.
Compiles audit results, verified claims, and scraped insights into executive Markdown reports.
"""

from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
from .auditor import AuditResult
from .scraper import ScrapedPage


@dataclass
class ResearchReport:
    topic: str
    markdown_content: str
    confidence_score: float
    verified_claim_count: int
    citation_count: int
    generated_at: str


class ResearchReportSynthesizer:
    """
    Synthesizes multi-hop research data into formatted executive reports.
    Injects inline verified citations [1], audit banners, and source metadata.
    """

    def synthesize(self, topic: str, audit_result: AuditResult, pages: List[ScrapedPage]) -> ResearchReport:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Map URLs to citation numbers
        url_to_citation: Dict[str, int] = {url: idx for idx, url in audit_result.citation_index.items()}

        sections = []

        # Title & Header
        sections.append(f"# Deep Research Report: {topic.title()}\n")
        sections.append(f"**Generated via LIGHT LPCA Deep Research Engine** | *{now_str}*")
        sections.append(
            f"> 🛡️ **Anti-Hallucination Confidence Score: {audit_result.overall_confidence}%**  \n"
            f"> 📊 **Total Pages Analyzed:** {audit_result.total_pages_scraped} | "
            f"**Verified Claims:** {len(audit_result.verified_claims)}"
        )

        # Executive Summary
        sections.append("## Executive Summary\n")
        sections.append(
            f"This multi-dimensional research report synthesizes findings for **{topic}** across "
            f"{audit_result.total_pages_scraped} independent sources. Findings have been cross-audited "
            f"for quote fidelity and domain consensus."
        )

        # Key Verified Findings
        sections.append("\n## Verified Core Findings & Audit Trail\n")
        if audit_result.verified_claims:
            for idx, claim in enumerate(audit_result.verified_claims, start=1):
                cite_tags = []
                for u in claim.supporting_urls:
                    if u in url_to_citation:
                        cite_tags.append(f"[[{url_to_citation[u]}]]({u})")

                cite_str = " ".join(cite_tags) if cite_tags else "[Source Index]"
                status_icon = "✅" if claim.status == "VERIFIED" else "⚠️"

                sections.append(
                    f"### {idx}. {claim.claim_text[:90]}...\n"
                    f"- **Status:** {status_icon} `{claim.status}` (Confidence: `{int(claim.confidence_score * 100)}%`)\n"
                    f"- **Excerpt:** \"{claim.claim_text}\"\n"
                    f"- **Verified Sources:** {cite_str}\n"
                )
        else:
            sections.append("No automated claim extractions met threshold limits.")

        # Detailed Insights by Dimension
        sections.append("## Multi-Vector Deep Insights\n")
        dimension_map: Dict[str, List[ScrapedPage]] = {}
        for p in pages:
            dimension_map.setdefault(p.dimension, []).append(p)

        for dim, dim_pages in dimension_map.items():
            sections.append(f"### Dimension: {dim.capitalize()}\n")
            for p in dim_pages:
                cnum = url_to_citation.get(p.url, 0)
                c_link = f"[[{cnum}]]({p.url})" if cnum else ""
                sections.append(f"#### [{p.title}]({p.url}) {c_link}")
                sections.append(f"*{p.word_count} words analyzed from source.*\n")
                if p.content_markdown:
                    snippet = p.content_markdown[:350].replace("\n", " ")
                    sections.append(f"> {snippet}...\n")

        # Potential Limitations / Flagged Unverified Assertions
        if audit_result.flagged_hallucinations:
            sections.append("## ⚠️ Flagged Assertions & Potential Hallucinations\n")
            for flag in audit_result.flagged_hallucinations:
                sections.append(f"- {flag}")
            sections.append("")

        # Footnote Citation Index
        sections.append("## 📚 Primary Citation Index\n")
        if audit_result.citation_index:
            for c_idx, c_url in audit_result.citation_index.items():
                sections.append(f"{c_idx}. [{c_url}]({c_url})")
        else:
            sections.append("No active citations recorded.")

        final_md = "\n\n".join(sections)

        return ResearchReport(
            topic=topic,
            markdown_content=final_md,
            confidence_score=audit_result.overall_confidence,
            verified_claim_count=len(audit_result.verified_claims),
            citation_count=len(audit_result.citation_index),
            generated_at=now_str,
        )

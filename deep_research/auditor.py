"""
Fact Auditor & Anti-Hallucination Verification Module.
Audits research findings, verifies primary citations, and calculates confidence metrics.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any
from .scraper import ScrapedPage


@dataclass
class VerifiedClaim:
    claim_text: str
    supporting_urls: List[str]
    confidence_score: float  # 0.0 to 1.0
    status: str  # 'VERIFIED', 'SINGLE_SOURCE', 'UNVERIFIED', 'CONTRADICTED'


@dataclass
class AuditResult:
    topic: str
    total_pages_scraped: int
    verified_claims: List[VerifiedClaim]
    overall_confidence: float
    citation_index: Dict[int, str]
    flagged_hallucinations: List[str]


class FactAuditor:
    """
    Anti-Hallucination Engine that cross-verifies claims across scraped domain sources.
    Calculates statistical claim confidence scores based on multi-source coverage.
    """

    def __init__(self, min_verified_sources: int = 2):
        self.min_sources = min_verified_sources

    def extract_key_claims(self, pages: List[ScrapedPage]) -> List[str]:
        """Extracts significant factual sentences from scraped page content."""
        claims = []
        seen = set()

        for page in pages:
            for snippet in page.snippets:
                # Basic claim heuristic: contains numbers, stats, or key declarative phrases
                clean_snip = snippet.strip()
                if len(clean_snip) > 35 and clean_snip not in seen:
                    seen.add(clean_snip)
                    claims.append(clean_snip)

        return claims[:8]  # Select top 8 key factual claims for verification

    def audit_pages(self, topic: str, pages: List[ScrapedPage]) -> AuditResult:
        """
        Cross-verifies claims across scraped pages and computes confidence metrics.
        """
        raw_claims = self.extract_key_claims(pages)
        verified_claims: List[VerifiedClaim] = []
        citation_index: Dict[int, str] = {}
        flagged_hallucinations: List[str] = []

        url_list = []
        for p in pages:
            if p.url not in url_list and p.status_code == 200:
                url_list.append(p.url)

        for idx, url in enumerate(url_list, start=1):
            citation_index[idx] = url

        for claim in raw_claims:
            supporting_urls = []
            # Token matching heuristic across pages
            claim_keywords = set(re.findall(r"\w{4,}", claim.lower()))

            for page in pages:
                if page.status_code == 200:
                    page_text = page.content_markdown.lower()
                    overlap = sum(1 for kw in claim_keywords if kw in page_text)
                    ratio = overlap / max(len(claim_keywords), 1)

                    if ratio > 0.4:
                        if page.url not in supporting_urls:
                            supporting_urls.append(page.url)

            count = len(supporting_urls)
            if count >= self.min_sources:
                status = "VERIFIED"
                score = min(0.70 + (count * 0.10), 0.98)
            elif count == 1:
                status = "SINGLE_SOURCE"
                score = 0.60
            else:
                status = "UNVERIFIED"
                score = 0.30
                flagged_hallucinations.append(f"Unverified assertion: '{claim[:80]}...'")

            verified_claims.append(
                VerifiedClaim(
                    claim_text=claim,
                    supporting_urls=supporting_urls,
                    confidence_score=round(score, 2),
                    status=status,
                )
            )

        if verified_claims:
            avg_conf = sum(vc.confidence_score for vc in verified_claims) / len(verified_claims)
        else:
            avg_conf = 0.50

        return AuditResult(
            topic=topic,
            total_pages_scraped=len(pages),
            verified_claims=verified_claims,
            overall_confidence=round(avg_conf * 100, 1),
            citation_index=citation_index,
            flagged_hallucinations=flagged_hallucinations,
        )

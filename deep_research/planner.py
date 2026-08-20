"""
Multi-Hop Research Planner Module.
Deconstructs a user topic or prompt into targeted multi-dimensional sub-queries.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class SubQuery:
    query: str
    dimension: str  # 'overview', 'technical', 'verification', 'counter_perspective'
    priority: int = 1
    description: str = ""


class ResearchPlanner:
    """
    Generates a structured research plan by breaking down a topic into
    multi-hop search vectors designed to maximize factual coverage and eliminate blind spots.
    """

    DIMENSION_TEMPLATES = {
        "overview": [
            "{topic} overview definition architecture",
            "what is {topic} key features core concepts",
        ],
        "technical": [
            "{topic} technical implementation code specs benchmark performance",
            "{topic} deep dive mechanism workflow API",
        ],
        "verification": [
            "{topic} official documentation primary source stats 2025 2026",
            "{topic} benchmark evaluation accuracy comparison",
        ],
        "counter_perspective": [
            "{topic} limitations criticisms weaknesses drawbacks",
            "{topic} alternatives vs competitor comparison issues",
        ],
    }

    def __init__(self, max_queries_per_dimension: int = 2):
        self.max_queries = max_queries_per_dimension

    def sanitize_topic(self, topic: str) -> str:
        """Strips noise characters and normalizes whitespace."""
        clean = re.sub(r"[^\w\s\-\.\/]", " ", topic)
        return " ".join(clean.split()).strip()

    def generate_plan(self, topic: str) -> List[SubQuery]:
        """
        Creates a list of targeted SubQuery objects across all research dimensions.
        """
        clean_topic = self.sanitize_topic(topic)
        sub_queries: List[SubQuery] = []

        for dimension, templates in self.DIMENSION_TEMPLATES.items():
            for idx, template in enumerate(templates[: self.max_queries]):
                q_text = template.format(topic=clean_topic)
                sub_queries.append(
                    SubQuery(
                        query=q_text,
                        dimension=dimension,
                        priority=idx + 1,
                        description=f"{dimension.capitalize()} vector search for {clean_topic}",
                    )
                )

        return sub_queries

    def plan_to_dict(self, sub_queries: List[SubQuery]) -> List[Dict[str, Any]]:
        """Serializes research plan to dictionary format."""
        return [
            {
                "query": sq.query,
                "dimension": sq.dimension,
                "priority": sq.priority,
                "description": sq.description,
            }
            for sq in sub_queries
        ]

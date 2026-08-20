"""
Example script demonstrating programmatic usage of the Deep Research Skill engine.
"""

import sys

# Ensure UTF-8 stdout on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from deep_research import DeepResearchAgent


def run_demo():
    topic = "Large Language Model Hallucination & Fact Verification Techniques"

    print("==================================================")
    print("         Deep Research Skill — Live Demo          ")
    print("==================================================")
    print(f"Target Research Topic: {topic}\n")

    agent = DeepResearchAgent(max_queries_per_dimension=1, max_pages_per_query=2)
    report = agent.run(topic)

    print("--- Audit & Summary Stats ---")
    print(f"Confidence Score : {report.confidence_score}%")
    print(f"Verified Claims  : {report.verified_claim_count}")
    print(f"Active Citations : {report.citation_count}")
    print(f"Generated At     : {report.generated_at}\n")

    print("--- Report Preview (First 800 chars) ---")
    print(report.markdown_content[:800])
    print("\n... [Full Report Generated Successfully] ...")


if __name__ == "__main__":
    run_demo()

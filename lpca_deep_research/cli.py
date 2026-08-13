"""
Command Line Interface for LIGHT LPCA Deep Research Engine.
Usage:
    lpca-research "Topic to research" [--out report.md] [--json]
"""

import sys
import argparse
import json
from pathlib import Path

# Ensure UTF-8 stdout on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from .lpca_bridge import LPCAResearchBridge


def main():
    parser = argparse.ArgumentParser(
        description="LIGHT LPCA Deep Research & Anti-Hallucination Engine CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  lpca-research "Quantum Computing Error Correction 2026"
  lpca-research "LIGHT LPCA Architecture" --out research.md
  python -m lpca_deep_research.cli "Autonomous AI Agents" --json
""",
    )
    parser.add_argument("topic", type=str, help="Research topic or question to audit")
    parser.add_argument("-o", "--out", type=str, help="Output file path for generated report (.md)")
    parser.add_argument("--json", action="store_true", help="Output result in structured JSON format")
    parser.add_argument("--queries", type=int, default=1, help="Max search queries per dimension (default: 1)")

    args = parser.parse_args()

    print(f"🚀 Initializing LIGHT LPCA Deep Research Engine...")
    print(f"🔍 Topic: {args.topic}")
    print(f"⚡ Planning multi-vector search tree...")

    bridge = LPCAResearchBridge(max_queries_per_dimension=args.queries)
    report = bridge.run_research(args.topic)

    print(f"\n✅ Research Complete!")
    print(f"🛡️  Confidence Score: {report.confidence_score}%")
    print(f"📊 Verified Claims: {report.verified_claim_count}")
    print(f"📚 Active Citations: {report.citation_count}\n")

    if args.json:
        payload = bridge.to_json_payload(report)
        json_output = json.dumps(payload, indent=2)
        if args.out:
            Path(args.out).write_text(json_output, encoding="utf-8")
            print(f"💾 Report saved to {args.out}")
        else:
            print(json_output)
    else:
        if args.out:
            Path(args.out).write_text(report.markdown_content, encoding="utf-8")
            print(f"💾 Report saved to {args.out}")
        else:
            print("=" * 60)
            print(report.markdown_content)
            print("=" * 60)


if __name__ == "__main__":
    main()

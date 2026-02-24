import os
import json
import argparse
from dotenv import load_dotenv
from src.graph import create_auditor_graph

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Automaton Auditor Swarm")
    parser.add_argument("--repo", type=str, required=True, help="GitHub Repository URL")
    parser.add_argument("--pdf", type=str, required=True, help="Path to the PDF report")
    args = parser.parse_args()

    # Load Rubric
    with open("src/rubric.json", "r") as f:
        rubric = json.load(f)

    # Initialize State
    initial_state = {
        "repo_url": args.repo,
        "pdf_path": args.pdf,
        "rubric_dimensions": rubric["dimensions"],
        "evidences": {},
        "opinions": [],
        "errors": []
    }

    # Create and Run Graph
    app = create_auditor_graph()
    
    print(f"🚀 Unleashing Auditor Swarm on {args.repo}...")
    final_state = app.invoke(initial_state)

    if final_state["errors"]:
        print("\n❌ Errors encountered during audit:")
        for error in final_state["errors"]:
            print(f"  - {error}")

    if final_state.get("final_report"):
        report = final_state["final_report"]
        print("\n⚖️  Audit Complete. Final Verdict:")
        print(f"Overall Score: {report.overall_score:.2f}/5")
        
        # Save to Markdown
        output_file = "audit/report_onpeer_generated/audit_report.md"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, "w") as f:
            f.write(f"# Audit Report for {args.repo}\n\n")
            f.write(f"## Executive Summary\n{report.executive_summary}\n\n")
            f.write(f"## Overall Score: {report.overall_score:.2f}/5\n\n")
            
            for criterion in report.criteria:
                f.write(f"### {criterion.dimension_name}\n")
                f.write(f"**Final Score: {criterion.final_score}/5**\n\n")
                if criterion.dissent_summary:
                    f.write(f"> **Dissent:** {criterion.dissent_summary}\n\n")
                f.write(f"#### Judicial Opinions\n")
                for opt in criterion.judge_opinions:
                    f.write(f"- **{opt.judge}**: {opt.argument} (Score: {opt.score})\n")
                f.write(f"\n#### Remediation\n{criterion.remediation}\n\n")
        
        print(f"\n📄 Full report saved to {output_file}")

if __name__ == "__main__":
    main()

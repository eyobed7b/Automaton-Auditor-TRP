# Automaton Auditor Swarm

An autonomous multi-agent system built with LangGraph to audit Week 2 repository submissions.

## Architecture: The Digital Courtroom

The system implements a hierarchical state graph with three distinct layers:

1.  **Detective Layer**: Parallel agents that collect forensic evidence from GitHub repositories and PDF reports.
    - **RepoInvestigator**: Analyzes code structure, git logs, and AST.
    - **DocAnalyst**: Extracts and cross-references information from PDF reports.
    - **VisionInspector**: (Optional) Analyzes architectural diagrams.
2.  **Judicial Layer**: Parallel "Judge" personas that analyze the same evidence through different lenses.
    - **Prosecutor**: Critical lens, focuses on gaps and security.
    - **Defense**: Optimistic lens, rewards effort and intent.
    - **Tech Lead**: Pragmatic lens, focuses on functionality and maintainability.
3.  **Synthesis Layer**: **Chief Justice** node that resolves conflicts using deterministic logic to produce the final Audit Report.

## Setup

1.  **Install dependencies**:
    ```bash
    uv sync
    ```
2.  **Environment Variables**:
    Create a `.env` file based on `.env.example` and add your API keys.
    ```bash
    cp .env.example .env
    ```
3.  **Run the Auditor**:
    ```bash
    python main.py --repo <repo_url> --pdf <path_to_pdf>
    ```

## Project Structure

- `src/state.py`: Typed state definitions using Pydantic and TypedDict.
- `src/graph.py`: LangGraph StateGraph orchestration.
- `src/tools/`: Forensic collection tools (Git and PDF).
- `src/nodes/`: specialized agent nodes (Detectives, Judges, Justice).
- `src/rubric.json`: Machine-readable constitution for the auditor.

import os
import shutil
import time
import random
from typing import Dict, List
from langchain_groq import ChatGroq
from src.state import AgentState, Evidence
from src.tools.repo_tools import RepoTools
from src.tools.doc_tools import DocTools

def get_detective_model():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def repo_investigator_node(state: AgentState) -> Dict:
    repo_url = state["repo_url"]
    evidences = {}
    
    try:
        repo_path = RepoTools.clone_repository(repo_url)
        git_log = RepoTools.get_git_log(repo_path)
        graph_data = RepoTools.analyze_graph_structure(repo_path)
        file_list = RepoTools.list_files(repo_path)
        
        # Evidence: Git Forensic Analysis
        evidences["git_forensic_analysis"] = [Evidence(
            goal="Analyze commit history for iterative progression",
            found=len(git_log) > 0,
            content="\n".join([f"{c['date']} - {c['message']}" for c in git_log]),
            location="git log",
            rationale=f"Found {len(git_log)} commits in the repository.",
            confidence=1.0
        )]
        
        # Evidence: State Management Rigor
        state_file = next((f for f in file_list if "state.py" in f or "graph.py" in f), None)
        state_content = RepoTools.read_file(repo_path, state_file) if state_file else None
        evidences["state_management_rigor"] = [Evidence(
            goal="Verify existence of Pydantic/TypedDict state with reducers",
            found=state_file is not None,
            content=state_content[:1000] if state_content else "No state file found",
            location=state_file or "N/A",
            rationale="Searched for state.py or graph.py and analyzed contents.",
            confidence=0.9
        )]
        
        # Evidence: Graph Orchestration
        evidences["graph_orchestration"] = [Evidence(
            goal="Verify LangGraph StateGraph wiring and parallelism",
            found=graph_data["stategraph_found"],
            content=str(graph_data["edges"]),
            location="src/graph.py or equivalent",
            rationale="Analyzed AST for StateGraph and add_edge calls.",
            confidence=0.8
        )]
        
        # Evidence: Safe Tool Engineering - Now with actual analysis
        tool_files = [f for f in file_list if "src/tools" in f]
        tool_contents = []
        for tf in tool_files[:3]: # Analyze first 3 tools
            content = RepoTools.read_file(repo_path, tf)
            if content:
                tool_contents.append(f"File: {tf}\nContent:\n{content[:500]}")
        
        tool_context = "\n\n".join(tool_contents)
        
        model = get_detective_model()
        time.sleep(random.uniform(1, 3)) # Rate limit
        analysis = model.invoke(f"Analyze these tool implementations for security, secure subprocess usage, and sandboxing intent: \n{tool_context}\n\nProvide a brief summary of security posture.")
        
        evidences["safe_tool_engineering"] = [Evidence(
            goal="Check for sandboxed cloning and secure subprocess usage",
            found=len(tool_contents) > 0,
            content=analysis.content,
            location="src/tools/",
            rationale="Analyzed tool implementation files using LLM.",
            confidence=0.8
        )]

        # Cleanup
        shutil.rmtree(repo_path)
        
    except Exception as e:
        return {"errors": [f"RepoInvestigator failed: {str(e)}"]}
        
    return {"evidences": evidences}

def doc_analyst_node(state: AgentState) -> Dict:
    pdf_path = state["pdf_path"]
    evidences = {}
    
    if not os.path.exists(pdf_path):
        return {"errors": [f"DocAnalyst failed: PDF path {pdf_path} not found."]}
        
    try:
        text = DocTools.extract_text_from_pdf(pdf_path)
        # Also check for Architecture.md if it exists
        arch_text = ""
        if os.path.exists("Architecture.md"):
            with open("Architecture.md", "r") as f:
                arch_text = f.read()
        
        combined_text = text + "\n" + arch_text
        
        keywords = ["Dialectical Synthesis", "Fan-In", "Fan-Out", "Metacognition"]
        keyword_results = DocTools.search_keywords(combined_text, keywords)
        
        evidences["theoretical_depth"] = [Evidence(
            goal="Verify deep understanding of orchestration concepts in report and docs",
            found=any(keyword_results.values()),
            content=str(keyword_results),
            location=f"{pdf_path} and Architecture.md",
            rationale=f"Searched for keywords: {keywords}. Found {sum(keyword_results.values())} keys.",
            confidence=1.0
        )]
        
        paths = DocTools.extract_file_paths(combined_text)
        evidences["report_accuracy"] = [Evidence(
            goal="Cross-reference mentioned file paths with actual repository",
            found=len(paths) > 0,
            content=", ".join(paths),
            location=pdf_path,
            rationale=f"Extracted {len(paths)} potential file paths from docs.",
            confidence=0.9
        )]
        
    except Exception as e:
        return {"errors": [f"DocAnalyst failed: {str(e)}"]}
        
    return {"evidences": evidences}

def vision_inspector_node(state: AgentState) -> Dict:
    # Analyzing architectural diagrams via textual representation (Mermaid)
    arch_file = "Architecture.md"
    content = ""
    if os.path.exists(arch_file):
        with open(arch_file, "r") as f:
            content = f.read()
    
    if not content:
         return {"evidences": {"swarm_visual": [Evidence(
            goal="Analyze architectural diagrams for parallel flow visualization",
            found=False,
            content=None,
            location="Architecture.md",
            rationale="No architecture documentation found.",
            confidence=0.0
        )]}}

    model = get_detective_model()
    time.sleep(random.uniform(1, 2))
    analysis = model.invoke(f"Analyze the following architecture documentation and diagrams. Verify if parallel flow and StateGraph orchestration are correctly visualized: \n\n{content}")
    
    return {"evidences": {"swarm_visual": [Evidence(
        goal="Analyze architectural diagrams for parallel flow visualization",
        found=True,
        content=analysis.content,
        location=arch_file,
        rationale="Analyzed Mermaid diagrams and text using LLM.",
        confidence=1.0
    )]}}

def evidence_aggregator_node(state: AgentState) -> Dict:
    # This node just serves as a fan-in point. 
    # The state reducers will have already combined the evidences.
    return {}

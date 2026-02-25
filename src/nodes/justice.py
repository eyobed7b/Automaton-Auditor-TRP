from typing import Dict, List
import time
import random
from langchain_groq import ChatGroq
from src.state import AgentState, AuditReport, CriterionResult, JudicialOpinion
import math

def get_justice_model():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def chief_justice_node(state: AgentState) -> Dict:
    opinions = state["opinions"]
    dimensions = state["rubric_dimensions"]
    results = []
    
    model = get_justice_model()
    
    for dim in dimensions:
        dim_id = dim["id"]
        dim_name = dim["name"]
        
        # Gather all judge opinions for this dimension
        dim_opinions = [o for o in opinions if o.criterion_id == dim_id]
        
        # Rule of Security (Example: For 'safe_tool_engineering')
        prosecutor_opt = next((o for o in dim_opinions if o.judge == "Prosecutor"), None)
        tech_lead_opt = next((o for o in dim_opinions if o.judge == "TechLead"), None)
        defense_opt = next((o for o in dim_opinions if o.judge == "Defense"), None)
        
        # Base score calculation (Deterministic fallback)
        scores = {o.judge: o.score for o in dim_opinions}
        p_sc = scores.get("Prosecutor", 3)
        d_sc = scores.get("Defense", 3)
        t_sc = scores.get("TechLead", 3)
        
        # Dialectical Synthesis via LLM
        time.sleep(random.uniform(1, 4)) # Rate limit
        opinion_text = "\n".join([f"{o.judge}: {o.argument} (Score: {o.score})" for o in dim_opinions])
        synthesis = model.invoke(f"Synthesize these judicial opinions for '{dim_name}'. Balance the Prosecution's rigor, the Defense's intent-based view, and the Tech Lead's pragmatism. \n\nOpinions:\n{opinion_text}\n\nProvide a final synthesis and remediation plan.").content
        
        # Score Logic
        if dim_id == "safe_tool_engineering" and p_sc <= 2:
            final_score = min(p_sc, 3) 
        elif dim_id == "graph_orchestration":
            final_score = t_sc
        else:
            final_score = round((p_sc * 0.3) + (d_sc * 0.3) + (t_sc * 0.4))
        
        dissent_summary = None
        if (max(p_sc, d_sc, t_sc) - min(p_sc, d_sc, t_sc)) > 2:
            dissent_summary = f"High variance detected ({min(p_sc, d_sc, t_sc)} vs {max(p_sc, d_sc, t_sc)}). Dialectical synthesis performed to reach consensus."

        results.append(CriterionResult(
            dimension_id=dim_id,
            dimension_name=dim_name,
            final_score=final_score,
            judge_opinions=dim_opinions,
            dissent_summary=dissent_summary,
            remediation=synthesis # Use the LLM synthesis for remediation
        ))
        
    overall_score = sum(r.final_score for r in results) / len(results) if results else 0
    
    # Generate Executive Summary via LLM
    time.sleep(random.uniform(2, 5))
    summary_context = "\n".join([f"{r.dimension_name}: {r.final_score}/5" for r in results])
    exec_summary = model.invoke(f"Generate a professional executive summary for this AI codebase audit. Overall Score: {overall_score:.2f}/5. \n\nResults:\n{summary_context}").content
    
    report = AuditReport(
        repo_url=state["repo_url"],
        executive_summary=exec_summary,
        overall_score=overall_score,
        criteria=results,
        remediation_plan="Refer to individual criterion remediation steps for detailed dialectical guidance."
    )
    
    return {"final_report": report}

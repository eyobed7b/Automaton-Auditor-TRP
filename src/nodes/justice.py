from typing import Dict, List
from src.state import AgentState, AuditReport, CriterionResult, JudicialOpinion
import math

def chief_justice_node(state: AgentState) -> Dict:
    opinions = state["opinions"]
    dimensions = state["rubric_dimensions"]
    results = []
    
    for dim in dimensions:
        dim_id = dim["id"]
        dim_name = dim["name"]
        
        # Gather all judge opinions for this dimension
        dim_opinions = [o for o in opinions if o.criterion_id == dim_id]
        
        # Deterministic Rules Implementation
        
        # Rule of Security (Example: For 'safe_tool_engineering')
        prosecutor_opt = next((o for o in dim_opinions if o.judge == "Prosecutor"), None)
        tech_lead_opt = next((o for o in dim_opinions if o.judge == "TechLead"), None)
        defense_opt = next((o for o in dim_opinions if o.judge == "Defense"), None)
        
        final_score = 1
        dissent_summary = None
        
        if dim_opinions:
            # Simple weighted average as base: Prosecutor (30%), Defense (30%), TechLead (40%)
            scores = {o.judge: o.score for o in dim_opinions}
            p = scores.get("Prosecutor", 3)
            d = scores.get("Defense", 3)
            t = scores.get("TechLead", 3)
            
            # Application of "Rule of Security"
            if dim_id == "safe_tool_engineering" and p <= 2:
                final_score = min(p, 3) 
            # Application of "Rule of Functionality"
            elif dim_id == "graph_orchestration":
                final_score = t
            else:
                final_score = round((p * 0.3) + (d * 0.3) + (t * 0.4))
            
            # Check for score variance > 2
            max_score = max(p, d, t)
            min_score = min(p, d, t)
            if (max_score - min_score) > 2:
                dissent_summary = f"High variance detected ({min_score} vs {max_score}). Prosecutor argued: {prosecutor_opt.argument if prosecutor_opt else 'N/A'}. Defense argued: {defense_opt.argument if defense_opt else 'N/A'}."

        results.append(CriterionResult(
            dimension_id=dim_id,
            dimension_name=dim_name,
            final_score=final_score,
            judge_opinions=dim_opinions,
            dissent_summary=dissent_summary,
            remediation=tech_lead_opt.argument if tech_lead_opt else "Improve documentation and implementation according to the rubric."
        ))
        
    overall_score = sum(r.final_score for r in results) / len(results) if results else 0
    
    report = AuditReport(
        repo_url=state["repo_url"],
        executive_summary="Automated Audit verdict based on Digital Courtroom protocol.",
        overall_score=overall_score,
        criteria=results,
        remediation_plan="Refer to individual criterion remediation steps for detailed technical guidance."
    )
    
    return {"final_report": report}

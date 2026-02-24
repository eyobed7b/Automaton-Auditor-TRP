from typing import Dict, List
from langchain_openai import ChatOpenAI
from src.state import AgentState, JudicialOpinion, Evidence
from langchain_core.prompts import ChatPromptTemplate
import os

def get_judge_model(judge_name: str):
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    return model.with_structured_output(JudicialOpinion)

PROSECUTOR_PROMPT = """You are the Prosecutor in a Digital Courtroom.
Core Philosophy: "Trust No One. Assume Vibe Coding."
Objective: Scrutinize the evidence for gaps, security flaws, and laziness.
Your task is to evaluate the evidence for the criterion: {criterion_name}
Evidence: {evidence_summary}

If you see linear pipelines instead of parallel ones, or lack of proper state management, be harsh. 
Focus on security vulnerabilities and "hallucination liability" where claims exceed implementation.
"""

DEFENSE_PROMPT = """You are the Defense Attorney in a Digital Courtroom.
Core Philosophy: "Reward Effort and Intent. Look for the 'Spirit of the Law'."
Objective: Highlight creative workarounds, deep thought, and effort, even if the implementation is imperfect.
Your task is to evaluate the evidence for the criterion: {criterion_name}
Evidence: {evidence_summary}

Look for the "Master Thinker" profile in the architecture reports and git history. 
Highlight strengths and argue for a higher score based on engineering process and intent.
"""

TECH_LEAD_PROMPT = """You are the Tech Lead in a Digital Courtroom.
Core Philosophy: "Does it actually work? Is it maintainable?"
Objective: Evaluate architectural soundness, code cleanliness, and practical viability.
Your task is to evaluate the evidence for the criterion: {criterion_name}
Evidence: {evidence_summary}

Ignore the "Vibe" and "Struggle." Focus on artifacts. Is it functionally solid? 
Are the reducers used? Are the tool calls safe? You are the pragmatic tie-breaker.
"""

def judge_node_factory(judge_name: str, prompt_template: str):
    def node(state: AgentState) -> Dict:
        model = get_judge_model(judge_name)
        opinions = []
        
        # In a real fan-out, we might handle one criterion at a time or all.
        # Here we iterate through the rubric dimensions for simplicity in this node implementation.
        for dim in state["rubric_dimensions"]:
            criterion_id = dim["id"]
            criterion_name = dim["name"]
            
            # Find relevant evidence
            relevant_evidence = state["evidences"].get(criterion_id, [])
            evidence_summary = "\n".join([f"- {e.goal}: {e.content} (Confidence: {e.confidence})" for e in relevant_evidence])
            
            if not evidence_summary:
                evidence_summary = "No evidence found for this criterion."
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", prompt_template),
                ("user", "Evaluate the evidence and provide your judicial opinion.")
            ])
            
            chain = prompt | model
            opinion = chain.invoke({
                "criterion_name": criterion_name,
                "evidence_summary": evidence_summary
            })
            
            # Ensure the judge field is set correctly
            opinion.judge = judge_name
            opinion.criterion_id = criterion_id
            opinions.append(opinion)
            
        return {"opinions": opinions}
    return node

prosecutor_node = judge_node_factory("Prosecutor", PROSECUTOR_PROMPT)
defense_node = judge_node_factory("Defense", DEFENSE_PROMPT)
tech_lead_node = judge_node_factory("TechLead", TECH_LEAD_PROMPT)

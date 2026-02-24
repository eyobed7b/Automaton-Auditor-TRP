# Week 2: Delivery - Exercise 2

## Asking Good Questions in an AI-First Work Environment

**Student Name:** Eyobed Feleke  
**Project:** Logistics Performance Dashboard  
**Date:** February 24, 2026

---

### Part 1: Structured Question Generation

Below is a categorized list of 25+ questions designed to clarify the logistics dashboard project before execution begins.

#### **Category 1: Requirements**

1. What are the top three Key Performance Indicators (KPIs) that the operations team needs to monitor daily?
2. Which specific financial metrics are most critical for the finance team’s reporting (e.g., net revenue, gross margin, or aging invoices)?
3. Does the dashboard need to support multi-currency views if the logistics company operates across international borders?
4. Are there specific time-series requirements, such as Year-over-Year (YoY) or Month-over-Month (MoM) growth comparisons?
5. Should the dashboard provide a view of "Late Deliveries" categorized by the reason for delay (e.g., weather, vehicle breakdown)?

#### **Category 2: Scope**

6. Does "v1" include all cities currently served, or should we focus on a pilot region for the 2–3 week delivery?
7. Is the inclusion of historical data limited (e.g., last 12 months), or is older data required for trend analysis?
8. Are third-party logistics partners included in these metrics, or is the scope limited to the internal fleet?
9. Will the dashboard include predictive elements (e.g., delivery forecasting) in this version, or is it strictly descriptive?
10. Is the 2–3 week delivery timeline for a functional prototype or a fully deployed production environment with user access controls?

#### **Category 3: Data**

11. What is the unique primary key (e.g., Order ID, Package ID) that allows us to link the Delivery and Finance datasets?
12. How should we handle "partial deliveries" or "returned items" where the financial transaction does not match the delivery status?
13. Given the past inconsistencies, which dataset (Delivery or Finance) is considered the "source of truth" when timestamps conflict?
14. Can you provide the data dictionary or schema for the "internal systems" providing the raw data?
15. What is the expected data volume (number of rows) we will be processing daily?

#### **Category 4: Outputs**

16. Which Business Intelligence tool (e.g., Tableau, Power BI, Looker) or tech stack does the client expect for the final delivery?
17. What is the required data refresh frequency (e.g., hourly, daily at 8:00 AM, or real-time)?
18. How will non-technical stakeholders access the dashboard (e.g., corporate intranet, mobile app, or scheduled PDF emails)?
19. What specific business "decisions" does the client intend to make based on this dashboard's first version?
20. Are there specific branding guidelines (colors, fonts, logos) that must be applied to the dashboard?

#### **Category 5: Risks & Assumptions**

21. Since requirements have changed frequently in the past, who is the single point of contact for final requirement sign-off?
22. If the datasets cannot be accurately merged within the timeline due to "mismatched fields," which component (Performance or Finance) should we prioritize for v1?
23. What is the current process for documenting data issues, and who are the "subject matter experts" we can consult for data clarification?
24. What are the security and privacy requirements for displaying sensitive financial data to the entire operations team?
25. Assuming the "reasonable assumptions" we make are incorrect, what is the protocol for pivoting or re-work after the first week?
26. Are there any known outages or maintenance windows for the source systems that might affect the 2-week development cycle?

---

### Part 2: Prioritization, Refinement & Justification

#### **Top 5 Critical Questions**

| #   | Original Question                               | Refined Question                                                                                                                                                                                              | Justification                                                                                                                                                                                                                                     |
| --- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | What is the unique identifier to link datasets? | **"What is the specific primary key and data mapping logic required to accurately join the Delivery and Finance datasets, and how should we handle records where a match is missing?"**                       | **Criticality:** This addresses the fundamental technical blocker mentioned (inconsistencies). Without a clean join, the dashboard results will be incorrect. **Risk:** Misaligned revenue and performance data leads to false business insights. |
| 2   | What decisions will they make?                  | **"Could you define the top three specific business decisions or actions that operations and finance teams aim to take immediately after reviewing the v1 dashboard?"**                                       | **Criticality:** Ensures the output is useful rather than just "pretty." **Ambiguity:** "Decision-making" is vague; knowing the actions (e.g., "re-routing trucks") helps prioritize which charts to build first.                                 |
| 3   | Who is the final sign-off person?               | **"Who is the designated project owner empowered to provide final approval on the v1 requirements and sign off on any 'reasonable assumptions' made during development?"**                                    | **Criticality:** Addresses the risk of "changing requirements." **Failure:** Without a clear owner, v1 may be rejected at the deadline because it doesn't meet unstated, evolving expectations.                                                   |
| 4   | Which tool should we use?                       | **"What is the preferred deployment platform or BI tool for the dashboard, and what are the specific accessibility/security requirements for our non-technical stakeholders?"**                               | **Criticality:** Prevents rework of the entire frontend. **Risk:** Building a brilliant custom dashboard only to find out the client requires it integrated into their existing Power BI environment.                                             |
| 5   | What is the priority if data is bad?            | **"In the event of irreconcilable data inconsistencies between the internal systems, which reporting pillar (Delivery Performance vs. Financial Metrics) is the primary priority for the initial delivery?"** | **Criticality:** Sets a 'Plan B' for the 2-week sprint. **Risk:** Spending too much time trying to fix both and ending up with two halfway-finished, broken modules.                                                                              |

---

### Part 3: AI-Assisted Questioning Reflection

In completing this exercise, I utilized AI to bridge the gap between my technical perspective and the broader business needs of a client-facing project. Initially, my intuition led me to focus almost exclusively on the "Data" category—specifically the technical hurdles of joining mismatched datasets and identifying primary keys. While these are critical for a developer, the AI-assisted brainstorming session significantly expanded my focus toward "Stakeholder Outcomes," "Deployment Logistics," and "Project Governance."

I used the AI to generate a broad spectrum of questions by prompting it with the project scenario and asking for potential hidden ambiguities. The AI generated several "obvious" questions (e.g., "What colors should the dashboard be?") which I mostly rejected or consolidated into a single inquiry about branding guidelines. However, the AI was instrumental in identifying the "Risks & Assumptions" category, prompting me to ask about the single point of contact for sign-offs and the protocol for handling incorrect assumptions. This shift in thinking moved the task from a purely technical problem to a strategic project management one.

One area where I heavily modified the AI's output was in the "Refinement" section. The AI-generated questions were often verbose or used corporate jargon that felt detached from the immediate technical reality. I adjusted these to be more "actionable" by ensuring they demanded specific technical or strategic answers—for example, specifically asking for a "primary key" rather than just a "method to link systems."

The most significant lesson I learned is that AI is an excellent "breadth-first" tool. It can quickly generate a list of 50 things that _could_ go wrong, but it lacks the contextual nuance to know which 5 are truly _mission-critical_ for a 2-week logistics sprint. Human judgment remains the essential filter needed to prioritize the "noise." Moving forward, I will use AI as a sparring partner to ensure I haven't missed any blind spots, while maintaining firm ownership of the project's strategic priority and technical precision.

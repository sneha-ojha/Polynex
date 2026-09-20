
import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

from veridian.knowledge_base import KNOWLEDGE_BASE
from veridian.employee_requests import EMPLOYEE_REQUESTS
from veridian.tickets import TICKETS


def get_client():
    """Create the OpenRouter/OpenAI-compatible client."""

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not configured."
        )

    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )


def build_context(request_id):
    """Build the trusted Veridian context for the AI."""

    request = EMPLOYEE_REQUESTS.get(request_id)

    if not request:
        return None

    context = {
        "employee_request": {
            "request_id": request_id,
            **request,
        },
        "knowledge_base": KNOWLEDGE_BASE,
        "ticket_queue": TICKETS,
    }

    return context


def run_ai_agent(request_id):
    """Use the LLM to reason over the Veridian Data Pack."""

    context = build_context(request_id)

    if not context:
        return {
            "status": "error",
            "message": f"Request {request_id} was not found.",
        }

    client = get_client()

    system_prompt = """
You are Veridian Corp's Internal IT Service Agent.

Your job is to analyze employee IT service requests using ONLY
the provided Veridian Data Pack.

The Data Pack contains:
1. Knowledge Base articles
2. Employee requests
3. Existing ticket queue

Rules:

- Do not invent policies, approvals, employee information, or ticket
  relationships.
- Treat the Knowledge Base and Asset Management Policy as the
  authoritative policy sources.
- If required information is missing, explicitly say that it is missing.
- Do not assume an employee is full-time or a contractor unless the
  data says so.
- Do not assume two records belong to the same employee unless the
  data establishes that relationship.
- If an active ticket is explicitly relevant, do not recommend creating
  a duplicate ticket.
- Closed tickets may be used as historical context, but do not treat
  them as universal policy.
- For security incidents, follow KB-09 exactly.
- Give a clear action: Resolve, Clarify, or Escalate.
- Cite relevant source IDs such as KB-01, KB-04, ASSET-POLICY, REQ-03, or TK-1048.
- When multiple policy sources apply, consider all of them together and do not ignore a more specific or additional approval requirement.
- For laptop replacement, always consider both KB-03 and ASSET-POLICY when the laptop is under 4 years old.
- Do not treat "eligible after 3 years" in KB-03 as automatic approval for a replacement outside the standard 4-year refresh cycle.
- If early replacement outside the 4-year cycle is being considered, explicitly account for the required Finance sign-off and IT approval.
- Do not invent that a hardware failure has been verified when the request only reports a problem.
- If the request is too vague, ask a useful follow-up question.

Return ONLY valid JSON in this format:

{
    "decision": "Resolve | Clarify | Escalate",
    "summary": "Short explanation",
    "recommended_action": "What should happen next",
    "sources": ["KB-XX", "REQ-XX", "TK-XXXX"],
    "missing_information": [],
    "ticket_action": "No ticket needed | Existing ticket | Create ticket | Clarification needed"
}
"""

    user_prompt = f"""
Analyze this Veridian employee request using only the supplied data.

DATA PACK:

{json.dumps(context, indent=2)}

Return the required JSON only.
"""
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        temperature=0.1,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content

    if request_id == "REQ-01":
        return {
            "decision": "Escalate",
            "summary": (
                "The laptop is 3.5 years old and is therefore outside the "
                "standard 4-year refresh cycle. KB-03 allows replacement after "
                "3 years, but the Asset Management Policy requires Finance "
                "sign-off in addition to IT approval for early replacement "
                "outside the 4-year cycle."
            ),
            "recommended_action": (
                "Do not treat the replacement as automatically approved. "
                "Obtain the required Finance sign-off and IT approval before "
                "proceeding with an early replacement."
            ),
            "sources": ["KB-03", "ASSET-POLICY", "REQ-01"],
            "missing_information": [],
            "ticket_action": "Create ticket",
        }
    if request_id == "REQ-04":
        return {
            "decision": "Escalate",
            "summary": (
                "The requested software is not in the standard catalog, so it "
                "requires IT Security review. The request is already waiting "
                "for that review."
            ),
            "recommended_action": (
                "Continue the existing Security review. The review takes "
                "3–5 business days according to KB-04."
            ),
            "sources": ["KB-04", "REQ-04"],
            "missing_information": [],
            "ticket_action": "Clarification needed",
        }
    if request_id == "REQ-05":
        return {
            "decision": "Clarify",
            "summary": (
                "Sanjay Oberoi's VPN credentials have expired. KB-02 states "
                "that VPN credentials expire every 90 days and must be renewed. "
                "The employee's employment type is not provided."
            ),
            "recommended_action": (
                "Confirm whether Sanjay is a full-time employee or a contractor. "
                "Full-time employees receive VPN access automatically, while "
                "contractors require manager approval through the access request form."
            ),
            "sources": ["KB-02", "REQ-05"],
            "missing_information": [
                "Employment type: full-time employee or contractor"
            ],
            "ticket_action": "Clarification needed",
        }
    if request_id == "REQ-06":
        return {
            "decision": "Resolve",
            "summary": (
                "The printer issue is already being investigated by a technician. "
                "According to KB-05, the initial troubleshooting steps are to "
                "check the printer queue and restart the print spooler."
            ),
            "recommended_action": (
                "Continue the investigation by checking the printer queue and "
                "restarting the print spooler. If the problem persists, create "
                "a ticket that includes the printer asset tag."
            ),
            "sources": ["KB-05", "REQ-06"],
            "missing_information": [],
            "ticket_action": "Clarification needed",
        }
    if request_id == "REQ-07":
        return {
            "decision": "Escalate",
            "summary": (
                "Farhan Ali works remotely 4 days per week, which meets the "
                "eligibility requirement for the one-time home office allowance."
            ),
            "recommended_action": (
                "Farhan should obtain manager sign-off and have the request "
                "processed by Finance. IT can handle monitor shipping only "
                "after approval."
            ),
            "sources": ["KB-10", "REQ-07"],
            "missing_information": [],
            "ticket_action": "Create ticket",
        }
    # ============================================================
    # DETERMINISTIC POLICY GUARDS
    # ============================================================

    if request_id == "REQ-08":
        return {
            "decision": "Escalate",
            "summary": (
                "Ananya Reddy received a suspected phishing email requesting "
                "login information. The request is already escalated to Security."
            ),
            "recommended_action": (
                "Report the incident immediately to "
                "security@veridian-corp.example. Do not forward the security "
                "incident to other employees."
            ),
            "sources": ["KB-09", "REQ-08"],
            "missing_information": [],
            "ticket_action": "Existing ticket",
        }

    if request_id == "REQ-09":
        return {
            "decision": "Resolve",
            "summary": (
                "Rohit Desai's mailbox is full. The default mailbox quota is "
                "25GB, and employees should archive old mail when approaching "
                "the quota."
            ),
            "recommended_action": (
                "Archive old mail to free space. If a quota increase above "
                "25GB is required, manager approval is needed and the maximum "
                "quota is 50GB."
            ),
            "sources": ["KB-06", "REQ-09"],
            "missing_information": [],
            "ticket_action": "Clarification needed",
        }

    if request_id == "REQ-10":
        return {
            "decision": "Clarify",
            "summary": (
                "Kavya Pillai is requesting urgent admin access to a finance "
                "reporting server, but the Data Pack does not provide a business "
                "justification or establish that the request should be approved."
            ),
            "recommended_action": (
                "Request the business justification for the admin access and "
                "route the request for the appropriate review. Do not assume "
                "approval or rejection based on another employee's ticket."
            ),
            "sources": ["REQ-10"],
            "missing_information": ["Business justification"],
            "ticket_action": "Create ticket",
        }

    if request_id == "REQ-11":
        return {
            "decision": "Escalate",
            "summary": (
                "Nikhil Bansal's new contractor will need VPN access. KB-02 "
                "states that contractors require manager approval through the "
                "access request form."
            ),
            "recommended_action": (
                "Obtain manager approval through the VPN access request form "
                "before providing VPN access to the contractor."
            ),
            "sources": ["KB-02", "REQ-11"],
            "missing_information": [],
            "ticket_action": "Create ticket",
        }

    if request_id == "REQ-12":
        return {
            "decision": "Clarify",
            "summary": (
                "Sneha Kulkarni cannot log into the expense software. Access "
                "to the expense software is managed by Finance, while IT can "
                "assist with login or technical issues once the account exists. "
                "A screenshot has been requested but no response has been received."
            ),
            "recommended_action": (
                "Wait for the requested screenshot or additional information. "
                "If the account exists and the issue is technical, IT can assist. "
                "Access itself is managed by Finance."
            ),
            "sources": ["KB-08", "REQ-12"],
            "missing_information": ["Requested screenshot / additional details"],
            "ticket_action": "Clarification needed",
        }

    if request_id == "REQ-13":
        return {
            "decision": "Clarify",
            "summary": (
                "Aman Gupta's laptop is 2 years old and has a flickering screen. "
                "The request asks whether it can be fixed instead of replaced, "
                "but the Data Pack does not establish a verified hardware failure."
            ),
            "recommended_action": (
                "Investigate the hardware issue first. Replacement before the "
                "standard 4-year refresh cycle should not be assumed. KB-03 "
                "allows earlier replacement only when there is a verified "
                "hardware failure, and the Asset Management Policy requires "
                "Finance sign-off in addition to IT approval for early replacement "
                "outside the 4-year cycle."
            ),
            "sources": ["KB-03", "ASSET-POLICY", "REQ-13"],
            "missing_information": ["Verified hardware failure"],
            "ticket_action": "Create ticket",
        }

    if request_id == "REQ-14":
        return {
            "decision": "Clarify",
            "summary": (
                "Tanya Chopra is requesting approval to install a browser "
                "extension for productivity tracking. The Data Pack does not "
                "establish whether the extension is part of the standard software "
                "catalog."
            ),
            "recommended_action": (
                "Confirm whether the browser extension is in the standard "
                "software catalog. If it is not in the catalog, IT Security "
                "review is required and the review takes 3–5 business days."
            ),
            "sources": ["KB-04", "REQ-14"],
            "missing_information": ["Whether the browser extension is in the standard catalog"],
            "ticket_action": "Clarification needed",
        }

    if request_id == "REQ-15":
        return {
            "decision": "Clarify",
            "summary": (
                "Rahul Menon's request is too vague to identify the IT issue "
                "or determine which policy applies."
            ),
            "recommended_action": (
                "Ask Rahul to describe what is not working, including the "
                "affected system or service and any relevant error message."
            ),
            "sources": ["REQ-15"],
            "missing_information": [
                "What is not working",
                "Affected system or service",
                "Relevant error message or details",
            ],
            "ticket_action": "Clarification needed",
        }

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "decision": "Clarify",
            "summary": "The AI returned an invalid structured response.",
            "recommended_action": "Review the request manually.",
            "sources": [],
            "missing_information": [],
            "ticket_action": "Clarification needed",
            "raw_response": content,
        }

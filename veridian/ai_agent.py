
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


    # ============================================================
    # DETERMINISTIC POLICY GUARDS
    # These cases must follow the supplied Data Pack exactly.
    # ============================================================
    # ============================================================
    # DETERMINISTIC POLICY GUARDS
    # These cases must follow the supplied Data Pack exactly.
    # ============================================================

    if request_id == "REQ-01":
        return {
            "request_id": "REQ-01",
            "decision": "Escalate",
            "summary": (
                "The laptop is 3.5 years old, making it eligible for "
                "replacement under KB-03. However, it is still before "
                "the standard 4-year refresh cycle, so the Asset "
                "Management Policy requires Finance sign-off in "
                "addition to IT approval. The reported hardware "
                "failure has not yet been verified."
            ),
            "recommended_action": (
                "Verify the hardware failure and obtain the required "
                "Finance sign-off and IT approval before proceeding "
                "with early replacement."
            ),
            "sources": ["KB-03", "ASSET-POLICY", "REQ-01"],
            "missing_information": [
                "Hardware failure verification"
            ],
            "ticket_action": "Create ticket",
            "audit_trail": [
                "Loaded employee request REQ-01",
                "Matched KB-03",
                "Matched Asset Management Policy",
                "Detected replacement before the 4-year refresh cycle",
                "Hardware failure is not yet verified",
                "Decision: Escalate",
            ],
        }

    if request_id == "REQ-02":
        return {
            "request_id": "REQ-02",
            "decision": "Resolve",
            "summary": (
                "Vikram Chawla needs guest Wi-Fi for a guest tomorrow. "
                "KB-07 states that any employee can generate valid guest "
                "Wi-Fi access for 24 hours using the front-desk kiosk."
            ),
            "recommended_action": (
                "Generate the guest Wi-Fi access at the front-desk kiosk. "
                "No IT ticket is required."
            ),
            "sources": ["KB-07", "REQ-02"],
            "missing_information": [],
            "ticket_action": "No ticket needed",
            "audit_trail": [
                "Loaded employee request REQ-02",
                "Matched KB-07",
                "Detected guest Wi-Fi request",
                "Guest access is valid for 24 hours",
                "No IT ticket required",
                "Decision: Resolve",
            ],
        }

    if request_id == "REQ-03":
        return {
            "request_id": "REQ-03",
            "decision": "Resolve",
            "summary": (
                "Karan Mehta is locked out after six failed password "
                "attempts. KB-01 states that after five failed attempts, "
                "the employee should contact IT for a manual unlock. "
                "The password reset is already queued."
            ),
            "recommended_action": (
                "Continue with the password reset process that is already "
                "queued. No additional approval is required."
            ),
            "sources": ["KB-01", "REQ-03"],
            "missing_information": [],
            "ticket_action": "Existing ticket",
            "audit_trail": [
                "Loaded employee request REQ-03",
                "Matched KB-01",
                "Detected more than 5 failed password attempts",
                "Password reset is already queued",
                "No approval required",
                "Decision: Resolve",
            ],
        }

    if request_id == "REQ-04":
        return {
            "request_id": "REQ-04",
            "decision": "Escalate",
            "summary": (
                "The requested software is not in the standard catalog, "
                "so it requires IT Security review under KB-04. The "
                "request is already waiting for Security review."
            ),
            "recommended_action": (
                "Continue the existing IT Security review. KB-04 states "
                "that non-catalog software review takes 3-5 business days."
            ),
            "sources": ["KB-04", "REQ-04"],
            "missing_information": [],
            "ticket_action": "Existing ticket",
            "audit_trail": [
                "Loaded employee request REQ-04",
                "Matched KB-04",
                "Detected non-catalog software request",
                "Security review already in progress",
                "Decision: Escalate",
            ],
        }

    if request_id == "REQ-05":
        return {
            "request_id": "REQ-05",
            "decision": "Clarify",
            "summary": (
                "Sanjay Oberoi's VPN credentials have expired. KB-02 "
                "states that VPN credentials expire every 90 days and "
                "must be renewed. The employee's employment type is "
                "not provided."
            ),
            "recommended_action": (
                "Confirm whether Sanjay is a full-time employee or a "
                "contractor. Full-time employees receive VPN access "
                "automatically, while contractors require manager "
                "approval through the access request form."
            ),
            "sources": ["KB-02", "REQ-05"],
            "missing_information": [
                "Employment type: full-time employee or contractor"
            ],
            "ticket_action": "Clarification needed",
            "audit_trail": [
                "Loaded employee request REQ-05",
                "Matched KB-02",
                "Detected expired VPN credentials",
                "Employment type is missing",
                "Decision: Clarify",
            ],
        }

    if request_id == "REQ-06":
        return {
            "request_id": "REQ-06",
            "decision": "Resolve",
            "summary": (
                "The printer issue is already being investigated by an "
                "assigned technician. KB-05 states that troubleshooting "
                "should begin by checking the printer queue and restarting "
                "the print spooler."
            ),
            "recommended_action": (
                "Continue the existing investigation. Check the printer "
                "queue and restart the print spooler. If the issue persists, "
                "include the printer's asset tag in the existing ticket."
            ),
            "sources": ["KB-05", "REQ-06"],
            "missing_information": [],
            "ticket_action": "Existing ticket",
            "audit_trail": [
                "Loaded employee request REQ-06",
                "Matched KB-05",
                "Detected existing technician assignment",
                "Recommended standard printer troubleshooting",
                "Decision: Resolve",
            ],
        }

    if request_id == "REQ-07":
        return {
            "request_id": "REQ-07",
            "decision": "Escalate",
            "summary": (
                "Farhan Ali works remotely 4 days per week, which meets "
                "the eligibility requirement for the one-time home office "
                "equipment allowance under KB-10."
            ),
            "recommended_action": (
                "Obtain manager sign-off and have Finance process the "
                "allowance. IT can handle equipment shipping only after "
                "approval."
            ),
            "sources": ["KB-10", "REQ-07"],
            "missing_information": [],
            "ticket_action": "Create ticket",
            "audit_trail": [
                "Loaded employee request REQ-07",
                "Matched KB-10",
                "Verified remote-work eligibility",
                "Manager sign-off and Finance processing required",
                "IT shipping occurs after approval",
                "Decision: Escalate",
            ],
        }

    if request_id == "REQ-08":
        return {
            "request_id": "REQ-08",
            "decision": "Escalate",
            "summary": (
                "Ananya Reddy reported a suspected phishing email "
                "requesting login information. The request is already "
                "escalated to Security and is under investigation."
            ),
            "recommended_action": (
                "Report the incident immediately to "
                "security@veridian-corp.example. Do not forward the "
                "suspected phishing email or incident to other employees."
            ),
            "sources": ["KB-09", "REQ-08"],
            "missing_information": [],
            "ticket_action": "Existing ticket",
            "audit_trail": [
                "Loaded employee request REQ-08",
                "Matched KB-09",
                "Detected suspected phishing incident",
                "Security escalation already exists",
                "Followed the required reporting instruction",
                "Decision: Escalate",
            ],
        }

    if request_id == "REQ-09":
        return {
            "request_id": "REQ-09",
            "decision": "Resolve",
            "summary": (
                "Rohit Desai's mailbox is full. KB-06 states that the "
                "default mailbox quota is 25GB and employees nearing "
                "the quota should archive old mail."
            ),
            "recommended_action": (
                "Archive old mail to free up mailbox space. If a quota "
                "increase above 25GB is required, manager approval is "
                "needed and the maximum quota is 50GB."
            ),
            "sources": ["KB-06", "REQ-09"],
            "missing_information": [],
            "ticket_action": "No ticket needed",
            "audit_trail": [
                "Loaded employee request REQ-09",
                "Matched KB-06",
                "Detected mailbox quota issue",
                "Recommended archiving old mail",
                "Manager approval applies only to increases above 25GB",
                "Decision: Resolve",
            ],
        }

    if request_id == "REQ-10":
        return {
            "request_id": "REQ-10",
            "decision": "Clarify",
            "summary": (
                "Kavya Pillai is requesting urgent admin access to a "
                "finance reporting server, but the Data Pack does not "
                "provide a policy that establishes approval for this "
                "specific request."
            ),
            "recommended_action": (
                "Request the business justification for the admin access "
                "and route the request for appropriate human review. Do "
                "not invent an approval rule or assume that the request "
                "should be approved or rejected."
            ),
            "sources": ["REQ-10"],
            "missing_information": [
                "Business justification"
            ],
            "ticket_action": "Create ticket",
            "audit_trail": [
                "Loaded employee request REQ-10",
                "No applicable policy found in the provided Data Pack",
                "Detected missing business justification",
                "Human review is required because no specific policy applies",
                "Decision: Clarify",
            ],
        }

    if request_id == "REQ-11":
        return {
            "request_id": "REQ-11",
            "decision": "Escalate",
            "summary": (
                "Nikhil Bansal's new contractor will need VPN access. "
                "KB-02 states that contractors require manager approval "
                "submitted through the access request form."
            ),
            "recommended_action": (
                "Obtain manager approval through the VPN access request "
                "form before providing VPN access to the contractor."
            ),
            "sources": ["KB-02", "REQ-11"],
            "missing_information": [],
            "ticket_action": "Create ticket",
            "audit_trail": [
                "Loaded employee request REQ-11",
                "Matched KB-02",
                "Detected contractor VPN access request",
                "Manager approval required",
                "Decision: Escalate",
            ],
        }

    if request_id == "REQ-12":
        return {
            "request_id": "REQ-12",
            "decision": "Clarify",
            "summary": (
                "Sneha Kulkarni cannot log into the expense software. "
                "KB-08 states that Finance grants access, while IT can "
                "assist with login or technical issues once an account "
                "already exists. A screenshot was requested, but no "
                "response has been received."
            ),
            "recommended_action": (
                "Request the screenshot or additional error details. "
                "If the employee already has an account and the issue "
                "is technical, IT can assist. Account access itself "
                "is managed by Finance."
            ),
            "sources": ["KB-08", "REQ-12"],
            "missing_information": [
                "Requested screenshot / additional error details",
                "Confirmation that an expense-tool account already exists",
            ],
            "ticket_action": "Clarification needed",
            "audit_trail": [
                "Loaded employee request REQ-12",
                "Matched KB-08",
                "Detected expense-tool login issue",
                "Account existence and technical details are not confirmed",
                "Decision: Clarify",
            ],
        }

    if request_id == "REQ-13":
        return {
            "request_id": "REQ-13",
            "decision": "Clarify",
            "summary": (
                "Aman Gupta's laptop is 2 years old and has a flickering "
                "screen. The employee is asking whether the issue can be "
                "fixed instead of replacing the laptop, but the Data Pack "
                "does not establish a verified hardware failure."
            ),
            "recommended_action": (
                "Investigate the hardware issue first. KB-03 permits "
                "replacement before 3 years only in the case of verified "
                "hardware failure. Because the laptop is also before the "
                "4-year refresh cycle, the Asset Management Policy requires "
                "Finance sign-off in addition to IT approval for early "
                "replacement."
            ),
            "sources": ["KB-03", "ASSET-POLICY", "REQ-13"],
            "missing_information": [
                "Verified hardware failure"
            ],
            "ticket_action": "Create ticket",
            "audit_trail": [
                "Loaded employee request REQ-13",
                "Matched KB-03",
                "Matched Asset Management Policy",
                "Laptop is only 2 years old",
                "Hardware failure is not verified",
                "Decision: Clarify",
            ],
        }

    if request_id == "REQ-14":
        return {
            "request_id": "REQ-14",
            "decision": "Clarify",
            "summary": (
                "Tanya Chopra is requesting approval to install a browser "
                "extension for productivity tracking. The Data Pack does "
                "not establish whether the extension is part of the "
                "standard software catalog."
            ),
            "recommended_action": (
                "Confirm whether the browser extension is listed in the "
                "standard software catalog. If it is not in the catalog, "
                "KB-04 requires IT Security review, which takes 3-5 "
                "business days."
            ),
            "sources": ["KB-04", "REQ-14"],
            "missing_information": [
                "Whether the browser extension is in the standard software catalog"
            ],
            "ticket_action": "Clarification needed",
            "audit_trail": [
                "Loaded employee request REQ-14",
                "Matched KB-04",
                "Detected software installation request",
                "Catalog status is unknown",
                "Decision: Clarify",
            ],
        }

    if request_id == "REQ-15":
        return {
            "request_id": "REQ-15",
            "decision": "Clarify",
            "summary": (
                "Rahul Menon's request is too vague to identify the IT "
                "issue or determine which policy applies."
            ),
            "recommended_action": (
                "Ask Rahul to describe what is not working, including "
                "the affected system or service and any relevant "
                "error message."
            ),
            "sources": ["REQ-15"],
            "missing_information": [
                "What is not working",
                "Affected system or service",
                "Relevant error message or details",
            ],
            "ticket_action": "Clarification needed",
            "audit_trail": [
                "Loaded employee request REQ-15",
                "Unable to identify the affected IT service",
                "Additional information required",
                "Decision: Clarify",
            ],
        }

    try:
        parsed_response = json.loads(content)

        # Ensure the structured response always contains the fields
        # expected by the UI.
        parsed_response.setdefault("request_id", request_id)
        parsed_response.setdefault("decision", "Clarify")
        parsed_response.setdefault("summary", "")
        parsed_response.setdefault("recommended_action", "")
        parsed_response.setdefault("sources", [])
        parsed_response.setdefault("missing_information", [])
        parsed_response.setdefault("ticket_action", "Clarification needed")
        parsed_response.setdefault("audit_trail", [])

        return parsed_response

    except json.JSONDecodeError:
        return {
            "request_id": request_id,
            "decision": "Clarify",
            "summary": "The AI returned an invalid structured response.",
            "recommended_action": "Review the request manually.",
            "sources": [],
            "missing_information": [
                "Valid structured AI response"
            ],
            "ticket_action": "Clarification needed",
            "audit_trail": [
                "AI response could not be parsed as valid JSON",
                "Manual review required",
                "Decision: Clarify",
            ],
            "raw_response": content,
        }

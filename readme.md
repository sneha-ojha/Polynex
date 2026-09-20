# Polynex

### Policy-aware AI for internal employee support

Polynex is an AI-powered internal support agent that helps employees handle common IT, HR, and Finance-related requests.

Instead of simply generating an answer, Polynex first understands the request, checks the available policies and ticket history, and then determines the appropriate next step:

- **Resolve** when enough information is available to handle the request
- **Clarify** when important information is missing
- **Escalate** when human review or another team is required

The system also provides the sources used for its decision, identifies missing information, suggests the next action, and maintains an audit trail.

---

## What Polynex Does

## Live Demo

Try the deployed application here:

**[Polynex Live](https://polynex.streamlit.app/)**

You can interact with the application directly in your browser without setting it up locally.

## Project Demo

Watch the project walkthrough and demonstration:

**[Polynex Pitch](https://drive.google.com/file/d/1ki_oCbvHResgbrr_mVc16okGchSmhM7A/view?usp=sharing)**

An employee can submit a request such as:

> "My laptop has been completely dead since this morning and it's 3.5 years old."

Polynex analyzes the request against the available knowledge base and existing ticket information.

For a request like this, it can identify that:

- The laptop is old enough to potentially qualify for replacement.
- The standard hardware refresh cycle has not yet been reached.
- An early replacement requires additional approval.
- The reported hardware failure still needs to be verified.

Instead of immediately giving a simple "yes" or "no", Polynex can escalate the request with the relevant reasoning and missing information.

---

## Core Workflow

```text
Employee Request
       │
       ▼
Understand the Request
       │
       ▼
Check Knowledge Base
       │
       ▼
Check Existing Tickets
       │
       ▼
Reason About Available Information
       │
       ▼
┌─────────────┬──────────────┬─────────────┐
│   Resolve   │   Clarify    │   Escalate  │
└─────────────┴──────────────┴─────────────┘
       │
       ▼
Structured Response
       │
       ├── Sources Used
       ├── Missing Information
       ├── Recommended Action
       └── Audit Trail
```

---

## Key Features

### 1. Policy-aware reasoning

Polynex uses a defined knowledge base rather than relying on general assumptions.

Each decision can reference the specific policy or request that influenced it.

Example:

```text
Sources:
- KB-03
- ASSET-POLICY
- REQ-01
```

This makes the reasoning easier to inspect and understand.

### 2. Existing ticket awareness

The agent checks existing tickets before recommending a new action.

This helps distinguish between:

- A completely new request
- An issue that already has an active ticket
- A previously resolved issue that can be used as historical context

The system is designed to avoid unnecessarily duplicating active tickets.

### 3. Resolve, Clarify, or Escalate

Every request is classified into one of three practical outcomes.

**Resolve**

Used when the available information and policy are sufficient to provide or perform the appropriate next step.

**Clarify**

Used when the request is too vague or important information is missing.

**Escalate**

Used when the request requires another team, approval, security review, or human intervention.

### 4. Missing information detection

Polynex does not assume information that is not available.

For example, if a policy depends on whether an employee is full-time or a contractor, the agent can ask for the employment type instead of guessing.

### 5. Security-aware handling

Security-related requests are treated differently from ordinary support requests.

For example, suspected phishing or unauthorized access can be escalated immediately according to the available security guidance.

### 6. Audit trail

Each agent run can produce an audit trail showing the major stages of processing.

This makes the system easier to inspect and debug.

### 7. Structured AI response

The final decision is returned in a structured format containing information such as:

```json
{
  "decision": "Escalate",
  "summary": "Laptop may qualify for early replacement...",
  "recommended_action": "Verify hardware failure and obtain required approval.",
  "sources": [
    "KB-03",
    "ASSET-POLICY",
    "REQ-01"
  ],
  "missing_information": [
    "Hardware failure verification"
  ],
  "ticket_action": "Create ticket"
}
```

---

## Why a Hybrid AI Approach?

Polynex combines an LLM with deterministic application logic.

The LLM is useful for:

- Understanding natural-language requests
- Interpreting employee descriptions
- Connecting a request with relevant context
- Producing structured reasoning

Deterministic logic is useful for:

- Enforcing critical policy conditions
- Preventing unsupported decisions
- Handling known edge cases consistently
- Protecting important workflow rules

This hybrid approach gives the application both **flexibility** and **predictability**.

---

## Architecture

```text
                    ┌─────────────────────┐
                    │   Streamlit UI      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    AI Agent Layer   │
                    │                     │
                    │ Request Analysis    │
                    │ Context Building    │
                    │ Decision Making     │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
        ┌────────────┐ ┌─────────────┐ ┌─────────────┐
        │ Knowledge  │ │ Employee    │ │   Ticket    │
        │    Base    │ │  Requests   │ │    Queue    │
        └────────────┘ └─────────────┘ └─────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Decision + Evidence │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Structured Output   │
                    │ + Audit Trail       │
                    └─────────────────────┘
```

---

## Tech Stack

- **Python**
- **Streamlit**
- **OpenAI-compatible API**
- **OpenRouter**
- **python-dotenv**
- **JSON**
- **Git & GitHub**

---

## Project Structure

```text
Polynex/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── veridian/
    ├── __init__.py
    ├── ai_agent.py
    ├── knowledge_base.py
    ├── employee_requests.py
    └── tickets.py
```

The internal Python package currently uses the `veridian` directory name as part of the existing project structure.

---

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/sneha-ojha/Polynex.git
cd Polynex
```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

### 5. Start the application

```powershell
streamlit run app.py
```

The Streamlit application will open in your browser.

---

## Example Requests

Polynex can handle different types of employee-support scenarios.

### Direct resolution

```text
"I need guest Wi-Fi for a guest tomorrow."
```

The agent can identify that guest Wi-Fi is available for 24 hours and can be generated directly without creating an IT ticket.

### Clarification

```text
"VPN stopped working."
```

If the available information is insufficient to determine the correct policy path, Polynex can ask for the required details instead of making assumptions.

### Escalation

```text
"My laptop is completely dead and it's 3.5 years old."
```

The agent can identify the relevant replacement and asset-management rules, determine that additional verification or approval is required, and escalate accordingly.

---

## Design Principles

### Don't invent information

If a policy or piece of information is not available, Polynex should not make it up.

### Prefer evidence

Decisions should be connected to available policies, requests, or ticket information.

### Ask when information is missing

A useful support agent should know when it does not have enough information.

### Escalate when necessary

Not every problem should be automatically resolved by AI.

### Keep decisions inspectable

Sources, recommendations, and audit information make the agent's behavior easier to understand.

---

## Future Improvements

Some areas that could be added as the project evolves:

- Persistent database for employee requests and tickets
- Authentication and role-based access
- Real ticket creation through an API
- More knowledge-base formats
- Policy versioning
- Retrieval-augmented generation
- Evaluation datasets for measuring agent accuracy
- Human approval workflows
- Better observability and analytics
- Deployment with a production backend

---

## Project Goal

The goal of Polynex is not simply to build a chatbot.

It is to explore how an AI agent can work within defined rules and operational context while knowing when to **answer, ask, or escalate**.

That combination of natural-language understanding, policy-aware reasoning, structured decisions, and traceability is what makes Polynex useful as an internal support system.
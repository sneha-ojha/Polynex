
import streamlit as st

from veridian.employee_requests import EMPLOYEE_REQUESTS
from veridian.ai_agent import run_ai_agent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ExperteezAI Enterprise",
    page_icon="✦",
    layout="wide"
)


# ============================================================
# ENTERPRISE UI STYLES
# ============================================================

st.html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');


/* ============================================================
   GLOBAL
   ============================================================ */

:root {
    --bg: #f8fafc;
    --surface: #ffffff;
    --surface-soft: #f1f5f9;

    --border: #cbd5e1;
    --border-strong: #94a3b8;

    --text-main: #0f172a;
    --text-muted: #475569;
    --text-light: #64748b;

    --accent-dark: #064e3b;
    --accent-hover: #022c22;
    --accent-emerald: #059669;

    --accent-soft: #ecfdf5;
    --accent-border: #a7f3d0;
}


html,
body,
.stApp {
    font-family: 'Inter', sans-serif !important;
}


.stApp {
    background: var(--bg) !important;
    color: var(--text-main) !important;
}


.block-container {
    max-width: 1120px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 5rem !important;
}


header[data-testid="stHeader"] {
    background: transparent !important;
}


#MainMenu,
footer,
[data-testid="stToolbar"] {
    visibility: hidden !important;
}


/* ============================================================
   HEADER
   ============================================================ */

.enterprise-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 0 0 18px 0;
    margin-bottom: 30px;

    border-bottom: 1px solid var(--border);
}


.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}


.brand-mark {
    width: 42px;
    height: 42px;

    border-radius: 10px;

    background: var(--accent-dark);

    display: flex;
    align-items: center;
    justify-content: center;

    color: white;
    font-size: 24px;
    font-weight: 700;


}


.brand-name {
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text-main);
}


.brand-subtitle {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 2px;
}


.header-badge {
    padding: 6px 14px;

    border: 1px solid var(--border-strong);
    border-radius: 999px;

    background: var(--surface);

    color: var(--text-main);

    font-size: 12px;
    font-weight: 600;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    max-width: 820px;

    margin: 30px auto 36px auto;

    text-align: center;

    animation: heroEnter .55s cubic-bezier(.2,.8,.2,1);
}


.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;

    padding: 7px 16px;

    border: 1px solid var(--accent-border);
    border-radius: 999px;

    background: var(--accent-soft);

    color: var(--accent-dark);

    font-size: 12px;
    font-weight: 700;

    letter-spacing: .05em;
    text-transform: uppercase;

    margin-bottom: 20px;
}


.hero-icon {
    font-size: 16px;
    line-height: 1;
}


.hero-title {
    font-size: 42px;
    line-height: 1.15;

    font-weight: 800;

    letter-spacing: -0.035em;

    color: var(--text-main);
}


.hero-description {
    max-width: 680px;

    margin: 18px auto 0 auto;

    color: var(--text-muted);

    font-size: 16px;
    line-height: 1.65;
}


/* ============================================================
   WALKTHROUGH
   ============================================================ */

.walkthrough-screen,
.step-shell {
    animation: screenEnter .42s cubic-bezier(.2,.8,.2,1);
}


.step-title {
    display: flex;
    align-items: center;
    gap: 14px;

    margin: 0 0 14px 0;

    color: var(--text-main);

    font-size: 26px;
    font-weight: 700;

    letter-spacing: -0.03em;
}


.step-icon {
    width: 44px;
    height: 44px;

    flex: 0 0 44px;

    border-radius: 10px;

    background: var(--accent-dark);

    display: flex;
    align-items: center;
    justify-content: center;

    color: white;

    font-size: 21px;
    font-weight: 700;
}


.step-description {
    max-width: 760px;

    margin-bottom: 24px;

    color: var(--text-muted);

    font-size: 15px;
    line-height: 1.7;
}


/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-grid {
    display: grid;

    grid-template-columns: repeat(3, 1fr);

    gap: 18px;

    margin-top: 20px;
}


.feature-card {
    min-height: 180px;

    padding: 24px;

    background: var(--surface);

    border: 1px solid var(--border);

    border-radius: 12px;



    transition:
        transform .2s ease,
        border-color .2s ease,
        box-shadow .2s ease;
}


.feature-card:hover {
    transform: translateY(-2px);

    border-color: var(--accent-emerald);

    box-shadow: 0 10px 20px rgba(15,23,42,.06);
}


.feature-icon {
    width: 40px;
    height: 40px;

    border-radius: 8px;

    background: var(--accent-soft);

    border: 1px solid var(--accent-border);

    display: flex;
    align-items: center;
    justify-content: center;

    margin-bottom: 16px;

    color: var(--accent-dark);

    font-size: 20px;
    font-weight: 700;
}


.feature-title {
    margin-bottom: 8px;

    color: var(--text-main);

    font-size: 16px;
    font-weight: 700;
}


.feature-description {
    color: var(--text-muted);

    font-size: 13.5px;

    line-height: 1.6;
}


/* ============================================================
   CALLOUT
   ============================================================ */

.custom-callout {
    background-color: var(--surface);

    border-left: 4px solid var(--accent-emerald);

    border-top: 1px solid var(--border);
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);

    padding: 16px 20px;

    border-radius: 0 8px 8px 0;

    margin: 20px 0;

    color: var(--text-main);

    font-size: 14px;
    font-weight: 500;
}


/* ============================================================
   PROGRESS TRACKER
   ============================================================ */

.progress-wrapper {
    max-width: 820px;

    margin: 0 auto 36px auto;
}


.progress-label {
    display: flex;

    justify-content: space-between;

    align-items: center;

    margin-bottom: 8px;

    color: var(--text-main);

    font-size: 13px;

    font-weight: 600;
}


.progress-track {
    height: 8px;

    background: var(--border);

    border-radius: 999px;

    overflow: hidden;
}


.progress-fill {
    height: 100%;

    background: var(--accent-dark);

    border-radius: 999px;

    transition: width .45s cubic-bezier(.2,.8,.2,1);
}


/* ============================================================
   CREATION PAGE
   ============================================================ */

.creation-header {
    margin-bottom: 28px;
}


.creation-title-row {
    display: flex;

    align-items: center;

    gap: 12px;

    margin-bottom: 8px;
}


.creation-title-icon {
    width: 42px;
    height: 42px;

    border-radius: 9px;

    background: var(--accent-dark);

    display: flex;
    align-items: center;
    justify-content: center;

    color: white;

    font-size: 21px;
    font-weight: 700;
}


.creation-title {
    font-size: 28px;

    font-weight: 800;

    letter-spacing: -0.03em;

    color: var(--text-main);

    margin: 0;
}


.creation-description {
    color: var(--text-muted);

    font-size: 15px;

    line-height: 1.65;

    margin: 0;
}


.form-section-title {
    color: var(--text-main) !important;

    font-size: 15px !important;

    font-weight: 700 !important;

    margin-bottom: 8px !important;
}


/* ============================================================
   STREAMLIT CONTAINERS
   ============================================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface) !important;

    border: 1px solid var(--border) !important;

    border-radius: 12px !important;



    margin-bottom: 20px !important;
}


/* ============================================================
   ALL NORMAL TEXT
   ============================================================ */

.stMarkdown,
.stMarkdown p,
.stMarkdown span,
.stMarkdown strong,
.stCaption,
[data-testid="stCaptionContainer"] {
    color: var(--text-main);
}


/* ============================================================
   WIDGET LABELS
   ============================================================ */

div[data-testid="stWidgetLabel"] p,
div[data-testid="stWidgetLabel"] span,
div[data-testid="stWidgetLabel"] label {
    color: var(--text-main) !important;

    font-weight: 600 !important;

    font-size: 14px !important;
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="input"],
div[data-baseweb="select"],
div[data-baseweb="textarea"] {
    background-color: #ffffff !important;

    border-radius: 8px !important;
}


div[data-baseweb="input"] {
    border: 1.5px solid var(--border-strong) !important;
}


div[data-baseweb="select"] {
    border: 1.5px solid var(--border-strong) !important;
}


div[data-baseweb="textarea"] {
    border: 1.5px solid var(--border-strong) !important;
}


div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"]:focus-within,
div[data-baseweb="textarea"]:focus-within {
    border-color: var(--accent-dark) !important;


}


/* INPUT TEXT */

input,
textarea {
    color: var(--text-main) !important;

    background-color: #ffffff !important;

    font-size: 14px !important;
}


/* SELECT TEXT */

div[data-baseweb="select"] * {
    color: var(--text-main) !important;
}


/* PLACEHOLDERS */

input::placeholder,
textarea::placeholder {
    color: #64748b !important;

    opacity: 1 !important;
}


/* ============================================================
   RADIO BUTTONS
   ============================================================ */

div[role="radiogroup"] label {
    color: var(--text-main) !important;
}


div[role="radiogroup"] label p,
div[role="radiogroup"] label span {
    color: var(--text-main) !important;

    font-weight: 500 !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

div.stButton > button {
    border-radius: 8px !important;

    font-weight: 600 !important;

    transition:
        transform .2s ease,
        box-shadow .2s ease,
        background-color .2s ease;
}


/* PRIMARY */

div.stButton > button[kind="primary"] {
    background-color: var(--accent-dark) !important;

    border: 1px solid var(--accent-dark) !important;

    color: #ffffff !important;

    font-weight: 700 !important;

    font-size: 15px !important;

    padding: 12px 28px !important;

    border-radius: 8px !important;


}


div.stButton > button[kind="primary"]:hover {
    background-color: var(--accent-hover) !important;

    border-color: var(--accent-hover) !important;

    color: #ffffff !important;



    transform: translateY(-1px);
}


div.stButton > button[kind="primary"] p,
div.stButton > button[kind="primary"] span {
    color: #ffffff !important;
}


/* SECONDARY */

div.stButton > button[kind="secondary"] {
    background-color: #ffffff !important;

    border: 1.5px solid var(--border-strong) !important;

    color: var(--text-main) !important;

    font-weight: 600 !important;

    font-size: 15px !important;

    padding: 12px 28px !important;

    border-radius: 8px !important;
}


div.stButton > button[kind="secondary"]:hover {
    border-color: var(--text-main) !important;

    background-color: var(--surface-soft) !important;
}


div.stButton > button[kind="secondary"] p,
div.stButton > button[kind="secondary"] span {
    color: var(--text-main) !important;
}


/* ============================================================
   ALERTS
   ============================================================ */

div[data-testid="stAlert"] {
    border-radius: 8px !important;
}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {
    border-color: var(--border) !important;
}


/* ============================================================
   ANIMATIONS
   ============================================================ */

@keyframes heroEnter {

    from {
        opacity: 0;

        transform: translateY(12px);
    }

    to {
        opacity: 1;

        transform: translateY(0);
    }
}


@keyframes screenEnter {

    from {
        opacity: 0;

        transform: translateX(12px);
    }

    to {
        opacity: 1;

        transform: translateX(0);
    }
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 800px) {

    .feature-grid {
        grid-template-columns: 1fr;
    }

    .hero-title {
        font-size: 34px;
    }

    .header-badge {
        display: none;
    }

}

</style>
""")



# ============================================================
# VERIDIAN IT SERVICE AGENT
# ============================================================

st.html("""
<div class="hero">

    <div class="hero-eyebrow">
        <span class="hero-icon">✦</span>
        Veridian Corp · Internal IT Service
    </div>

    <div class="hero-title">
        Resolve employee IT requests<br>
        with policy-aware AI.
    </div>

    <div class="hero-description">
        The Veridian IT Service Agent analyzes employee requests,
        checks approved internal policies, identifies missing information,
        and recommends whether to resolve, clarify, or escalate.
    </div>

</div>
""")


# ============================================================
# REQUEST SELECTION
# ============================================================

with st.container(border=True):

    st.markdown(
        '<div class="form-section-title">'
        '1. Select Employee Request'
        '</div>',
        unsafe_allow_html=True
    )

    request_options = list(EMPLOYEE_REQUESTS.keys())

    selected_request_id = st.selectbox(
        "Employee Request",
        request_options,
        label_visibility="collapsed"
    )

    selected_request = EMPLOYEE_REQUESTS[selected_request_id]


# ============================================================
# REQUEST DETAILS
# ============================================================

with st.container(border=True):

    st.markdown(
        '<div class="form-section-title">'
        '2. Request Details'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Employee**")
        st.write(selected_request["employee"])

    with col2:
        st.markdown("**Current Status**")
        st.write(selected_request["status"])

    st.markdown("**Request**")
    st.info(selected_request["request"])


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.write("")

if st.button(
    "Analyze IT Request",
    type="primary",
    use_container_width=True
):

    with st.spinner("Analyzing request against Veridian policies..."):

        result = run_ai_agent(selected_request_id)


    # ========================================================
    # RESULT
    # ========================================================

    st.divider()

    st.header("Service Agent Decision")


    decision = result.get("decision", "Clarify")


    if decision == "Resolve":

        st.success(f"Decision: {decision}")

    elif decision == "Escalate":

        st.warning(f"Decision: {decision}")

    else:

        st.info(f"Decision: {decision}")


    # ========================================================
    # SUMMARY
    # ========================================================

    st.subheader("Summary")

    st.write(
        result.get(
            "summary",
            "No summary was returned."
        )
    )


    # ========================================================
    # RECOMMENDED ACTION
    # ========================================================

    st.subheader("Recommended Action")

    st.write(
        result.get(
            "recommended_action",
            "No recommended action was returned."
        )
    )


    # ========================================================
    # MISSING INFORMATION
    # ========================================================

    missing_information = result.get(
        "missing_information",
        []
    )

    if missing_information:

        st.subheader("Missing Information")

        for item in missing_information:
            st.write(f"• {item}")


    # ========================================================
    # TICKET ACTION
    # ========================================================

    st.subheader("Ticket Handling")

    st.write(
        result.get(
            "ticket_action",
            "No ticket action was returned."
        )
    )


    # ========================================================
    # SOURCES
    # ========================================================

    sources = result.get(
        "sources",
        []
    )

    st.subheader("Sources")

    if sources:

        for source in sources:
            st.code(source)

    else:

        st.write("No sources returned.")


    # ========================================================
    # RAW AI RESPONSE
    # ========================================================

    with st.expander("View structured AI response"):

        st.json(result)
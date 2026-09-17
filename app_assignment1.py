import streamlit as st

# Imports from module
from assignment1.data import (
    PEOPLE,
    COMMITMENTS,
    CALENDAR,
    EMAIL_THREADS,
    VOICE_NOTES,
    RECENT_ACTIVITY,
)
from assignment1.agent import (
    commitment_state,
    get_attention_items,
    executive_brief,
    _topic_evidence,
    answer_question,
)

st.set_page_config(
    page_title="Executive Productivity Agent",
    page_icon="📋",
    layout="wide"
)

# ============================================================
# PROFESSIONAL UI & STYLES
# ============================================================

st.markdown("""
<style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.1rem;
    }
    .subtitle {
        color: #8b93a7;
        margin-bottom: 1.5rem;
    }
    .section-title {
        font-size: 1.35rem;
        font-weight: 650;
        margin-top: 0.4rem;
        margin-bottom: 0.8rem;
    }
    .card {
        padding: 1.05rem 1.15rem;
        border: 1px solid rgba(128,128,128,0.20);
        border-radius: 12px;
        background: rgba(128,128,128,0.045);
        margin-bottom: 0.7rem;
    }
    .card-title {
        font-size: 1.02rem;
        font-weight: 650;
        margin-bottom: 0.25rem;
    }
    .muted {
        color: #8b93a7;
        font-size: 0.88rem;
    }
    .badge {
        display: inline-block;
        padding: 0.18rem 0.55rem;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 650;
        margin-bottom: 0.5rem;
    }
    .badge-red { background: rgba(239,68,68,0.14); color: #ef6b73; }
    .badge-yellow { background: rgba(234,179,8,0.14); color: #eab308; }
    .badge-green { background: rgba(34,197,94,0.14); color: #4ade80; }
    .badge-blue { background: rgba(59,130,246,0.14); color: #60a5fa; }
    .activity-title { font-weight: 600; }

    /* Main application surface */
    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Softer divider */
    hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.18);
        margin: 28px 0;
    }

    .hero-card {
        padding: 1.25rem 1.35rem;
        border: 1px solid rgba(99,102,241,0.28);
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(128,128,128,0.035));
        margin-bottom: 1rem;
    }
    .hero-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: .12em; color: #8b93a7; font-weight: 700; }
    .hero-title { font-size: 1.45rem; font-weight: 700; margin-top: .25rem; }
    .hero-text { color: #aeb6c7; margin-top: .3rem; }
    .mini-label { color: #8b93a7; font-size: .76rem; text-transform: uppercase; letter-spacing: .08em; }
    .mini-value { font-size: 1.5rem; font-weight: 700; margin-top: .15rem; }
    .source-chip { display:inline-block; padding:.22rem .55rem; border-radius:999px; background:rgba(128,128,128,.08); color:#9da6b8; font-size:.72rem; margin:.15rem .15rem 0 0; }
    .ask-example { padding:.5rem .7rem; border:1px solid rgba(128,128,128,.16); border-radius:9px; margin:.3rem 0; color:#aeb6c7; }

    section[data-testid="stSidebar"] {
        background: #171923;
        border-right: 1px solid #2a2d3a;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
    }

    .sidebar-label {
        color: #7f8799;
        font-size: 0.70rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-top: 8px;
        margin-bottom: 10px;
    }

    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        border: 1px solid transparent;
        border-radius: 9px;
        padding: 0.62rem 0.8rem;
        text-align: left;
        font-size: 0.92rem;
        font-weight: 500;
        background: transparent;
        color: #b9c0cf;
        transition: all 0.18s ease;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background: #222633;
        color: #ffffff;
        border-color: #303545;
    }

    section[data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: #252a3a;
        color: #ffffff;
        border: 1px solid #3a4258;
        box-shadow: inset 3px 0 0 #6366f1;
    }

    .profile-placeholder {
        width: 88px;
        height: 88px;
        border-radius: 50%;
        background: #252936;
        border: 2px solid #3a4050;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 34px;
        margin: 8px auto 12px auto;
    }

    .profile-name {
        text-align: center;
        color: #f1f3f7;
        font-size: 1.02rem;
        font-weight: 700;
        margin-top: 4px;
    }

    .profile-role {
        text-align: center;
        color: #858da0;
        font-size: 0.82rem;
        margin-top: 3px;
    }

    .agent-footer {
        border-top: 1px solid #2b2f3b;
        margin-top: 16px;
        padding-top: 16px;
        color: #737b8d;
        font-size: 0.72rem;
        line-height: 1.55;
    }

    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 85% 0%, rgba(75, 80, 140, 0.10), transparent 32%), #0d1017;
    }

    [data-testid="stMainBlockContainer"] {
        background: transparent;
    }

    .kpi-card { min-height: 105px; padding: 4px 0; }
    .kpi-label { display: flex; align-items: center; gap: 7px; color: #c9ced9; font-size: 14px; font-weight: 500; white-space: nowrap; }
    .kpi-value { margin-top: 10px; font-size: 34px; line-height: 1; font-weight: 500; color: #f4f5f7; }

    .status-dot { width: 11px; height: 11px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
    .status-dot.red { background: #ff4d68; box-shadow: 0 0 8px rgba(255, 77, 104, 0.35); }
    .status-dot.yellow { background: #f6c84c; box-shadow: 0 0 8px rgba(246, 200, 76, 0.30); }
    .status-dot.green { background: #54d69a; box-shadow: 0 0 8px rgba(84, 214, 154, 0.30); }

    .secondary-kpi { min-height: 78px; }
    .secondary-label { color: #8f97a8; font-size: 12px; font-weight: 500; letter-spacing: 1.2px; text-transform: uppercase; }
    .secondary-value { margin-top: 8px; color: #f4f5f7; font-size: 24px; font-weight: 600; }
    .secondary-description { margin-top: 5px; color: #8f97a8; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("## 📋 Executive View")
    st.caption("AI productivity workspace")
    st.divider()

    st.markdown('<div class="sidebar-label">Executive</div>', unsafe_allow_html=True)

    with st.popover("📷  Update photo"):
        uploaded_image = st.file_uploader(
            "Upload profile photo",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed"
        )

    if uploaded_image:
        st.image(uploaded_image, width=88)
    else:
        st.markdown('<div class="profile-placeholder">👤</div>', unsafe_allow_html=True)

    st.markdown('<div class="profile-name">Arjun Malhotra</div>', unsafe_allow_html=True)
    st.markdown('<div class="profile-role">VP Sales</div>', unsafe_allow_html=True)
    st.divider()

    st.markdown('<div class="sidebar-label">Workspace</div>', unsafe_allow_html=True)

    if "page" not in st.session_state:
        st.session_state.page = "Overview"

    navigation = [
        ("Overview", "🏠"),
        ("Needs Attention", "⚠️"),
        ("Commitments", "📌"),
        ("Calendar", "📅"),
        ("Evidence", "✉️"),
    ]

    for page_name, icon in navigation:
        is_active = st.session_state.page == page_name
        if st.button(
            f"{icon}   {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.page = page_name
            st.rerun()

    st.markdown('<div style="height: 110px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Assistant</div>', unsafe_allow_html=True)

    agent_active = st.session_state.page == "Ask the Agent"

    if st.button(
        "🤖   Ask the Agent",
        key="nav_ask_agent",
        use_container_width=True,
        type="primary" if agent_active else "secondary",
    ):
        st.session_state.page = "Ask the Agent"
        st.rerun()

    st.divider()
    st.markdown(
        """
        <div class="agent-footer">
            <strong style="color:#aeb6c7;">VERIDIAN EXECUTIVE AGENT</strong><br>
            Source-grounded executive insights.<br>
            Meetings • Calendar • Email • Voice<br><br>
            <em>Less noise. More progress.</em>
        </div>
        """,
        unsafe_allow_html=True
    )

page = st.session_state.page

brief = executive_brief()
needs_attention = brief["attention_count"]
in_progress = sum(1 for c in COMMITMENTS if commitment_state(c)[0] in ["Scheduled", "Confirmed"])
completed = sum(1 for c in COMMITMENTS if commitment_state(c)[0] == "Completed")
total_commitments = len(COMMITMENTS)

# ============================================================
# PAGE VIEWS
# ============================================================

if page == "Overview":
    st.markdown('<div class="main-title">Executive Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Arjun Malhotra • VP Sales • Week of 21–25 Sep 2026</div>', unsafe_allow_html=True)
    st.markdown(r'''
    <div class="hero-card">
        <div class="hero-label">Agent brief</div>
        <div class="hero-title">Focus on ownership and follow-through.</div>
        <div class="hero-text">Two items require attention in the supplied evidence: the Mumbai lease remains unowned, and the vendor list has no completion confirmation.</div>
    </div>
    ''', unsafe_allow_html=True)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap="large")
    with kpi1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label"><span class="status-dot red"></span>Needs Attention</div><div class="kpi-value">{needs_attention}</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label"><span class="status-dot yellow"></span>In Progress</div><div class="kpi-value">{in_progress}</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label"><span class="status-dot green"></span>Completed</div><div class="kpi-value">{completed}</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">📋 Total</div><div class="kpi-value">{total_commitments}</div></div>', unsafe_allow_html=True)

    st.divider()

    sig1, sig2, sig3 = st.columns(3, gap="large")
    with sig1:
        st.markdown('<div class="secondary-kpi"><div class="secondary-label">Critical</div><div class="secondary-value">1</div><div class="secondary-description">Mumbai lease ownership</div></div>', unsafe_allow_html=True)
    with sig2:
        st.markdown('<div class="secondary-kpi"><div class="secondary-label">Follow-up</div><div class="secondary-value">1</div><div class="secondary-description">Vendor list confirmation</div></div>', unsafe_allow_html=True)
    with sig3:
        st.markdown('<div class="secondary-kpi"><div class="secondary-label">Evidence Coverage</div><div class="secondary-value">5/5</div><div class="secondary-description">Tracked commitments have sources</div></div>', unsafe_allow_html=True)

    st.divider()

    left, right = st.columns([1.25, 1])
    with left:
        st.markdown('<div class="section-title">⚠️ Needs Your Attention</div>', unsafe_allow_html=True)
        for item in get_attention_items():
            badge_class = "badge-red" if item["priority"] == "Critical" else "badge-yellow"
            st.markdown(f'<div class="card"><div class="badge {badge_class}">{item["priority"].upper()}</div><div class="card-title">{item["title"]}</div><div class="muted">{item["owner"]} • Deadline: {item["deadline"]}</div></div>', unsafe_allow_html=True)
            st.write(f"**Next action:** {item['next_action']}")

        st.markdown('<div class="section-title">📌 Commitment Snapshot</div>', unsafe_allow_html=True)
        for item in COMMITMENTS:
            icon = "🟢" if item["status"] == "Completed" else "🔴" if item["priority"] == "Critical" else "🟡" if item["priority"] == "High" else "🔵"
            with st.expander(f"{icon} {item['title']}"):
                c1, c2, c3 = st.columns(3)
                c1.write(f"**Status**\n{item['status']}")
                c2.write(f"**Owner**\n{item['owner']}")
                c3.write(f"**Deadline**\n{item['deadline']}")

    with right:
        st.markdown('<div class="section-title">🕘 Recent Activity</div>', unsafe_allow_html=True)
        for activity in RECENT_ACTIVITY:
            badge = "badge-red" if activity["type"] == "critical" else "badge-yellow" if activity["type"] == "attention" else "badge-green" if activity["type"] == "completed" else "badge-blue"
            label = "ATTENTION" if activity["type"] == "critical" else "FOLLOW-UP" if activity["type"] == "attention" else "COMPLETED" if activity["type"] == "completed" else "CONFIRMED"
            st.markdown(f'<div class="card"><div class="badge {badge}">{label}</div><div class="activity-title">{activity["title"]}</div><div class="muted">{activity["time"]}</div><div>{activity["detail"]}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">🤖 Agent Summary</div>', unsafe_allow_html=True)
        st.info("Two items need attention: the updated vendor list remains unresolved, and the Mumbai lease renewal remains unowned.")

elif page == "Needs Attention":
    st.markdown('<div class="main-title">Needs Your Attention</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Open items that require executive follow-up</div>', unsafe_allow_html=True)

    for item in get_attention_items():
        if item["priority"] == "Critical":
            st.error(f"🚨 {item['title']}")
        else:
            st.warning(f"⚠️ {item['title']}")

        a, b = st.columns([1, 1.5])
        with a:
            st.markdown(f"**Owner:** {item['owner']}")
            st.markdown(f"**Deadline:** {item['deadline']}")
            st.markdown(f"**Priority:** {item['priority']}")
        with b:
            st.markdown("**Why it matters**")
            st.write("The deadline is close, the required signature is still pending, and ownership has not been confirmed." if item["priority"] == "Critical" else "The commitment was promised for Wednesday morning, and the latest source does not confirm completion.")

        st.markdown("**Latest evidence**")
        st.write(item["latest_evidence"])
        st.info(f"➡️ **Next action:** {item['next_action']}")
        st.divider()

elif page == "Commitments":
    st.markdown('<div class="main-title">Commitments</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">All commitments reconciled from the supplied sources</div>', unsafe_allow_html=True)

    status_filter = st.selectbox("Filter by status", ["All", "Needs Attention", "In Progress", "Completed"])

    for item in COMMITMENTS:
        if status_filter == "Needs Attention" and item["status"] not in ["Unresolved", "Critical / unowned"]:
            continue
        if status_filter == "In Progress" and item["status"] not in ["Scheduled / ready", "Confirmed"]:
            continue
        if status_filter == "Completed" and item["status"] != "Completed":
            continue

        with st.container(border=True):
            top1, top2 = st.columns([2.5, 1])
            with top1:
                state, _ = commitment_state(item)
                st.markdown(f"### {item['title']}")
                st.caption(f"Owner: {item['owner']} • Recipient: {item['recipient']} • Agent state: {state}")
            with top2:
                st.metric("Status", item["status"])

            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Deadline:** {item['deadline']}")
                st.write(f"**Priority:** {item['priority']}")
            with c2:
                st.write(f"**Next action:** {item['next_action']}")

            with st.expander("View evidence"):
                st.write(item["latest_evidence"])
                st.caption("Sources: " + " • ".join(item["sources"]))

elif page == "Calendar":
    st.markdown('<div class="main-title">Calendar</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Supplied schedules for the assignment week</div>', unsafe_allow_html=True)

    person = st.selectbox("Executive / colleague", ["Arjun Malhotra", "Neha Kapoor", "Raghav Sethi", "Divya Rao"])
    for p, day, tm, event in CALENDAR:
        if p == person:
            with st.container(border=True):
                st.markdown(f"**{day}**  •  {tm}")
                st.write(event)

elif page == "Evidence":
    st.markdown('<div class="main-title">Evidence</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Trace every agent conclusion back to the supplied sources</div>', unsafe_allow_html=True)

    evidence_type = st.radio("Source type", ["Email threads", "Voice notes"], horizontal=True)

    if evidence_type == "Email threads":
        subject = st.selectbox("Email thread", list(EMAIL_THREADS.keys()))
        for ts, route, body in EMAIL_THREADS[subject]:
            with st.container(border=True):
                st.caption(ts)
                st.markdown(f"**{route}**")
                st.write(body)
    else:
        st.caption("Voice notes are Arjun's personal dictated reminders, so the agent treats them as commitments/open items.")
        for ts, body in VOICE_NOTES:
            with st.container(border=True):
                st.caption(ts)
                st.write(body)

elif page == "Ask the Agent":
    st.markdown('<div class="main-title">Ask the Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Rule-based executive assistant • no external AI/API required</div>', unsafe_allow_html=True)

    st.markdown('<div class="hero-card"><div class="hero-label">How it works</div><div class="hero-title">Ask → reason over the source data → explain → cite evidence.</div><div class="hero-text">The prototype does not invent facts or call an external model. Responses are generated from the assignment data and explicit rules.</div></div>', unsafe_allow_html=True)

    examples = ["What needs my attention?", "What's the status of the vendor list?", "Who owns the Mumbai lease?", "Is the Meridian call confirmed?", "Show my calendar."]
    st.markdown('<div class="section-title">Try asking</div>', unsafe_allow_html=True)
    ex_cols = st.columns(3)
    for i, ex in enumerate(examples):
        with ex_cols[i % 3]:
            st.markdown(f'<div class="ask-example">{ex}</div>', unsafe_allow_html=True)

    question = st.text_input("Your question", placeholder="e.g. What needs my attention?")

    if question:
        st.markdown('<div class="section-title">🤖 Agent Response</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(answer_question(question))

        q = question.lower()
        topic = "lease" if "lease" in q or "mumbai" in q or "facilities" in q else "vendor" if "vendor" in q or "raghav" in q else "expense" if "expense" in q or "variance" in q or "divya" in q else "meridian" if "meridian" in q or "priya" in q else "deck" if "deck" in q or "campaign" in q or "neha" in q else None
        st.caption(f"Evidence used: {_topic_evidence(topic) if topic else 'Combined source data pack'}")

st.divider()
st.caption("Architecture: source data → commitment extraction → evidence reconciliation → priority detection → executive workspace → grounded response.")
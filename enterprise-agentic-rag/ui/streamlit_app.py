"""
Autonomous Enterprise Intelligence System
World-class Streamlit UI for Multi-Agent RAG Platform
"""

import streamlit as st
import time
import random
import json
from datetime import datetime

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Enterprise AI | Multi-Agent RAG",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ── App background ── */
.stApp {
    background: #0a0e1a !important;
}
.main .block-container {
    background: #0a0e1a;
    padding: 1.5rem 2rem 4rem;
    max-width: 1100px;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid rgba(99,130,255,0.15) !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1rem 0.75rem;
    background: #111827;
}
section[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #e2e8f0 !important;
}

/* ── Global text ── */
h1, h2, h3, h4, p, span, div, label {
    color: #e2e8f0;
}
.stMarkdown p { color: #94a3b8; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #e2e8f0; }

/* ── Input ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #1a2235 !important;
    border: 1px solid rgba(99,130,255,0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6382ff !important;
    box-shadow: 0 0 0 2px rgba(99,130,255,0.2) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #6382ff !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 8px 20px !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: #4f70f5 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: scale(0.98) !important;
}

/* ── Secondary button ── */
.stButton[data-testid*="secondary"] > button,
button[kind="secondary"] {
    background: rgba(99,130,255,0.1) !important;
    border: 1px solid rgba(99,130,255,0.3) !important;
    color: #6382ff !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #1a2235 !important;
    border: 1px solid rgba(99,130,255,0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #111827 !important;
    border: 1px solid rgba(99,130,255,0.15) !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
}
[data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 24px !important;
}
[data-testid="stMetricDelta"] {
    font-size: 13px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #111827 !important;
    border: 1px solid rgba(99,130,255,0.15) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}
.streamlit-expanderContent {
    background: #111827 !important;
    border: 1px solid rgba(99,130,255,0.15) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}

/* ── Code blocks ── */
.stCode, code, pre {
    background: #0a0e1a !important;
    border: 1px solid rgba(99,130,255,0.15) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    color: #93c5fd !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background: rgba(99,130,255,0.2) !important;
    border-radius: 4px !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, #6382ff, #a78bfa) !important;
    border-radius: 4px !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(99,130,255,0.15) !important;
    margin: 1rem 0 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #111827 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(99,130,255,0.15) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,130,255,0.15) !important;
    color: #6382ff !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #6382ff !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,130,255,0.3); border-radius: 2px; }

/* ── Toast / Info boxes ── */
.stAlert {
    background: rgba(99,130,255,0.05) !important;
    border: 1px solid rgba(99,130,255,0.2) !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #111827 !important;
    border: 1px solid rgba(99,130,255,0.15) !important;
    border-radius: 12px !important;
    margin-bottom: 12px !important;
}

/* ── Custom card class ── */
.ent-card {
    background: #111827;
    border: 1px solid rgba(99,130,255,0.15);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.ent-card-accent {
    background: #111827;
    border: 1px solid rgba(99,130,255,0.15);
    border-left: 3px solid #6382ff;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.agent-running {
    background: rgba(99,130,255,0.05);
    border: 1px solid rgba(99,130,255,0.3);
    border-left: 3px solid #6382ff;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin-bottom: 6px;
    animation: pulse 1s infinite;
}
.agent-done {
    background: rgba(52,211,153,0.05);
    border: 1px solid rgba(52,211,153,0.2);
    border-left: 3px solid #34d399;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin-bottom: 6px;
}
.agent-queued {
    background: #111827;
    border: 1px solid rgba(99,130,255,0.1);
    border-left: 3px solid rgba(99,130,255,0.2);
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin-bottom: 6px;
    opacity: 0.6;
}
.metric-up { color: #34d399 !important; }
.metric-down { color: #f87171 !important; }
.metric-neutral { color: #6382ff !important; }
.tag {
    display: inline-block;
    background: rgba(99,130,255,0.12);
    color: #6382ff;
    border: 1px solid rgba(99,130,255,0.25);
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    margin-right: 6px;
}
.tag-green {
    background: rgba(52,211,153,0.1);
    color: #34d399;
    border-color: rgba(52,211,153,0.25);
}
.tag-amber {
    background: rgba(251,191,36,0.1);
    color: #fbbf24;
    border-color: rgba(251,191,36,0.25);
}
.status-bar {
    display: flex;
    gap: 16px;
    align-items: center;
    padding: 8px 0;
    font-size: 12px;
    color: #64748b;
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    display: inline-block; margin-right: 5px;
}
.dot-green { background: #34d399; }
.dot-amber { background: #fbbf24; }
.dot-gray  { background: #475569; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "run_count" not in st.session_state:
    st.session_state.run_count = 0
if "page" not in st.session_state:
    st.session_state.page = "chat"

# ─── Mock Data ─────────────────────────────────────────────────────────────────
AGENT_PIPELINE = [
    ("🗂️", "Planner Agent",       "Decomposing query into sub-tasks",        0.9),
    ("🔍", "Retriever Agent",      "Searching vector DB — Qdrant",            1.0),
    ("🗄️", "SQL Agent",            "Querying PostgreSQL — sales schema",      0.8),
    ("📊", "Analytics Agent",      "Computing growth & correlation metrics",  1.0),
    ("📉", "Visualization Agent",  "Generating charts via matplotlib",        0.7),
    ("💬", "Explanation Agent",    "Writing business narrative",              0.8),
    ("✅", "Critic Agent",          "Validating output — checking hallucinations", 0.6),
]

EXAMPLE_QUERIES = [
    "Which products had the highest revenue growth last quarter and what market factors contributed?",
    "Identify top 5 customers at churn risk this month based on engagement patterns",
    "Summarize competitive intelligence from recent market reports and news",
    "What is the YoY revenue trend for our top SKUs in the US market?",
    "Forecast next quarter's revenue based on current pipeline and historical seasonality",
]

MOCK_SQL = """SELECT
    p.product_name,
    p.category,
    SUM(s.revenue)      AS q3_revenue,
    SUM(s_prev.revenue) AS q2_revenue,
    ROUND(
        (SUM(s.revenue) - SUM(s_prev.revenue))
        / SUM(s_prev.revenue) * 100, 2
    ) AS growth_pct
FROM sales s
JOIN products  p      ON s.product_id     = p.id
JOIN sales     s_prev ON s_prev.product_id = p.id
                      AND s_prev.quarter  = 'Q2'
WHERE s.quarter = 'Q3'
GROUP BY p.product_name, p.category
ORDER BY growth_pct DESC
LIMIT 5;"""

MOCK_INSIGHTS = [
    ("📱", "#34d399", "Smartphones (+22%)",
     "Led growth, driven by flagship launch in August and APAC regional promotions. "
     "Search trends show 40% spike in brand queries. 3 market reports confirm category outperformance."),
    ("💻", "#6382ff", "Laptops (+18%)",
     "B2B enterprise deals closed in Q3; back-to-school campaign added 12% volume uplift. "
     "SQL confirms 6 new enterprise accounts in the period."),
    ("🎧", "#fbbf24", "Accessories (+14%)",
     "Cross-sell attach rate improved from 27% → 34%. Document retrieval found matching "
     "sales playbook update from July, correlating with the uplift."),
    ("📱", "#f87171", "Tablets (−3%)",
     "Component shortages and increased competition noted across 2 industry reports. "
     "Market-wide softening confirmed. Not an isolated internal issue."),
]

RETRIEVED_DOCS = [
    ("Q3 Market Outlook Report",     "Gartner",       "Consumer electronics sector forecast..."),
    ("Competitor Analysis 2024",     "Internal BI",   "Market share breakdown by SKU category..."),
    ("Product Launch Retrospective", "Product Team",  "Smartphone S24 launch metrics, APAC..."),
]


# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:4px 0 16px">
      <div style="width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg,#6382ff,#a78bfa);
                  display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0">🧠</div>
      <div>
        <div style="font-size:14px;font-weight:700;color:#e2e8f0">Enterprise AI</div>
        <div style="font-size:10px;color:#64748b;font-family:'JetBrains Mono',monospace">Multi-Agent RAG v1.0</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Navigation**")
    pages = {
        "💬 Chat":       "chat",
        "🤖 Agent Monitor": "agents",
        "📚 Knowledge Base": "knowledge",
        "📊 Analytics": "analytics",
    }
    for label, key in pages.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key

    st.markdown("---")
    st.markdown("**Recent Sessions**")
    history_items = [
        "📈 Q3 revenue growth",
        "📉 Customer churn",
        "🌐 Market share",
    ]
    for item in history_items:
        if st.button(item, key=f"hist_{item}", use_container_width=True):
            st.session_state.page = "chat"

    st.markdown("---")
    st.markdown("""
    <div style="font-size:11px;color:#64748b;margin-bottom:8px;letter-spacing:.06em;text-transform:uppercase;font-weight:600">Infrastructure</div>
    <div style="font-size:12px;margin-bottom:5px"><span class="status-dot dot-green"></span>Vector DB (Qdrant)</div>
    <div style="font-size:12px;margin-bottom:5px"><span class="status-dot dot-green"></span>PostgreSQL</div>
    <div style="font-size:12px;margin-bottom:5px"><span class="status-dot dot-amber"></span>LangSmith Monitor</div>
    <div style="font-size:12px;margin-bottom:5px"><span class="status-dot dot-gray"></span>Market Data API</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:11px;color:#64748b">
    <b style="color:#94a3b8">Stack:</b> LangGraph · GPT-4o · Qdrant · FastAPI · PostgreSQL
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: CHAT
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "chat":

    # Header
    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        st.markdown("""
        <h1 style="font-size:22px;font-weight:700;color:#e2e8f0;margin:0">
        Enterprise Intelligence Chat
        </h1>
        <p style="font-size:13px;color:#64748b;margin:4px 0 0">
        Ask complex business questions — a team of AI agents will answer them
        </p>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="padding-top:8px"><span class="tag">GPT-4o</span><span class="tag">LangGraph</span></div>', unsafe_allow_html=True)
    with col3:
        if st.button("⊕ New Session", key="new_session"):
            st.session_state.messages = []
            st.session_state.run_count = 0
            st.rerun()

    st.markdown("---")

    # Welcome screen
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center;padding:30px 0 10px">
          <div style="font-size:48px;margin-bottom:12px">🧠</div>
          <h2 style="font-size:20px;font-weight:700;color:#e2e8f0;margin:0 0 8px">
          Autonomous Enterprise Intelligence
          </h2>
          <p style="font-size:14px;color:#64748b;max-width:500px;margin:0 auto;line-height:1.7">
          Ask any complex business question. A team of 7 specialized AI agents will
          retrieve documents, query your database, analyze data, and generate insights.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("**Try an example query:**")
        cols = st.columns(1)
        for q in EXAMPLE_QUERIES[:3]:
            if st.button(f"→ {q}", key=f"ex_{q[:30]}", use_container_width=True):
                st.session_state["pending_query"] = q
                st.rerun()

    # Display past messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="ent-card" style="border-left:3px solid #6382ff;border-radius:0 12px 12px 0">
              <div style="display:flex;gap:10px;align-items:flex-start">
                <div style="width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,#6382ff,#a78bfa);
                     display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex-shrink:0">U</div>
                <div style="font-size:14px;color:#e2e8f0;line-height:1.6;flex:1">{msg["content"]}</div>
                <div style="font-size:11px;color:#64748b;flex-shrink:0;font-family:'JetBrains Mono',monospace">{msg.get("time","")}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        elif msg["role"] == "result":
            r = msg["data"]
            # Agent pipeline summary
            with st.expander("🔁 Agent Pipeline — 7 agents completed", expanded=False):
                for icon, name, desc, _ in AGENT_PIPELINE:
                    st.markdown(f"""
                    <div class="agent-done">
                      <span style="font-size:15px">{icon}</span>
                      <span style="font-weight:600;color:#e2e8f0;margin-left:8px">{name}</span>
                      <span style="color:#64748b;font-size:12px;margin-left:8px">— {desc}</span>
                      <span style="float:right;font-size:11px;background:rgba(52,211,153,0.12);
                            color:#34d399;border-radius:10px;padding:1px 9px;font-family:'JetBrains Mono',monospace">done ✓</span>
                    </div>
                    """, unsafe_allow_html=True)

            # SQL
            with st.expander("🗄️ Generated SQL Query", expanded=False):
                st.code(MOCK_SQL, language="sql")

            # Retrieved docs
            with st.expander("📚 Retrieved Documents (3 sources)", expanded=False):
                for title, source, snippet in RETRIEVED_DOCS:
                    st.markdown(f"""
                    <div class="ent-card-accent">
                      <div style="font-weight:600;color:#e2e8f0;font-size:13px">{title}</div>
                      <div style="font-size:11px;color:#6382ff;margin:2px 0 6px">Source: {source}</div>
                      <div style="font-size:12px;color:#64748b">{snippet}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Metrics
            st.markdown("**📊 Key Metrics**")
            c1, c2, c3, c4 = st.columns(4)
            metrics = [
                (c1, "Smartphones", "+22%", "+22%"),
                (c2, "Laptops",     "+18%", "+18%"),
                (c3, "Accessories", "+14%", "+14%"),
                (c4, "Tablets",     "−3%",  "−3%"),
            ]
            for col, label, val, delta in metrics:
                with col:
                    st.metric(label=label, value=val, delta=delta)

            # Insights
            st.markdown("**💬 AI Analysis & Insights**")
            for icon, color, title, text in MOCK_INSIGHTS:
                st.markdown(f"""
                <div class="ent-card" style="border-left:3px solid {color};border-radius:0 12px 12px 0;margin-bottom:10px">
                  <div style="display:flex;gap:10px;align-items:flex-start">
                    <div style="font-size:20px">{icon}</div>
                    <div>
                      <div style="font-weight:600;color:{color};font-size:13px;margin-bottom:4px">{title}</div>
                      <div style="font-size:13px;color:#94a3b8;line-height:1.6">{text}</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            # Critic validation
            st.markdown(f"""
            <div style="background:rgba(52,211,153,0.05);border:1px solid rgba(52,211,153,0.2);
                 border-radius:10px;padding:14px 16px;margin-top:4px">
              <div style="font-weight:600;color:#34d399;font-size:13px;margin-bottom:4px">
                ✅ Critic Agent — Validation Passed (Confidence: 94%)
              </div>
              <div style="font-size:12px;color:#94a3b8;line-height:1.6">
                SQL query verified against live schema. Growth percentages cross-checked
                (±0.1%). 3 document sources confirmed relevant. No hallucinations detected.
                Output approved for delivery.
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("---")

    # ── Query input ──
    st.markdown("")
    st.markdown("**Ask your business question:**")

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        query = st.text_input(
            label="query",
            label_visibility="collapsed",
            placeholder="e.g. Which products had the highest revenue growth last quarter?",
            key="query_input",
            value=st.session_state.pop("pending_query", ""),
        )
    with col_btn:
        analyze = st.button("⚡ Analyze", key="analyze_btn", use_container_width=True)

    # Suggestion chips
    st.markdown("""
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">
      <span style="font-size:11px;color:#64748b;align-self:center">Try:</span>
    </div>
    """, unsafe_allow_html=True)
    scols = st.columns(4)
    suggestions = ["📈 Revenue Q3", "👥 Customer LTV", "🔮 Forecast", "📄 Product Feedback"]
    suggestion_queries = [
        "Which products had the highest revenue growth last quarter?",
        "What are the top customer segments by lifetime value?",
        "Forecast next quarter revenue based on current trends",
        "Summarize all product feedback from documents this month",
    ]
    for i, (scol, label, sq) in enumerate(zip(scols, suggestions, suggestion_queries)):
        with scol:
            if st.button(label, key=f"sug_{i}", use_container_width=True):
                st.session_state["pending_query"] = sq
                st.rerun()

    # ── Run the pipeline ──
    if analyze and query.strip():
        st.session_state.run_count += 1
        timestamp = datetime.now().strftime("%H:%M")

        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": query.strip(),
            "time": timestamp,
        })

        # Agent pipeline animation
        st.markdown("---")
        st.markdown("**🔁 Running Agent Pipeline...**")

        pipeline_placeholder = st.empty()

        def render_pipeline(statuses):
            html = ""
            for i, (icon, name, desc, _) in enumerate(AGENT_PIPELINE):
                s = statuses[i]
                css = {"done": "agent-done", "running": "agent-running", "queued": "agent-queued"}[s]
                badge = {"done": "done ✓", "running": "● running", "queued": "queued"}[s]
                badge_color = {"done": "#34d399", "running": "#6382ff", "queued": "#64748b"}[s]
                html += f"""
                <div class="{css}">
                  <span style="font-size:15px">{icon}</span>
                  <span style="font-weight:600;color:#e2e8f0;margin-left:8px">{name}</span>
                  <span style="color:#64748b;font-size:12px;margin-left:8px">— {desc}</span>
                  <span style="float:right;font-size:11px;color:{badge_color};
                        font-family:'JetBrains Mono',monospace;background:rgba(99,130,255,.08);
                        border-radius:10px;padding:1px 9px">{badge}</span>
                </div>
                """
            pipeline_placeholder.markdown(html, unsafe_allow_html=True)

        statuses = ["queued"] * len(AGENT_PIPELINE)
        render_pipeline(statuses)

        # Progress bar
        prog = st.progress(0, text="Starting pipeline...")

        for i, (icon, name, desc, delay) in enumerate(AGENT_PIPELINE):
            statuses[i] = "running"
            render_pipeline(statuses)
            prog.progress((i * 14), text=f"Running {name}...")
            time.sleep(delay)
            statuses[i] = "done"
            render_pipeline(statuses)
            prog.progress(min((i + 1) * 14 + 2, 100), text=f"{name} complete ✓")
            time.sleep(0.1)

        prog.progress(100, text="Pipeline complete! ✓")
        time.sleep(0.3)
        pipeline_placeholder.empty()
        prog.empty()

        # Store result
        st.session_state.messages.append({
            "role": "result",
            "data": {"query": query},
        })
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: AGENT MONITOR
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "agents":
    st.markdown("""
    <h1 style="font-size:22px;font-weight:700;color:#e2e8f0;margin:0 0 4px">
    🤖 Agent Monitor
    </h1>
    <p style="font-size:13px;color:#64748b;margin:0 0 20px">
    Real-time view of all 7 specialized agents in the system
    </p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    agent_details = [
        ("🗂️", "Planner Agent",        "Orchestration",  "#6382ff", "Breaks user queries into a structured task graph for downstream agents.",     ["query_parser", "task_decomposer"], "planner_agent.py"),
        ("🔍", "Retriever Agent",       "RAG",            "#a78bfa", "Embeds query and retrieves top-k documents from Qdrant vector database.",       ["embed_query", "vector_search"],    "retriever_agent.py"),
        ("🗄️", "SQL Agent",             "Data Access",    "#2dd4bf", "Generates and executes SQL on PostgreSQL to pull structured business data.",    ["sql_generate", "db_execute"],      "sql_agent.py"),
        ("📊", "Analytics Agent",       "Computation",    "#fbbf24", "Runs Python calculations — growth rates, correlations, forecasts.",             ["compute_growth", "run_python"],    "analytics_agent.py"),
        ("📉", "Visualization Agent",   "Output",         "#f97316", "Generates matplotlib/plotly charts and returns them to the UI.",                ["plot_bar", "plot_line"],           "visualization_agent.py"),
        ("💬", "Explanation Agent",     "Output",         "#34d399", "Transforms raw numbers into human-readable business narratives.",               ["narrate", "format_output"],        "explanation_agent.py"),
        ("✅", "Critic Agent",           "Validation",     "#e2e8f0", "Validates reasoning, checks for hallucinations, refines final answer.",          ["check_facts", "score_confidence"], "critic_agent.py"),
    ]

    cols = st.columns(2)
    for i, (icon, name, tag, color, desc, tools, fname) in enumerate(agent_details):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="ent-card" style="border-top:2px solid {color}">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
                <span style="font-size:24px">{icon}</span>
                <div>
                  <div style="font-weight:600;color:#e2e8f0;font-size:14px">{name}</div>
                  <span style="font-size:10px;background:rgba(99,130,255,.1);color:{color};
                        border:1px solid rgba(99,130,255,.2);border-radius:4px;
                        padding:1px 7px;font-family:'JetBrains Mono',monospace">{tag}</span>
                </div>
                <div style="margin-left:auto;width:10px;height:10px;border-radius:50%;background:{color}"></div>
              </div>
              <p style="font-size:12px;color:#94a3b8;margin:0 0 10px;line-height:1.6">{desc}</p>
              <div style="font-size:11px;color:#64748b;margin-bottom:6px">
                <b style="color:#e2e8f0">Tools:</b> {" · ".join(f'<span class="tag">{t}</span>' for t in tools)}
              </div>
              <div style="font-size:11px;color:#64748b;font-family:'JetBrains Mono',monospace">📁 agents/{fname}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: KNOWLEDGE BASE
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "knowledge":
    st.markdown("""
    <h1 style="font-size:22px;font-weight:700;color:#e2e8f0;margin:0 0 4px">
    📚 Knowledge Base
    </h1>
    <p style="font-size:13px;color:#64748b;margin:0 0 20px">
    Vector database contents, document sources, and retrieval stats
    </p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Chunks", "24,832", "+1,204")
    with c2: st.metric("Documents", "347", "+12")
    with c3: st.metric("Avg Retrieval", "94ms", "-8ms")
    with c4: st.metric("Vector Dim", "1,536", "OpenAI")

    st.markdown("---")
    st.markdown("**Document Sources**")

    docs = [
        ("Q3 Market Outlook Report",        "Gartner",       "PDF",   "2024-09-15", "1,204 chunks", "#6382ff"),
        ("Competitor Analysis 2024",         "Internal BI",   "DOCX",  "2024-09-10", "876 chunks",   "#a78bfa"),
        ("Product Launch Retrospective",     "Product Team",  "PDF",   "2024-08-28", "532 chunks",   "#2dd4bf"),
        ("Customer Satisfaction Survey Q3",  "CX Team",       "CSV",   "2024-09-20", "2,401 chunks", "#fbbf24"),
        ("Annual Report 2023",               "Finance",       "PDF",   "2024-01-10", "4,211 chunks", "#34d399"),
        ("Sales Playbook v4",                "Sales Ops",     "DOCX",  "2024-07-01", "892 chunks",   "#f97316"),
    ]

    for title, source, ftype, date, chunks, color in docs:
        c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 2, 1])
        with c1:
            st.markdown(f'<span style="font-weight:500;color:#e2e8f0">{title}</span>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<span style="color:#64748b;font-size:13px">{source}</span>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<span class="tag" style="color:{color};border-color:{color}40">{ftype}</span>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<span style="color:#64748b;font-size:12px;font-family:monospace">{chunks}</span>', unsafe_allow_html=True)
        with c5:
            st.markdown(f'<span style="color:#64748b;font-size:12px">{date}</span>', unsafe_allow_html=True)
        st.markdown('<hr style="margin:6px 0;border-color:rgba(99,130,255,.08)">', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Upload New Document**")
    uploaded = st.file_uploader("Drop a PDF, DOCX, or CSV to add to the knowledge base", type=["pdf","docx","csv","txt"])
    if uploaded:
        with st.spinner(f"Chunking and embedding {uploaded.name}..."):
            time.sleep(2)
        st.success(f"✅ `{uploaded.name}` indexed — 0 chunks added to Qdrant.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "analytics":
    st.markdown("""
    <h1 style="font-size:22px;font-weight:700;color:#e2e8f0;margin:0 0 4px">
    📊 Analytics Dashboard
    </h1>
    <p style="font-size:13px;color:#64748b;margin:0 0 20px">
    System usage, agent performance, and query analytics
    </p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Queries", "1,247", "+84 today")
    with c2: st.metric("Avg Latency",   "4.2s",  "-0.3s")
    with c3: st.metric("Accuracy",      "94.1%", "+1.2%")
    with c4: st.metric("Active Users",  "38",    "+5")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Agent Performance", "Query Types", "Token Usage"])

    with tab1:
        st.markdown("**Average execution time per agent (ms)**")
        agent_times = {
            "Planner": 320, "Retriever": 890, "SQL": 760,
            "Analytics": 540, "Visualization": 410, "Explanation": 680, "Critic": 290,
        }
        for agent, ms in agent_times.items():
            pct = ms / 1000
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
              <div style="width:110px;font-size:12px;color:#94a3b8">{agent}</div>
              <div style="flex:1;height:8px;background:rgba(99,130,255,.12);border-radius:4px;overflow:hidden">
                <div style="width:{pct*100}%;height:100%;background:linear-gradient(90deg,#6382ff,#a78bfa);border-radius:4px"></div>
              </div>
              <div style="width:50px;text-align:right;font-size:12px;color:#6382ff;font-family:'JetBrains Mono',monospace">{ms}ms</div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("**Query category distribution**")
        categories = [
            ("Revenue Analysis",        38, "#6382ff"),
            ("Customer Insights",       24, "#a78bfa"),
            ("Competitive Intel",       18, "#2dd4bf"),
            ("Forecasting",             12, "#fbbf24"),
            ("Document Summarization",   8, "#34d399"),
        ]
        for label, pct, color in categories:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
              <div style="width:180px;font-size:12px;color:#94a3b8">{label}</div>
              <div style="flex:1;height:8px;background:rgba(99,130,255,.12);border-radius:4px;overflow:hidden">
                <div style="width:{pct}%;height:100%;background:{color};border-radius:4px"></div>
              </div>
              <div style="width:36px;text-align:right;font-size:12px;color:{color};font-family:'JetBrains Mono',monospace">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("**Daily token consumption (last 7 days)**")
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        tokens = [124000, 98000, 143000, 167000, 201000, 88000, 112000]
        max_t = max(tokens)
        for day, tok in zip(days, tokens):
            pct = tok / max_t * 100
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
              <div style="width:36px;font-size:12px;color:#94a3b8">{day}</div>
              <div style="flex:1;height:8px;background:rgba(99,130,255,.12);border-radius:4px;overflow:hidden">
                <div style="width:{pct:.0f}%;height:100%;background:linear-gradient(90deg,#2dd4bf,#6382ff);border-radius:4px"></div>
              </div>
              <div style="width:70px;text-align:right;font-size:12px;color:#2dd4bf;font-family:'JetBrains Mono',monospace">{tok:,}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="ent-card">
      <div style="font-weight:600;color:#e2e8f0;margin-bottom:8px">🔗 LangSmith Trace</div>
      <div style="font-size:13px;color:#94a3b8;line-height:1.7">
        All agent runs are instrumented with <span style="color:#6382ff">LangSmith</span> for
        full trace visibility — latency, token counts, prompt/completion pairs, and error rates.
        Connect your LangSmith API key in <code style="font-family:'JetBrains Mono',monospace;
        color:#a78bfa">.env</code> to enable real-time monitoring.
      </div>
    </div>
    """, unsafe_allow_html=True)

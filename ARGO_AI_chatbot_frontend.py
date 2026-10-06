import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import textwrap

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ARGO Ocean Intelligence",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 80% 5%, #073b55 0%, transparent 28%),
        radial-gradient(circle at 8% 90%, #032c48 0%, transparent 28%),
        linear-gradient(135deg, #020817, #041525, #020b18);
    color: white;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.block-container {
    padding-top: 2.5rem;
    padding-left: 3.5rem;
    padding-right: 3.5rem;
    padding-bottom: 4rem;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#031827,#020b15);
    border-right: 1px solid rgba(44,225,255,.14);
}

[data-testid="stSidebar"] * {
    color: #d9f8ff;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(44,225,255,.10);
}

.sidebar-title {
    font-size: 26px;
    font-weight: 800;
}

.sidebar-subtitle {
    color: #688b9b;
    font-size: 10px;
    letter-spacing: 1.5px;
    margin-top: 4px;
}

/* TYPOGRAPHY */

.argo-label {
    color: #39e7ff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 4px;
}

.main-title {
    font-size: 52px;
    font-weight: 800;
    margin: 5px 0 2px 0;
    background: linear-gradient(90deg,#fff,#56e9ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #89a6b8;
    font-size: 16px;
    line-height: 1.7;
    max-width: 850px;
}

.section-label {
    color: #678b9c;
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: 700;
    margin-top: 8px;
}

.section-title {
    color: #f2fcff;
    font-size: 23px;
    font-weight: 700;
    margin: 3px 0 15px 0;
}

.glow-line {
    height: 1px;
    margin: 25px 0;
    background: linear-gradient(
        90deg,
        #25dfff,
        rgba(37,223,255,.12),
        transparent
    );
}

.live-badge {
    display:inline-block;
    margin-top:17px;
    padding:7px 14px;
    border-radius:30px;
    border:1px solid #00e5a8;
    background:rgba(0,229,168,.06);
    color:#00f5b0;
    font-size:11px;
    font-weight:700;
}

/* CARDS */

.metric-card {
    min-height: 145px;
    padding: 20px;
    border-radius: 17px;
    background: linear-gradient(
        145deg,
        rgba(8,38,57,.88),
        rgba(3,18,31,.93)
    );
    border:1px solid rgba(66,220,255,.13);
    box-shadow:0 12px 30px rgba(0,0,0,.20);
    transition:.25s;
}

.metric-card:hover {
    transform:translateY(-3px);
    border-color:rgba(66,220,255,.45);
}

.card-top {
    display:flex;
    justify-content:space-between;
}

.card-icon {font-size:23px;}

.status-good {
    color:#00e7b1;
    font-size:9px;
    letter-spacing:1px;
    font-weight:700;
}

.status-warn {
    color:#ffb454;
    font-size:9px;
    letter-spacing:1px;
    font-weight:700;
}

.card-label {
    color:#7594a5;
    font-size:10px;
    font-weight:700;
    letter-spacing:1.2px;
    margin-top:16px;
}

.card-value {
    color:white;
    font-size:27px;
    font-weight:800;
    margin-top:3px;
}

.card-note {
    color:#00dca8;
    font-size:10px;
    margin-top:5px;
}

.card-note-warn {
    color:#ffb454;
    font-size:10px;
    margin-top:5px;
}

/* PANELS */

.panel {
    padding:20px;
    border-radius:17px;
    background:linear-gradient(
        145deg,
        rgba(6,31,48,.78),
        rgba(3,17,29,.86)
    );
    border:1px solid rgba(60,220,255,.10);
}

.panel-title {
    color:#effcff;
    font-size:16px;
    font-weight:700;
}

.panel-text {
    color:#7d9ba9;
    font-size:12px;
    line-height:1.7;
    margin-top:6px;
}

.info-box {
    padding:17px;
    border-radius:14px;
    background:rgba(45,220,255,.045);
    border:1px solid rgba(45,220,255,.12);
}

.warning-box {
    padding:17px;
    border-radius:14px;
    background:rgba(255,171,74,.055);
    border:1px solid rgba(255,171,74,.20);
}

.success-box {
    padding:17px;
    border-radius:14px;
    background:rgba(0,229,168,.055);
    border:1px solid rgba(0,229,168,.17);
}

.result-big {
    color:#48e6ff;
    font-size:34px;
    font-weight:800;
}

.result-label {
    color:#7998a7;
    font-size:10px;
    letter-spacing:1.4px;
    font-weight:700;
}

.small-text {
    color:#7895a4;
    font-size:11px;
    line-height:1.6;
}

/* TABLE */

[data-testid="stDataFrame"] {
    border:1px solid rgba(54,218,255,.10);
    border-radius:14px;
}

/* BUTTON */

.stButton > button {
    border-radius:10px;
    border:1px solid rgba(49,220,255,.30);
    background:rgba(26,168,196,.10);
    color:#dffbff;
    font-weight:600;
}

.stButton > button:hover {
    border-color:#38e4ff;
    color:white;
}

/* TABS */

.stTabs [data-baseweb="tab-list"] {
    gap:10px;
}

.stTabs [data-baseweb="tab"] {
    background:rgba(5,29,44,.65);
    border-radius:10px;
    padding:10px 18px;
}


/* ARGO AI CHAT */

.chat-welcome {
    padding: 22px;
    border-radius: 18px;
    background: linear-gradient(145deg, rgba(8,38,57,.82), rgba(3,18,31,.92));
    border: 1px solid rgba(66,220,255,.16);
    margin-bottom: 18px;
}

.chat-welcome-title {
    color: #effcff;
    font-size: 19px;
    font-weight: 750;
}

.chat-welcome-text {
    color: #7f9eac;
    font-size: 12px;
    line-height: 1.7;
    margin-top: 7px;
}

[data-testid="stChatMessage"] {
    background: rgba(4,25,40,.62);
    border: 1px solid rgba(57,220,255,.10);
    border-radius: 16px;
    padding: 8px 12px;
    margin-bottom: 10px;
}

[data-testid="stChatInput"] {
    border: 1px solid rgba(57,220,255,.20);
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def page_header(label, title, description):
    st.markdown(
        f'<div class="argo-label">{label}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="main-title">{title}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="subtitle">{description}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="glow-line"></div>',
        unsafe_allow_html=True
    )


def section(label, title):
    st.markdown(
        f'<div class="section-label">{label}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )


def metric_card(icon, label, value, status, note, warning=False):
    status_class = "status-warn" if warning else "status-good"
    note_class = "card-note-warn" if warning else "card-note"

    card_html = (
        f'<div class="metric-card">'
        f'<div class="card-top">'
        f'<div class="card-icon">{icon}</div>'
        f'<div class="{status_class}">{status}</div>'
        f'</div>'
        f'<div class="card-label">{label}</div>'
        f'<div class="card-value">{value}</div>'
        f'<div class="{note_class}">{note}</div>'
        f'</div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)



def style_figure(fig, height=330):

    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=25, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#7896a5"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )
    )

    fig.update_xaxes(
        gridcolor="rgba(255,255,255,.04)"
    )

    fig.update_yaxes(
        gridcolor="rgba(255,255,255,.05)"
    )

    return fig


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🌊 ARGO AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'OCEAN INTELLIGENCE PLATFORM'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "🤖 ARGO AI Chat",
            "🌐 Dashboard",
            "📁 Data Center",
            "🔮 Prediction",
            "⚠️ Anomaly Detection",
            "🧭 Float Explorer",
            "🌍 Ocean Map",
            "📊 Analytics"
        ]
    )

    st.markdown("---")

    st.caption("SYSTEM STATUS")

    st.success("● APPLICATION ONLINE")
    st.info("● FRONTEND READY")

    st.markdown("---")

    st.caption("ARGO Intelligence • v1.0")


# =========================================================
# DEFAULT DEMO DATA
# =========================================================

np.random.seed(21)

dates = pd.date_range(
    end=datetime.now(),
    periods=60,
    freq="D"
)

temperature = (
    24
    + np.sin(np.linspace(0, 8, 60)) * 1.4
    + np.random.normal(0, .18, 60)
)

salinity = (
    35
    + np.cos(np.linspace(0, 7, 60)) * .35
    + np.random.normal(0, .05, 60)
)

depth = np.random.randint(
    100,
    2001,
    60
)

demo_df = pd.DataFrame({
    "Date": dates,
    "Temperature": temperature,
    "Salinity": salinity,
    "Depth": depth
})


float_data = pd.DataFrame({

    "Float_ID": [
        "ARGO-101","ARGO-102","ARGO-103","ARGO-104",
        "ARGO-105","ARGO-106","ARGO-107","ARGO-108",
        "ARGO-109","ARGO-110","ARGO-111","ARGO-112",
        "ARGO-113","ARGO-114","ARGO-115"
    ],

    "Latitude": [
        18.9,14.2,9.8,-4.5,-18.2,
        25.5,-11.4,6.7,-27.2,31.1,
        1.2,-8.5,21.5,-15.1,3.8
    ],

    "Longitude": [
        72.8,82.4,65.3,89.8,108.4,
        57.6,74.3,94.5,67.1,69.4,
        79.6,101.2,92.1,61.3,86.5
    ],

    "Temperature": [
        24.6,25.2,26.1,23.7,21.9,
        24.1,22.8,26.4,20.7,23.9,
        25.6,24.8,25.1,21.8,26.0
    ],

    "Salinity": [
        35.1,34.9,35.3,35.0,34.7,
        35.2,35.4,34.8,35.0,35.3,
        34.9,35.1,35.0,35.5,34.8
    ],

    "Depth": [
        1800,2000,1600,1950,1750,
        2000,1850,1700,1900,2000,
        1650,1800,1900,1750,2000
    ],

    "Status": [
        "Normal","Normal","Normal","Anomaly",
        "Normal","Normal","Anomaly","Normal",
        "Normal","Normal","Normal","Anomaly",
        "Normal","Normal","Normal"
    ]
})



# =========================================================
# DEMO FLOAT PROFILE DATA
# =========================================================

# Temporary frontend-only profile data.
# Later, Person 1's backend/API can replace this dataframe
# without changing the Float Explorer page layout.

profile_rows = []

for float_index, float_row in float_data.iloc[:6].iterrows():

    for cycle in [1, 2, 3]:

        profile_depths = np.arange(0, 2001, 100)

        # Create realistic-looking demonstration vertical profiles.
        profile_temperature = (
            float_row["Temperature"]
            - 0.0075 * profile_depths
            + 0.35 * np.sin(profile_depths / 260 + cycle)
        )

        profile_salinity = (
            float_row["Salinity"]
            + 0.00018 * profile_depths
            + 0.035 * np.cos(profile_depths / 300 + cycle)
        )

        profile_date = (
            datetime.now()
            - timedelta(days=(3 - cycle) * 10 + float_index)
        )

        for d, t, s in zip(
            profile_depths,
            profile_temperature,
            profile_salinity
        ):
            profile_rows.append({
                "Float_ID": float_row["Float_ID"],
                "Cycle": cycle,
                "Date": profile_date,
                "Latitude": float_row["Latitude"],
                "Longitude": float_row["Longitude"],
                "Depth": float(d),
                "Temperature": float(t),
                "Salinity": float(s),
            })

profile_data = pd.DataFrame(profile_rows)


# =========================================================
# SESSION DATA
# =========================================================

if "ocean_data" not in st.session_state:
    st.session_state.ocean_data = demo_df

if "using_uploaded_data" not in st.session_state:
    st.session_state.using_uploaded_data = False


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_prompt_seed" not in st.session_state:
    st.session_state.chat_prompt_seed = None



# =========================================================
# ARGO AI CHAT HELPERS
# =========================================================

def interpret_argo_prompt(prompt):
    """Temporary frontend intent parser.
    Person 5 can later replace this with the real chatbot/API response.
    """
    q = prompt.lower().strip()

    if ("float" in q or "profile" in q) and (
        "depth" in q or "temperature" in q or "salinity" in q or "profile" in q
    ):
        return "profile"

    if any(word in q for word in ["anomaly", "anomalies", "abnormal", "unusual"]):
        return "anomaly"

    if any(word in q for word in ["predict", "prediction", "forecast", "future"]):
        if "salinity" in q:
            return "prediction_salinity"
        return "prediction_temperature"

    if "salinity" in q:
        return "salinity"

    if any(word in q for word in ["temperature", "temp", "warming"]):
        return "temperature"

    if any(word in q for word in ["map", "location", "locations", "where are", "floats"]):
        return "map"

    if any(word in q for word in ["summary", "overview", "analytics", "analyse", "analyze"]):
        return "summary"

    return "help"


def render_chat_result(intent):
    data = st.session_state.ocean_data.copy()

    if intent == "temperature":
        if "Temperature" not in data.columns:
            st.warning("Temperature data is not available in the current dataset.")
            return

        if "Date" not in data.columns:
            data["Date"] = range(1, len(data) + 1)

        st.markdown("**ARGO AI:** Here is the temperature trend in the current ocean dataset.")

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=data["Temperature"],
                mode="lines+markers",
                name="Temperature",
                line=dict(color="#35dcff", width=3)
            )
        )
        fig.update_layout(
            title="Temperature Trend",
            xaxis_title="Observation / Date",
            yaxis_title="Temperature (°C)"
        )
        style_figure(fig, 390)
        st.plotly_chart(fig, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Average", f"{data['Temperature'].mean():.2f} °C")
        c2.metric("Maximum", f"{data['Temperature'].max():.2f} °C")
        c3.metric("Minimum", f"{data['Temperature'].min():.2f} °C")

    elif intent == "salinity":
        if "Salinity" not in data.columns:
            st.warning("Salinity data is not available in the current dataset.")
            return

        if "Date" not in data.columns:
            data["Date"] = range(1, len(data) + 1)

        st.markdown("**ARGO AI:** Here is the salinity trend in the current ocean dataset.")

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=data["Salinity"],
                mode="lines+markers",
                name="Salinity",
                line=dict(color="#00e6ad", width=3)
            )
        )
        fig.update_layout(
            title="Salinity Trend",
            xaxis_title="Observation / Date",
            yaxis_title="Salinity (PSU)"
        )
        style_figure(fig, 390)
        st.plotly_chart(fig, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Average", f"{data['Salinity'].mean():.3f} PSU")
        c2.metric("Maximum", f"{data['Salinity'].max():.3f} PSU")
        c3.metric("Minimum", f"{data['Salinity'].min():.3f} PSU")

    elif intent == "profile":
        selected_float_id = profile_data["Float_ID"].iloc[0]
        selected_cycle = profile_data[
            profile_data["Float_ID"] == selected_float_id
        ]["Cycle"].max()

        selected_profile = profile_data[
            (profile_data["Float_ID"] == selected_float_id)
            & (profile_data["Cycle"] == selected_cycle)
        ].sort_values("Depth")

        st.markdown(
            f"**ARGO AI:** Showing the latest demo profile for "
            f"**{selected_float_id}**, cycle **{selected_cycle}**."
        )

        p1, p2 = st.columns(2)

        with p1:
            fig_t = go.Figure()
            fig_t.add_trace(
                go.Scatter(
                    x=selected_profile["Temperature"],
                    y=selected_profile["Depth"],
                    mode="lines+markers",
                    name="Temperature",
                    line=dict(color="#35dcff", width=3)
                )
            )
            fig_t.update_layout(
                title="Temperature vs Depth",
                xaxis_title="Temperature (°C)",
                yaxis_title="Depth (m)"
            )
            fig_t.update_yaxes(autorange="reversed")
            style_figure(fig_t, 430)
            st.plotly_chart(fig_t, use_container_width=True)

        with p2:
            fig_s = go.Figure()
            fig_s.add_trace(
                go.Scatter(
                    x=selected_profile["Salinity"],
                    y=selected_profile["Depth"],
                    mode="lines+markers",
                    name="Salinity",
                    line=dict(color="#00e6ad", width=3)
                )
            )
            fig_s.update_layout(
                title="Salinity vs Depth",
                xaxis_title="Salinity (PSU)",
                yaxis_title="Depth (m)"
            )
            fig_s.update_yaxes(autorange="reversed")
            style_figure(fig_s, 430)
            st.plotly_chart(fig_s, use_container_width=True)

    elif intent == "anomaly":
        anomaly_df = float_data.copy()
        anomaly_df["Anomaly_Score"] = [
            .08, .12, .15, .89, .18,
            .11, .82, .16, .13, .10,
            .20, .91, .14, .19, .09
        ]
        anomaly_df["AI_Result"] = np.where(
            anomaly_df["Anomaly_Score"] > .70,
            "Anomaly",
            "Normal"
        )

        flagged = anomaly_df[anomaly_df["AI_Result"] == "Anomaly"]

        st.markdown(
            f"**ARGO AI:** I found **{len(flagged)} demonstration anomalies** "
            "in the current float dataset."
        )

        fig = px.bar(
            anomaly_df,
            x="Float_ID",
            y="Anomaly_Score",
            color="AI_Result",
            title="Anomaly Scores by ARGO Float"
        )
        fig.add_hline(
            y=.70,
            line_dash="dash",
            annotation_text="Demo threshold"
        )
        style_figure(fig, 420)
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            flagged[
                [
                    "Float_ID",
                    "Temperature",
                    "Salinity",
                    "Depth",
                    "Anomaly_Score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )
        st.caption("Demo anomaly results — Person 3's model will replace these values.")

    elif intent in ["prediction_temperature", "prediction_salinity"]:
        target = "Temperature" if intent == "prediction_temperature" else "Salinity"
        unit = "°C" if target == "Temperature" else "PSU"
        horizon = 7
        future_dates = pd.date_range(
            datetime.now() + timedelta(days=1),
            periods=horizon,
            freq="D"
        )

        if target == "Temperature":
            values = 24.5 + np.sin(np.linspace(0, 2, horizon)) * .7
        else:
            values = 35.0 + np.cos(np.linspace(0, 2, horizon)) * .15

        st.markdown(
            f"**ARGO AI:** Here is a **7-day demo {target.lower()} forecast**. "
            "Person 2's trained model will later provide the real forecast."
        )

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=future_dates,
                y=values,
                mode="lines+markers",
                name=f"{target} Forecast",
                line=dict(color="#41e4ff", width=3)
            )
        )
        fig.update_layout(
            title=f"7-Day {target} Forecast",
            xaxis_title="Date",
            yaxis_title=f"{target} ({unit})"
        )
        style_figure(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Forecast Average", f"{values.mean():.2f} {unit}")
        c2.metric("Maximum", f"{values.max():.2f} {unit}")
        c3.metric("Minimum", f"{values.min():.2f} {unit}")

    elif intent == "map":
        st.markdown("**ARGO AI:** Here are the current demonstration ARGO float locations.")

        fig = px.scatter_geo(
            float_data,
            lat="Latitude",
            lon="Longitude",
            color="Temperature",
            size="Depth",
            hover_name="Float_ID",
            hover_data={
                "Temperature": True,
                "Salinity": True,
                "Depth": True,
                "Status": True
            },
            color_continuous_scale="Turbo",
            projection="natural earth"
        )
        fig.update_geos(
            showland=True,
            landcolor="#071923",
            showocean=True,
            oceancolor="#031827",
            coastlinecolor="#24566a",
            countrycolor="#183d4b",
            showcountries=True,
            bgcolor="rgba(0,0,0,0)"
        )
        fig.update_layout(
            height=500,
            margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#7d9ba9")
        )
        st.plotly_chart(fig, use_container_width=True)

    elif intent == "summary":
        st.markdown("**ARGO AI:** Here is a quick summary of the current ocean observations.")

        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Records", len(data))

        if "Temperature" in data.columns:
            s2.metric("Avg Temperature", f"{data['Temperature'].mean():.2f} °C")
        else:
            s2.metric("Avg Temperature", "N/A")

        if "Salinity" in data.columns:
            s3.metric("Avg Salinity", f"{data['Salinity'].mean():.3f} PSU")
        else:
            s3.metric("Avg Salinity", "N/A")

        s4.metric(
            "Anomaly Floats",
            int((float_data["Status"] == "Anomaly").sum())
        )

        numeric = data.select_dtypes(include=np.number).columns.tolist()
        if len(numeric) >= 2:
            corr = data[numeric].corr()
            fig = px.imshow(
                corr,
                text_auto=".2f",
                aspect="auto",
                title="Ocean Parameter Correlation"
            )
            style_figure(fig, 430)
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.markdown(
            "**ARGO AI:** I can currently create visual analytics for "
            "**temperature, salinity, float profiles, anomalies, predictions, "
            "maps and dataset summaries**."
        )
        st.info(
            'Try: "Show temperature trend", "Show salinity analysis", '
            '"Show anomalies", "Predict temperature", '
            '"Show a float profile", or "Show float locations".'
        )


# =========================================================
# DASHBOARD
# =========================================================

if page == "🤖 ARGO AI Chat":

    page_header(
        "CONVERSATIONAL OCEAN INTELLIGENCE",
        "Ask ARGO AI.",
        "Ask a question about ocean observations and receive "
        "an instant visual response."
    )

    st.markdown(
        '<div class="chat-welcome">'
        '<div class="chat-welcome-title">🌊 What would you like to explore?</div>'
        '<div class="chat-welcome-text">'
        'Ask for temperature or salinity trends, float profiles, '
        'anomaly results, forecasts, maps or a quick dataset summary. '
        'This frontend currently uses a temporary prompt interpreter; '
        'Person 5 can later connect the real AI chatbot without redesigning this page.'
        '</div></div>',
        unsafe_allow_html=True
    )

    section("QUICK QUESTIONS", "Try a Prompt")

    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("🌡️ Temperature Trend", use_container_width=True):
            st.session_state.chat_prompt_seed = "Show temperature trend"
    with q2:
        if st.button("💧 Salinity Analysis", use_container_width=True):
            st.session_state.chat_prompt_seed = "Show salinity analysis"
    with q3:
        if st.button("⚠️ Show Anomalies", use_container_width=True):
            st.session_state.chat_prompt_seed = "Show anomalies"

    q4, q5, q6 = st.columns(3)
    with q4:
        if st.button("🧭 Float Profile", use_container_width=True):
            st.session_state.chat_prompt_seed = "Show a float profile"
    with q5:
        if st.button("🔮 Predict Temperature", use_container_width=True):
            st.session_state.chat_prompt_seed = "Predict temperature"
    with q6:
        if st.button("🌍 Float Locations", use_container_width=True):
            st.session_state.chat_prompt_seed = "Show float locations on map"

    st.write("")
    section("CONVERSATION", "Ocean Analytics Assistant")

    # Render previous conversation turns.
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])
            if message["role"] == "assistant" and message.get("intent"):
                render_chat_result(message["intent"])

    prompt = st.chat_input(
        "Ask ARGO AI about temperature, salinity, profiles, anomalies or predictions..."
    )

    # Quick buttons behave like ready-made prompts.
    if st.session_state.chat_prompt_seed:
        prompt = st.session_state.chat_prompt_seed
        st.session_state.chat_prompt_seed = None

    if prompt:
        st.session_state.chat_history.append(
            {"role": "user", "text": prompt}
        )

        intent = interpret_argo_prompt(prompt)

        response_text = {
            "temperature": "I analysed your request and generated a temperature visualization.",
            "salinity": "I analysed your request and generated a salinity visualization.",
            "profile": "I selected an ARGO float profile and generated vertical ocean-profile charts.",
            "anomaly": "I analysed the float observations and generated the anomaly view.",
            "prediction_temperature": "I generated the current demo temperature forecast.",
            "prediction_salinity": "I generated the current demo salinity forecast.",
            "map": "I generated the ARGO float location map.",
            "summary": "I generated a quick analytics summary of the current dataset.",
            "help": "I need a little more detail about the ocean analysis you want."
        }[intent]

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "text": response_text,
                "intent": intent
            }
        )

        st.rerun()


elif page == "🌐 Dashboard":

    page_header(
        "ARGO INTELLIGENCE",
        "Ocean Intelligence.",
        "AI-powered monitoring, prediction and anomaly detection "
        "for ARGO ocean observations."
    )

    st.markdown(
        '<div class="live-badge">● SYSTEM ONLINE</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    data = st.session_state.ocean_data

    # Get usable averages safely

    if "Temperature" in data.columns:
        avg_temp = data["Temperature"].mean()
    else:
        avg_temp = 24.6

    if "Salinity" in data.columns:
        avg_salinity = data["Salinity"].mean()
    else:
        avg_salinity = 35.1

    anomaly_count = len(
        float_data[
            float_data["Status"] == "Anomaly"
        ]
    )

    section(
        "OCEAN STATUS",
        "Live Overview"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "🌡️",
            "AVG TEMPERATURE",
            f"{avg_temp:.1f} °C",
            "NORMAL",
            "● Ocean observation"
        )

    with c2:
        metric_card(
            "💧",
            "AVG SALINITY",
            f"{avg_salinity:.2f} PSU",
            "STABLE",
            "● Within expected range"
        )

    with c3:
        metric_card(
            "📡",
            "ARGO FLOATS",
            str(len(float_data)),
            "ACTIVE",
            "● Monitoring network"
        )

    with c4:
        metric_card(
            "⚠️",
            "ANOMALIES",
            str(anomaly_count),
            "ATTENTION",
            "⚠ Requires analysis",
            True
        )


    st.write("")
    st.write("")

    section(
        "OCEAN OBSERVATIONS",
        "Parameter Trends"
    )

    if (
        "Temperature" in data.columns
        and
        "Salinity" in data.columns
    ):

        graph_data = data.copy()

        if "Date" not in graph_data.columns:
            graph_data["Date"] = range(
                1,
                len(graph_data) + 1
            )

        g1, g2 = st.columns(2)

        with g1:

            temp_fig = go.Figure()

            temp_fig.add_trace(
                go.Scatter(
                    x=graph_data["Date"],
                    y=graph_data["Temperature"],
                    mode="lines",
                    name="Temperature",
                    line=dict(
                        color="#35dcff",
                        width=3
                    ),
                    fill="tozeroy",
                    fillcolor="rgba(53,220,255,.04)"
                )
            )

            style_figure(temp_fig)

            st.plotly_chart(
                temp_fig,
                use_container_width=True
            )

        with g2:

            salt_fig = go.Figure()

            salt_fig.add_trace(
                go.Scatter(
                    x=graph_data["Date"],
                    y=graph_data["Salinity"],
                    mode="lines",
                    name="Salinity",
                    line=dict(
                        color="#00e6ad",
                        width=3
                    )
                )
            )

            style_figure(salt_fig)

            st.plotly_chart(
                salt_fig,
                use_container_width=True
            )

    else:

        st.info(
            "Upload data containing Temperature and Salinity "
            "columns to display both trend charts."
        )


    st.write("")

    section(
        "AI SYSTEM",
        "Platform Capabilities"
    )

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown("""
        <div class="info-box">
        <div class="panel-title">🔮 Forecasting</div>
        <div class="panel-text">
        Predict future temperature and salinity behaviour
        from historical ARGO observations.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div class="info-box">
        <div class="panel-title">⚠️ Anomaly Detection</div>
        <div class="panel-text">
        Identify unusual ocean profiles, sensor behaviour
        and potentially abnormal measurements.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown("""
        <div class="info-box">
        <div class="panel-title">🌍 Spatial Intelligence</div>
        <div class="panel-text">
        Explore ocean observations geographically through
        an interactive ARGO monitoring network.
        </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# DATA CENTER
# =========================================================

elif page == "📁 Data Center":

    page_header(
        "DATA MANAGEMENT",
        "ARGO Data Center.",
        "Upload, inspect and prepare ocean observations "
        "before prediction and anomaly analysis."
    )

    section(
        "DATA INPUT",
        "Upload Dataset"
    )

    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            uploaded_df = pd.read_csv(
                uploaded_file
            )

            st.session_state.ocean_data = uploaded_df
            st.session_state.using_uploaded_data = True

            st.success(
                "Dataset loaded successfully."
            )

        except Exception as error:

            st.error(
                f"Could not read dataset: {error}"
            )


    data = st.session_state.ocean_data

    if st.session_state.using_uploaded_data:
        st.info("Currently using your uploaded dataset.")
    else:
        st.info(
            "No dataset uploaded yet. "
            "The application is using demonstration data."
        )


    st.write("")

    section(
        "DATA OVERVIEW",
        "Dataset Summary"
    )

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        st.metric(
            "Rows",
            len(data)
        )

    with d2:
        st.metric(
            "Columns",
            len(data.columns)
        )

    with d3:
        st.metric(
            "Missing Values",
            int(data.isnull().sum().sum())
        )

    with d4:
        st.metric(
            "Duplicates",
            int(data.duplicated().sum())
        )


    st.write("")

    tab1, tab2, tab3 = st.tabs(
        [
            "Dataset Preview",
            "Column Information",
            "Missing Values"
        ]
    )

    with tab1:

        st.dataframe(
            data.head(100),
            use_container_width=True
        )

    with tab2:

        column_info = pd.DataFrame({
            "Column": data.columns,
            "Data Type": [
                str(dtype)
                for dtype in data.dtypes
            ]
        })

        st.dataframe(
            column_info,
            use_container_width=True,
            hide_index=True
        )

    with tab3:

        missing = pd.DataFrame({
            "Column": data.columns,
            "Missing Values": data.isnull().sum().values
        })

        missing["Percentage"] = (
            missing["Missing Values"]
            / max(len(data), 1)
            * 100
        ).round(2)

        st.dataframe(
            missing,
            use_container_width=True,
            hide_index=True
        )


    st.write("")

    csv_data = data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇ Download Current Dataset",
        csv_data,
        "argo_dataset.csv",
        "text/csv"
    )


# =========================================================
# PREDICTION PAGE
# =========================================================

elif page == "🔮 Prediction":

    page_header(
        "MODULE 01 • FORECASTING",
        "Ocean Prediction.",
        "Configure future ocean forecasts for temperature "
        "and salinity. Real ML models will be connected "
        "to this interface in the model-integration stage."
    )

    left, right = st.columns(
        [1, 2]
    )

    with left:

        section(
            "FORECAST SETTINGS",
            "Configure Prediction"
        )

        target = st.selectbox(
            "Prediction Target",
            [
                "Temperature",
                "Salinity"
            ]
        )

        model_name = st.selectbox(
            "Forecasting Model",
            [
                "LSTM",
                "GRU",
                "Prophet",
                "XGBoost",
                "LightGBM",
                "TFT"
            ]
        )

        horizon = st.slider(
            "Forecast Horizon",
            1,
            30,
            7
        )

        depth_input = st.slider(
            "Ocean Depth (m)",
            0,
            2000,
            500,
            step=50
        )

        latitude = st.number_input(
            "Latitude",
            value=18.90
        )

        longitude = st.number_input(
            "Longitude",
            value=72.80
        )

        run_prediction = st.button(
            "🔮 Generate Forecast",
            use_container_width=True
        )


    with right:

        section(
            "FORECAST OUTPUT",
            f"{target} Forecast"
        )

        if run_prediction:

            # ---------------------------------------------
            # DEMO ONLY
            # Replace this section with real model.predict()
            # ---------------------------------------------

            future_dates = pd.date_range(
                datetime.now() + timedelta(days=1),
                periods=horizon,
                freq="D"
            )

            if target == "Temperature":

                base = 24.5

                prediction_values = (
                    base
                    + np.sin(
                        np.linspace(
                            0,
                            2,
                            horizon
                        )
                    ) * .7
                )

                unit = "°C"

            else:

                base = 35.0

                prediction_values = (
                    base
                    + np.cos(
                        np.linspace(
                            0,
                            2,
                            horizon
                        )
                    ) * .15
                )

                unit = "PSU"


            prediction_df = pd.DataFrame({
                "Date": future_dates,
                "Prediction": prediction_values
            })


            pred_fig = go.Figure()

            pred_fig.add_trace(
                go.Scatter(
                    x=prediction_df["Date"],
                    y=prediction_df["Prediction"],
                    mode="lines+markers",
                    name="Forecast",
                    line=dict(
                        color="#41e4ff",
                        width=3
                    )
                )
            )

            style_figure(
                pred_fig,
                380
            )

            st.plotly_chart(
                pred_fig,
                use_container_width=True
            )


            r1, r2, r3 = st.columns(3)

            with r1:
                st.metric(
                    "Forecast Average",
                    f"{prediction_values.mean():.2f} {unit}"
                )

            with r2:
                st.metric(
                    "Maximum",
                    f"{prediction_values.max():.2f} {unit}"
                )

            with r3:
                st.metric(
                    "Minimum",
                    f"{prediction_values.min():.2f} {unit}"
                )


            st.warning(
                "Demo frontend forecast only. "
                "This result is not yet produced by the trained "
                f"{model_name} model."
            )


            st.download_button(
                "⬇ Export Forecast",
                prediction_df.to_csv(
                    index=False
                ).encode("utf-8"),
                "argo_forecast.csv",
                "text/csv"
            )

        else:

            st.markdown("""
            <div class="info-box">

            <div class="panel-title">
            🌊 Forecast Workspace
            </div>

            <div class="panel-text">

            Choose the target, forecasting model,
            location, depth and prediction horizon.

            <br><br>

            The forecast visualization and model results
            will appear here.

            </div>

            </div>
            """, unsafe_allow_html=True)


# =========================================================
# ANOMALY DETECTION
# =========================================================

elif page == "⚠️ Anomaly Detection":

    page_header(
        "MODULE 02 • AI DETECTION",
        "Anomaly Detection.",
        "Identify unusual ARGO observations and analyse "
        "why a measurement may require attention."
    )

    section(
        "ANALYSIS SETTINGS",
        "Configure Detector"
    )

    a1, a2, a3 = st.columns(3)

    with a1:

        anomaly_model = st.selectbox(
            "Detection Model",
            [
                "Isolation Forest",
                "One-Class SVM",
                "Autoencoder"
            ]
        )

    with a2:

        sensitivity = st.slider(
            "Detection Sensitivity",
            1,
            10,
            5
        )

    with a3:

        anomaly_parameter = st.selectbox(
            "Analyse Parameter",
            [
                "All Parameters",
                "Temperature",
                "Salinity",
                "Depth"
            ]
        )


    run_detection = st.button(
        "⚠️ Run Anomaly Detection"
    )


    st.write("")

    if run_detection:

        # ---------------------------------------------
        # DEMO ANOMALY RESULT
        # Replace with actual model predictions later.
        # ---------------------------------------------

        result_df = float_data.copy()

        result_df["Anomaly_Score"] = [
            .08,.12,.15,.89,.18,
            .11,.82,.16,.13,.10,
            .20,.91,.14,.19,.09
        ]

        result_df["AI_Result"] = np.where(
            result_df["Anomaly_Score"] > .70,
            "Anomaly",
            "Normal"
        )


        normal_count = (
            result_df["AI_Result"] == "Normal"
        ).sum()

        anomaly_total = (
            result_df["AI_Result"] == "Anomaly"
        ).sum()


        r1, r2, r3 = st.columns(3)

        with r1:
            metric_card(
                "📊",
                "OBSERVATIONS",
                str(len(result_df)),
                "ANALYSED",
                "● Detection complete"
            )

        with r2:
            metric_card(
                "✓",
                "NORMAL",
                str(normal_count),
                "SAFE",
                "● Expected behaviour"
            )

        with r3:
            metric_card(
                "⚠️",
                "ANOMALIES",
                str(anomaly_total),
                "ATTENTION",
                "⚠ Review observations",
                True
            )


        st.write("")
        st.write("")

        section(
            "AI RESULTS",
            "Detection Results"
        )


        anomaly_only = result_df[
            result_df["AI_Result"]
            ==
            "Anomaly"
        ]


        st.dataframe(
            result_df[
                [
                    "Float_ID",
                    "Temperature",
                    "Salinity",
                    "Depth",
                    "Anomaly_Score",
                    "AI_Result"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


        st.write("")

        section(
            "EXPLAINABLE AI",
            "Why Were These Flagged?"
        )


        for _, row in anomaly_only.iterrows():

            st.markdown(
                f"""
                <div class="warning-box">

                <div class="panel-title">
                ⚠ {row['Float_ID']}
                </div>

                <div class="panel-text">

                Anomaly score:
                <b>{row['Anomaly_Score']:.2f}</b>

                <br>

                The observation differs from the
                expected combination of temperature,
                salinity and depth behaviour.

                <br>

                This record should be reviewed before
                being used in downstream forecasting.

                </div>

                </div>

                <br>
                """,
                unsafe_allow_html=True
            )


        st.warning(
            "These are demonstration anomaly scores. "
            f"The actual {anomaly_model} model will replace "
            "this logic during ML integration."
        )


        st.download_button(
            "⬇ Export Detection Results",
            result_df.to_csv(
                index=False
            ).encode("utf-8"),
            "anomaly_results.csv",
            "text/csv"
        )


    else:

        st.markdown("""
        <div class="info-box">

        <div class="panel-title">
        🤖 AI Anomaly Engine
        </div>

        <div class="panel-text">

        Select the anomaly detection model and sensitivity,
        then run the analysis.

        <br><br>

        Results, anomaly scores and explanations
        will appear here.

        </div>

        </div>
        """, unsafe_allow_html=True)


# =========================================================
# FLOAT PROFILE EXPLORER
# =========================================================

elif page == "🧭 Float Explorer":

    page_header(
        "ARGO PROFILE EXPLORATION",
        "Float Profile Explorer.",
        "Explore a selected ARGO float and inspect how temperature "
        "and salinity change through the water column."
    )

    st.info(
        "Frontend demonstration data is being used on this page. "
        "The same interface is ready to receive real profile data "
        "from the backend API during integration."
    )

    section(
        "PROFILE CONTROLS",
        "Select Float & Cycle"
    )

    control1, control2 = st.columns(2)

    with control1:
        explorer_float = st.selectbox(
            "Select ARGO Float",
            sorted(profile_data["Float_ID"].unique()),
            key="explorer_float"
        )

    available_cycles = sorted(
        profile_data.loc[
            profile_data["Float_ID"] == explorer_float,
            "Cycle"
        ].unique()
    )

    with control2:
        explorer_cycle = st.selectbox(
            "Select Profile / Cycle",
            available_cycles,
            key="explorer_cycle"
        )

    selected_profile = profile_data[
        (profile_data["Float_ID"] == explorer_float)
        & (profile_data["Cycle"] == explorer_cycle)
    ].copy()

    selected_profile = selected_profile.sort_values("Depth")

    profile_date = pd.to_datetime(
        selected_profile["Date"].iloc[0]
    )

    profile_latitude = selected_profile["Latitude"].iloc[0]
    profile_longitude = selected_profile["Longitude"].iloc[0]
    max_depth = selected_profile["Depth"].max()

    st.write("")

    section(
        "PROFILE SUMMARY",
        "Selected Observation"
    )

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        metric_card(
            "📡",
            "FLOAT ID",
            explorer_float,
            "SELECTED",
            f"● Cycle {explorer_cycle}"
        )

    with p2:
        metric_card(
            "📅",
            "PROFILE DATE",
            profile_date.strftime("%d %b %Y"),
            "AVAILABLE",
            "● Observation time"
        )

    with p3:
        metric_card(
            "📍",
            "LOCATION",
            f"{profile_latitude:.1f}°, {profile_longitude:.1f}°",
            "LOCATED",
            "● Latitude / Longitude"
        )

    with p4:
        metric_card(
            "🌊",
            "MAX DEPTH",
            f"{max_depth:.0f} m",
            "PROFILED",
            "● Water column"
        )

    st.write("")
    st.write("")

    section(
        "VERTICAL PROFILE",
        "Temperature & Salinity vs Depth"
    )

    chart1, chart2 = st.columns(2)

    with chart1:

        temperature_profile_fig = go.Figure()

        temperature_profile_fig.add_trace(
            go.Scatter(
                x=selected_profile["Temperature"],
                y=selected_profile["Depth"],
                mode="lines+markers",
                name="Temperature",
                line=dict(
                    color="#35dcff",
                    width=3
                ),
                marker=dict(size=5),
                hovertemplate=(
                    "Temperature: %{x:.2f} °C"
                    "<br>Depth: %{y:.0f} m"
                    "<extra></extra>"
                )
            )
        )

        temperature_profile_fig.update_layout(
            title="Temperature vs Depth",
            xaxis_title="Temperature (°C)",
            yaxis_title="Depth (m)"
        )

        temperature_profile_fig.update_yaxes(
            autorange="reversed"
        )

        style_figure(
            temperature_profile_fig,
            480
        )

        st.plotly_chart(
            temperature_profile_fig,
            use_container_width=True
        )

    with chart2:

        salinity_profile_fig = go.Figure()

        salinity_profile_fig.add_trace(
            go.Scatter(
                x=selected_profile["Salinity"],
                y=selected_profile["Depth"],
                mode="lines+markers",
                name="Salinity",
                line=dict(
                    color="#00e6ad",
                    width=3
                ),
                marker=dict(size=5),
                hovertemplate=(
                    "Salinity: %{x:.3f} PSU"
                    "<br>Depth: %{y:.0f} m"
                    "<extra></extra>"
                )
            )
        )

        salinity_profile_fig.update_layout(
            title="Salinity vs Depth",
            xaxis_title="Salinity (PSU)",
            yaxis_title="Depth (m)"
        )

        salinity_profile_fig.update_yaxes(
            autorange="reversed"
        )

        style_figure(
            salinity_profile_fig,
            480
        )

        st.plotly_chart(
            salinity_profile_fig,
            use_container_width=True
        )

    st.write("")

    section(
        "PROFILE STATISTICS",
        "Quick Summary"
    )

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric(
            "Surface Temperature",
            f"{selected_profile.iloc[0]['Temperature']:.2f} °C"
        )

    with s2:
        st.metric(
            "Deep Temperature",
            f"{selected_profile.iloc[-1]['Temperature']:.2f} °C"
        )

    with s3:
        st.metric(
            "Average Salinity",
            f"{selected_profile['Salinity'].mean():.3f} PSU"
        )

    with s4:
        st.metric(
            "Profile Levels",
            len(selected_profile)
        )

    st.write("")

    with st.expander("View profile observations"):

        st.dataframe(
            selected_profile[
                [
                    "Float_ID",
                    "Cycle",
                    "Date",
                    "Latitude",
                    "Longitude",
                    "Depth",
                    "Temperature",
                    "Salinity"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# OCEAN MAP
# =========================================================

elif page == "🌍 Ocean Map":

    page_header(
        "GLOBAL MONITORING",
        "Ocean Map.",
        "Explore ARGO float locations and inspect "
        "ocean observations spatially."
    )


    m1, m2, m3 = st.columns(3)

    with m1:
        metric_card(
            "📡",
            "FLOATS DISPLAYED",
            str(len(float_data)),
            "ACTIVE",
            "● Monitoring network"
        )

    with m2:

        normal_float_count = (
            float_data["Status"] == "Normal"
        ).sum()

        metric_card(
            "✓",
            "NORMAL",
            str(normal_float_count),
            "STABLE",
            "● Expected observations"
        )

    with m3:

        map_anomalies = (
            float_data["Status"] == "Anomaly"
        ).sum()

        metric_card(
            "⚠️",
            "ANOMALIES",
            str(map_anomalies),
            "ATTENTION",
            "⚠ Review required",
            True
        )


    st.write("")
    st.write("")

    f1, f2 = st.columns(2)

    with f1:

        status_filter = st.selectbox(
            "Float Status",
            [
                "All Floats",
                "Normal",
                "Anomaly"
            ]
        )

    with f2:

        map_parameter = st.selectbox(
            "Map Parameter",
            [
                "Temperature",
                "Salinity",
                "Depth"
            ]
        )


    if status_filter == "All Floats":

        map_data = float_data.copy()

    else:

        map_data = float_data[
            float_data["Status"]
            ==
            status_filter
        ].copy()


    section(
        "SPATIAL INTELLIGENCE",
        "ARGO Float Network"
    )


    if map_parameter == "Temperature":

        color_scale = "Turbo"

    elif map_parameter == "Salinity":

        color_scale = "Viridis"

    else:

        color_scale = "Blues"


    map_fig = px.scatter_geo(
        map_data,

        lat="Latitude",
        lon="Longitude",

        color=map_parameter,

        size="Depth",

        hover_name="Float_ID",

        hover_data={
            "Temperature": True,
            "Salinity": True,
            "Depth": True,
            "Status": True
        },

        color_continuous_scale=color_scale,

        projection="natural earth"
    )


    map_fig.update_geos(
        showland=True,
        landcolor="#071923",

        showocean=True,
        oceancolor="#031827",

        coastlinecolor="#24566a",

        countrycolor="#183d4b",

        showcountries=True,

        bgcolor="rgba(0,0,0,0)"
    )


    map_fig.update_layout(
        height=580,

        margin=dict(
            l=0,
            r=0,
            t=10,
            b=0
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#7d9ba9"
        )
    )


    st.plotly_chart(
        map_fig,
        use_container_width=True
    )


    section(
        "FLOAT INSPECTOR",
        "Inspect Observation"
    )


    selected_float = st.selectbox(
        "Select ARGO Float",
        float_data["Float_ID"]
    )


    selected = float_data[
        float_data["Float_ID"]
        ==
        selected_float
    ].iloc[0]


    i1, i2, i3, i4 = st.columns(4)

    with i1:
        st.metric(
            "Temperature",
            f"{selected['Temperature']} °C"
        )

    with i2:
        st.metric(
            "Salinity",
            f"{selected['Salinity']} PSU"
        )

    with i3:
        st.metric(
            "Depth",
            f"{selected['Depth']} m"
        )

    with i4:
        st.metric(
            "Status",
            selected["Status"]
        )


    st.markdown(
        f"""
        <div class="info-box">

        <div class="panel-title">
        📍 {selected_float}
        </div>

        <div class="panel-text">

        Latitude: {selected['Latitude']}°

        <br>

        Longitude: {selected['Longitude']}°

        <br>

        Current status: {selected['Status']}

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# ANALYTICS
# =========================================================

elif page == "📊 Analytics":

    page_header(
        "DATA ANALYSIS",
        "Ocean Analytics.",
        "Explore distributions, relationships and patterns "
        "inside ARGO ocean observations."
    )

    data = st.session_state.ocean_data

    numeric_columns = data.select_dtypes(
        include=np.number
    ).columns.tolist()


    if len(numeric_columns) == 0:

        st.warning(
            "No numeric columns are available "
            "for analytics."
        )

    else:

        section(
            "EXPLORATION",
            "Visual Analytics"
        )


        parameter = st.selectbox(
            "Select Parameter",
            numeric_columns
        )


        tab1, tab2, tab3 = st.tabs(
            [
                "Distribution",
                "Box Plot",
                "Statistics"
            ]
        )


        with tab1:

            histogram = px.histogram(
                data,
                x=parameter,
                nbins=25
            )

            style_figure(
                histogram,
                400
            )

            st.plotly_chart(
                histogram,
                use_container_width=True
            )


        with tab2:

            box = px.box(
                data,
                y=parameter,
                points="outliers"
            )

            style_figure(
                box,
                400
            )

            st.plotly_chart(
                box,
                use_container_width=True
            )


        with tab3:

            statistics = data[
                numeric_columns
            ].describe().T

            st.dataframe(
                statistics,
                use_container_width=True
            )


        if len(numeric_columns) >= 2:

            st.write("")
            st.write("")

            section(
                "RELATIONSHIPS",
                "Correlation Analysis"
            )


            corr = data[
                numeric_columns
            ].corr()


            heatmap = px.imshow(
                corr,
                text_auto=".2f",
                aspect="auto"
            )


            heatmap.update_layout(
                height=500,
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#7f9cab"
                )
            )


            st.plotly_chart(
                heatmap,
                use_container_width=True
            )


        st.write("")
        st.write("")

        section(
            "DATA QUALITY",
            "Quick Assessment"
        )


        q1, q2, q3 = st.columns(3)


        with q1:

            metric_card(
                "📊",
                "TOTAL RECORDS",
                str(len(data)),
                "LOADED",
                "● Available observations"
            )


        with q2:

            missing_count = int(
                data.isnull().sum().sum()
            )

            metric_card(
                "🔍",
                "MISSING VALUES",
                str(missing_count),
                "CHECKED",
                "● Quality assessment"
            )


        with q3:

            duplicate_count = int(
                data.duplicated().sum()
            )

            metric_card(
                "📑",
                "DUPLICATES",
                str(duplicate_count),
                "CHECKED",
                "● Dataset inspection"
            )
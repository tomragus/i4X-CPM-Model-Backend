import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="CPM S-Curve Generator", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@400;600&display=swap');

:root {
    color-scheme: light only;
}
html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
    font-size: 18px;
    color: #0D1B2A;
}
.stApp {
    background-color: #FFFFFF;
}
[data-testid="stSidebar"] {
    background-color: #EEF2F7;
}
h1 {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 42px !important;
    color: #0D1B2A;
    letter-spacing: 0.02em;
}
[data-testid="stSidebar"] h1 {
    font-size: 24px !important;
    border-bottom: 3px solid #F5C518;
    padding-bottom: 8px;
    margin-bottom: 16px;
}
label, .stRadio label p, .stNumberInput label, .stTextInput label,
.stFileUploader label {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #0D1B2A !important;
}
input[type="number"], input[type="text"] {
    font-family: 'Barlow', sans-serif !important;
    font-size: 18px !important;
}
.stRadio div[role="radiogroup"] label {
    font-size: 18px !important;
}
.stButton > button {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    background-color: #F5C518 !important;
    color: #0D1B2A !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 10px 0 !important;
    letter-spacing: 0.05em;
}
.stButton > button:hover {
    background-color: #17C3B2 !important;
    color: #FFFFFF !important;
}
[data-testid="stMetric"] {
    background-color: #EEF2F7;
    border-left: 5px solid #17C3B2;
    border-radius: 6px;
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] p {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #0D1B2A !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    color: #17C3B2 !important;
}
[data-testid="stInfo"] {
    font-family: 'Barlow', sans-serif !important;
    font-size: 18px !important;
    border-left: 5px solid #17C3B2 !important;
    background-color: #EEF2F7 !important;
    color: #0D1B2A !important;
}
[data-testid="stAlert"] {
    font-size: 18px !important;
    font-family: 'Barlow', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

CONSTANTS = {
    "Total": {
        "mean_sq_ft": 86243.0147,
        "median_budget_per_sqft": 297.9594,
        "models": {
            "duration": "trained_models/Duration_Months_model_v2.joblib",
            "k":        "trained_models/S_Curve_k_model_v2.joblib",
            "t0":       "trained_models/S_Curve_t0_model_v2.joblib",
        },
    },
    "PM Fees and Overhead": {
        "mean_sq_ft": 86068.1878,
        "median_budget_per_sqft": 12.4897,
        "models": {
            "duration": "trained_models/Duration_Months_model_l6_v1.joblib",
            "k":        "trained_models/S_Curve_k_model_l6_v1.joblib",
            "t0":       "trained_models/S_Curve_t0_model_l6_v1.joblib",
        },
    },
}

FEATURES = [
    "Gross Sq Footage", "Projected Budget", "Projected Commitments",
    "Estimate at Completion", "EAC_Budget_Ratio", "Commitments_Budget_Ratio",
    "Budget_per_SqFt", "Log_Projected_Budget", "Log_Gross_SqFt",
]


@st.cache_resource
def load_models(mode):
    cfg = CONSTANTS[mode]["models"]
    return (
        joblib.load(cfg["duration"]),
        joblib.load(cfg["k"]),
        joblib.load(cfg["t0"]),
    )


def clean_and_filter(df, mode):
    df_cleaned = df.iloc[:, 1:].copy()
    if len(df_cleaned) > 0:
        df_cleaned.iat[-1, 0] = "Total"
        start_col_idx = 6
        if df_cleaned.shape[1] > start_col_idx:
            last_row = df_cleaned.iloc[[-1], start_col_idx:]
            cleaned_last_row = (
                last_row.astype("string")
                .apply(lambda s: s.str.split(r"\r\n|\n|\r", regex=True).str[0])
            )
            df_cleaned.iloc[-1, start_col_idx:] = cleaned_last_row.iloc[0].to_numpy()
    df_cleaned = df_cleaned.reset_index(drop=True)
    df = df_cleaned

    if mode == "Total":
        filtered = df[df.iloc[:, 0].astype(str).eq("Total")].copy()
    else:
        filtered = df[df["Line Item"].astype(str).str.lstrip("0").eq("6")].copy()

    filtered = filtered.drop(columns=["Line Item", "Description"])
    return filtered.reset_index(drop=True)


def engineer_features(df, gross_sq_ft, mode, project_code):
    cfg = CONSTANTS[mode]

    df.insert(0, "Project Code", project_code)
    df.insert(1, "Gross Sq Footage", gross_sq_ft)

    df = df.drop(columns=["Actuals To Date", "Actuals + Projections"], errors="ignore")

    _eac = "Estimate at Completion"
    if _eac in df.columns:
        _i = list(df.columns).index(_eac)
        df = df.iloc[:, : _i + 1]

    df[["Gross Sq Footage", "Projected Budget", "Projected Commitments", "Estimate at Completion"]] = (
        df[["Gross Sq Footage", "Projected Budget", "Projected Commitments", "Estimate at Completion"]]
        .replace({"[$,]": ""}, regex=True)
        .astype(float)
    )

    df["EAC_Budget_Ratio"] = df["Estimate at Completion"] / df["Projected Budget"].replace(0, np.nan)
    df["Commitments_Budget_Ratio"] = df["Projected Commitments"] / df["Projected Budget"].replace(0, np.nan)

    df["Gross Sq Footage"] = df["Gross Sq Footage"].fillna(cfg["mean_sq_ft"])
    df["Budget_per_SqFt"] = df["Projected Budget"] / df["Gross Sq Footage"].replace(0, np.nan)
    df["Budget_per_SqFt"] = df["Budget_per_SqFt"].fillna(cfg["median_budget_per_sqft"])
    df["Log_Projected_Budget"] = np.log1p(df["Projected Budget"])
    df["Log_Gross_SqFt"] = np.log1p(df["Gross Sq Footage"])

    return df


def build_features_from_raw(gross_sq_ft, budget, commitments, eac, mode, project_code):
    cfg = CONSTANTS[mode]
    sq = gross_sq_ft if gross_sq_ft > 0 else cfg["mean_sq_ft"]
    bps = budget / sq if sq > 0 else cfg["median_budget_per_sqft"]
    return pd.DataFrame([{
        "Project Code":             project_code,
        "Gross Sq Footage":         sq,
        "Projected Budget":         budget,
        "Projected Commitments":    commitments,
        "Estimate at Completion":   eac,
        "EAC_Budget_Ratio":         eac / budget if budget != 0 else np.nan,
        "Commitments_Budget_Ratio": commitments / budget if budget != 0 else np.nan,
        "Budget_per_SqFt":          bps,
        "Log_Projected_Budget":     np.log1p(budget),
        "Log_Gross_SqFt":           np.log1p(sq),
    }])


def run_prediction(df, mode):
    duration_model, k_model, t0_model = load_models(mode)

    X = df[FEATURES]
    duration_pred = duration_model.predict(X)[0]
    log_k_pred = k_model.predict(X)[0]
    t0_rel_pred = t0_model.predict(X)[0]

    k_pred = np.exp(log_k_pred)
    t0_pred = t0_rel_pred * duration_pred
    L_pred = float(df["Projected Commitments"].values[0])

    return duration_pred, k_pred, t0_pred, L_pred


def make_figure(duration, k, t0, L, project_code, mode):
    def logistic_curve(t, L, k, t0):
        return L / (1 + np.exp(-k * (t - t0)))

    def fmt(x):
        if x >= 1e6:
            return f"${x * 1e-6:.1f}M"
        elif x >= 1e3:
            return f"${x * 1e-3:.0f}K"
        else:
            return f"${x:,.0f}"

    x_data = np.arange(int(duration))
    y_data = logistic_curve(x_data, L, k, t0)
    hover_labels = [fmt(v) for v in y_data]
    tick_vals = np.linspace(0, y_data.max(), 8)
    tick_text = [fmt(v) for v in tick_vals]

    title = (
        f"Standardized S-Curve: Project {project_code}"
        if mode == "Total"
        else f"Standardized S-Curve (PM Fees & Overhead): Project {project_code}"
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode="lines",
        line=dict(color="#17C3B2", width=3),
        name="Parameterized S-Curve",
        customdata=hover_labels,
        hovertemplate="Month: %{x}<br>Cost: %{customdata}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=14)),
        xaxis=dict(
            title="Months from Project Start",
            dtick=3,
            minor=dict(dtick=1, showgrid=True, gridcolor="#EEEEEE"),
            gridcolor="#CCCCCC",
        ),
        yaxis=dict(
            title="Cumulative Cost",
            tickvals=tick_vals,
            ticktext=tick_text,
            gridcolor="#CCCCCC",
        ),
        legend=dict(x=0.01, y=0.99),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="Barlow Condensed, sans-serif", size=16, color="#0D1B2A"),
        height=400,
    )
    return fig


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Capital Project Cashflow Predictor")
    input_method = st.radio("Input Method", ["CSV Upload", "Manual Entry"])
    mode = st.radio("Curve Type", ["Total", "PM Fees and Overhead"])

    if input_method == "CSV Upload":
        uploaded_file = st.file_uploader("Upload Project CSV", type="csv")
        gross_sq_ft = st.number_input("Gross Sq Footage", min_value=0.0, step=1000.0)
    else:
        project_name = st.text_input("Project Name / Code")
        projected_budget = st.number_input("Projected Budget ($)", min_value=0.0, step=10000.0)
        projected_commitments = st.number_input("Projected Commitments ($)", min_value=0.0, step=10000.0)
        eac = st.number_input("Estimate at Completion ($)", min_value=0.0, step=10000.0)
        gross_sq_ft = st.number_input("Gross Sq Footage", min_value=0.0, step=1000.0)

    generate = st.button("Generate S-Curve", use_container_width=True)

# ── Main area ─────────────────────────────────────────────────────────────────
title_col, logo_col = st.columns([5, 1])
with title_col:
    st.title("Capital Project Cashflow Predictor")
with logo_col:
    st.image("logo.png", width=140)

if generate:
    if input_method == "CSV Upload":
        if uploaded_file is None:
            st.error("Please upload a CSV file.")
        elif gross_sq_ft <= 0:
            st.error("Please enter a valid Gross Sq Footage.")
        else:
            with st.spinner("Running prediction..."):
                project_code = Path(uploaded_file.name).stem
                df_raw = pd.read_csv(uploaded_file, header=0)
                df = clean_and_filter(df_raw, mode)
                df = engineer_features(df, gross_sq_ft, mode, project_code)
                duration, k, t0, L = run_prediction(df, mode)
                fig = make_figure(duration, k, t0, L, project_code, mode)
    else:
        errors = []
        if not project_name.strip():
            errors.append("Please enter a Project Name / Code.")
        if projected_budget <= 0:
            errors.append("Please enter a valid Projected Budget.")
        if projected_commitments <= 0:
            errors.append("Please enter a valid Projected Commitments.")
        if eac <= 0:
            errors.append("Please enter a valid Estimate at Completion.")
        if gross_sq_ft <= 0:
            errors.append("Please enter a valid Gross Sq Footage.")
        for e in errors:
            st.error(e)
        if not errors:
            with st.spinner("Running prediction..."):
                df = build_features_from_raw(
                    gross_sq_ft, projected_budget, projected_commitments,
                    eac, mode, project_name.strip()
                )
                duration, k, t0, L = run_prediction(df, mode)
                fig = make_figure(duration, k, t0, L, project_name.strip(), mode)

    if "fig" in locals():
        st.plotly_chart(fig, use_container_width=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Duration", f"{duration:.1f} months")
        col2.metric("Growth Rate (k)", f"{k:.4f}")
        col3.metric("Midpoint (t₀)", f"{t0:.1f} months")
else:
    st.info("This tool predicts how capital project spending will unfold over time. Input your project's parameters and generate a cash flow S-curve to support planning and budget forecasting.")

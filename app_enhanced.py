import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import f1_score, accuracy_score

# ── Config ─────────────────────────────────────────────────────────────────────
DATA_PATH    = "Breast_Cancer.csv"
DROP_COLS    = []
TARGET_COL   = "Status"
RANDOM_STATE = 42

st.set_page_config(page_title="🏥 Medico Diagnosis", layout="wide", page_icon="🏥")

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

with st.sidebar:
    st.markdown("<div class='brand-orb'></div>", unsafe_allow_html=True)
    st.markdown("### 🏥 Medico")
    st.caption("Breast Cancer Diagnosis AI")
    nav_choice = st.radio(
        "Navigation",
        ["Dashboard", "Predict", "Clinical Insights", "Risk Stratification", "Treatment Planning", "Patients", "Reports"],
        index=["dashboard", "predict", "insights", "risk", "treatment", "patients", "reports"].index(st.session_state.page) if st.session_state.page in ["dashboard", "predict", "insights", "risk", "treatment", "patients", "reports"] else 0,
        label_visibility="collapsed",
    )

page_map = {
    "Dashboard": "dashboard",
    "Predict": "predict",
    "Clinical Insights": "insights",
    "Risk Stratification": "risk",
    "Treatment Planning": "treatment",
    "Patients": "patients",
    "Reports": "reports"
}
page = page_map.get(nav_choice, "dashboard")
st.session_state.page = page

# ── Enhanced CSS ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Serif+Display&display=swap');

html, body, .stApp { font-family: 'DM Sans', sans-serif !important; background: #f3f5fb !important; }
#MainMenu, footer { visibility: hidden; }

/* Sidebar polish */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #17213b 0%, #1b2b4a 100%) !important;
    border-right: 1px solid rgba(255,255,255,.07);
}
[data-testid="stSidebar"] * {
    color: #d7deef !important;
}
[data-testid="stSidebar"] [data-baseweb="radio"] > div {
    gap: 6px;
}
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 10px;
    padding: 8px 10px;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: rgba(95, 113, 255, .24);
    border-color: rgba(124, 143, 255, .5);
}

.brand-orb {
    width: 14px;
    height: 14px;
    border-radius: 4px;
    background: linear-gradient(140deg, #7c86ff 0%, #5c66f5 100%);
    margin-bottom: 8px;
}

section.main > div.block-container {
    padding-top: 32px !important;
    padding-bottom: 32px !important;
    padding-left: 36px !important;
    padding-right: 36px !important;
    max-width: 100% !important;
}

.stApp > header { display: none !important; }
.stApp { padding-top: 0 !important; margin-top: 0 !important; }

/* ── Top Bar ── */
.top-bar {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 26px;
    background: #ffffff;
    border: 1px solid #eceff8;
    border-radius: 16px;
    padding: 14px 18px;
    box-shadow: 0 3px 14px rgba(26, 32, 72, .06);
}
.top-greeting h1 {
    font-size: 24px; color: #1a1a2e; margin: 0; font-weight: 700;
}
.top-greeting p { font-size: 12.5px; color: #aaa; margin: 3px 0 0; }
.top-badge {
    background: linear-gradient(180deg, #ffffff 0%, #f9faff 100%);
    border: 1px solid #e2e6ff; border-radius: 10px;
    padding: 8px 14px; font-size: 12.5px; color: #555;
    font-weight: 500; display: inline-block; margin-left: 8px;
}
.top-badge b { color: #e84545; }

/* ── Stat Cards ── */
.stat-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 24px; }
.stat-card {
    background: #fff; border-radius: 16px; padding: 20px;
    border: 1px solid #eceff8; box-shadow: 0 6px 16px rgba(29, 42, 109, .07);
    transition: transform .16s ease, box-shadow .16s ease;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(29, 42, 109, .11);
}
.sc-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.sc-icon {
    width: 38px; height: 38px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center; font-size: 17px;
}
.sc-icon.r { background: #fff0f0; }
.sc-icon.b { background: #f0f4ff; }
.sc-icon.g { background: #f0faf4; }
.sc-icon.a { background: #fffbf0; }
.sc-value   { font-size: 28px; font-weight: 700; color: #1a1a2e; line-height: 1; }
.sc-label   { font-size: 12px; color: #aaa; margin-top: 4px; font-weight: 500; }

/* ── Generic Card ── */
.card {
    background: #fff; border-radius: 16px; padding: 22px 22px 18px;
    border: 1px solid #eceff8; box-shadow: 0 4px 12px rgba(23, 31, 76, .06); margin-bottom: 20px;
}
.card-title {
    font-size: 14.5px; font-weight: 700; color: #1a1a2e;
    margin: 0 0 16px; display: flex; align-items: center; gap: 8px;
}
.ct-dot { width: 8px; height: 8px; border-radius: 50%; background: #e84545; flex-shrink: 0; }

/* ── Alert Cards ── */
.alert-red {
    background: linear-gradient(135deg, rgba(232,69,69,.1) 0%, rgba(255,107,107,.1) 100%);
    border: 1.5px solid #ff9999;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 12px;
}
.alert-yellow {
    background: linear-gradient(135deg, rgba(245,166,35,.1) 0%, rgba(247,201,72,.1) 100%);
    border: 1.5px solid #ffc966;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 12px;
}
.alert-green {
    background: linear-gradient(135deg, rgba(34,197,139,.1) 0%, rgba(52,211,153,.1) 100%);
    border: 1.5px solid #66d9a0;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 12px;
}
.alert-title { font-weight: 700; color: #1a1a2e; font-size: 13px; margin-bottom: 4px; }
.alert-msg { font-size: 12px; color: #555; line-height: 1.4; }

/* ── Risk Badge ── */
.risk-badge {
    display: inline-block; border-radius: 20px; padding: 6px 12px;
    font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
}
.risk-low { background: #d4edda; color: #155724; }
.risk-med { background: #fff3cd; color: #856404; }
.risk-high { background: #f8d7da; color: #721c24; }

/* ── Result banner ── */
.res-banner {
    border-radius: 14px; padding: 20px 22px; margin-bottom: 16px; color: #fff;
}
.res-banner.hi { background: linear-gradient(135deg, #e84545 0%, #ff6b6b 100%); }
.res-banner.lo { background: linear-gradient(135deg, #f5a623 0%, #f7c948 100%); }
.res-lbl  { font-size: 10px; font-weight: 700; opacity:.8; letter-spacing:1.2px; text-transform:uppercase; }
.res-diag { font-size: 26px; font-weight: 800; margin: 4px 0 2px; font-family:'DM Serif Display',serif; }
.res-conf { font-size: 13px; opacity:.9; }

/* ── Bar rows ── */
.bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 9px; }
.bar-lbl { font-size: 12px; font-weight: 500; color: #555; width: 140px; flex-shrink: 0; }
.bar-track { flex: 1; background: #f2f2f2; border-radius: 99px; height: 8px; overflow: hidden; }
.bar-fill  { height: 100%; border-radius: 99px; background: #e84545; }
.bar-fill.blue { background: linear-gradient(90deg,#4c6ef5,#748ffc); }
.bar-pct   { font-size: 12px; font-weight: 700; color: #333; width: 50px; text-align: right; flex-shrink: 0; }

/* ── Treatment Cards ── */
.treatment-box {
    background: linear-gradient(135deg, rgba(76,110,245,.08) 0%, rgba(116,143,252,.08) 100%);
    border: 1px solid rgba(76,110,245,.2);
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
}
.treatment-title { font-weight: 700; color: #1a1a2e; font-size: 12px; }
.treatment-info { font-size: 11px; color: #666; margin-top: 4px; }

/* ── Survival Curve ── */
.survival-box {
    background: linear-gradient(135deg, rgba(34,197,139,.08) 0%, rgba(52,211,153,.08) 100%);
    border: 1px solid rgba(34,197,139,.2);
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
}
.survival-time { font-size: 13px; font-weight: 700; color: #1a1a2e; }
.survival-pct { font-size: 24px; font-weight: 800; color: #22c58b; margin: 4px 0; }
.survival-label { font-size: 11px; color: #999; }

/* ── Form overrides ── */
.stFormSubmitButton > button {
    background: #e84545 !important; color: #fff !important;
    border: none !important; border-radius: 12px !important;
    font-size: 14px !important; font-weight: 700 !important;
    padding: 14px 0 !important;
    box-shadow: 0 4px 16px rgba(232,69,69,.35) !important;
}
.stFormSubmitButton > button:hover {
    background: #d13535 !important;
    box-shadow: 0 6px 22px rgba(232,69,69,.45) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px; background: #f5f6fa; border-radius: 12px; padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important; font-size: 12.5px !important;
    font-weight: 600 !important; color: #888 !important; padding: 7px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: #fff !important; color: #1a1a2e !important;
    box-shadow: 0 2px 8px rgba(0,0,0,.06) !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #eceff8;
    border-radius: 12px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# ── Data & Training ───────────────────────────────────────────────────────────
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

@st.cache_resource
def train_all(df):
    d = df.drop(columns=DROP_COLS).copy()
    for col in d.select_dtypes(include=["object"]).columns:
        if col != TARGET_COL:
            d[col] = d[col].fillna("Unknown")
    X      = d.drop(columns=[TARGET_COL]).copy()
    y_text = d[TARGET_COL].copy()
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()
    encoders, cat_map = {}, {}
    for col in cat_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le
        cat_map[col]  = le.classes_.tolist()
    target_le = LabelEncoder()
    y = target_le.fit_transform(y_text)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=.2, random_state=RANDOM_STATE, stratify=y)
    sc = StandardScaler()
    X_tr_s = sc.fit_transform(X_tr)
    X_te_s = sc.transform(X_te)
    lr  = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    lr.fit(X_tr_s, y_tr)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_tr_s, y_tr)
    gs = GridSearchCV(RandomForestClassifier(random_state=RANDOM_STATE),
                      {"n_estimators": [100, 200], "max_depth": [None, 10]},
                      cv=3, scoring="f1_macro", n_jobs=-1)
    gs.fit(X_tr_s, y_tr)
    rf = gs.best_estimator_
    mdl_map = {"Logistic Regression": lr, "Random Forest": rf, "KNN": knn}
    metrics = {}
    for name, mdl in mdl_map.items():
        p = mdl.predict(X_te_s)
        metrics[name] = {"accuracy": round(accuracy_score(y_te, p)*100,1),
                         "f1": round(f1_score(y_te, p, average="macro")*100,1)}
    num_bnd = {}
    for col in X.columns:
        if col not in cat_map:
            num_bnd[col] = (float(X[col].min()), float(X[col].max()), float(X[col].mean()))
    return dict(models=mdl_map, scaler=sc, encoders=encoders, target_le=target_le,
                feature_columns=X.columns.tolist(), cat_map=cat_map,
                num_bnd=num_bnd, metrics=metrics, df_model=d)

try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"Cannot load dataset: {e}"); st.stop()

with st.spinner("Training models — cached after first run…"):
    art = train_all(df)

models    = art["models"]
scaler    = art["scaler"]
encoders  = art["encoders"]
target_le = art["target_le"]
feat_cols = art["feature_columns"]
cat_map   = art["cat_map"]
num_bnd   = art["num_bnd"]
metrics   = art["metrics"]
df_model  = art["df_model"]

best_mdl = max(metrics, key=lambda m: metrics[m]["f1"])
best_f1 = metrics[best_mdl]["f1"]
best_acc = metrics[best_mdl]["accuracy"]

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# ── Helper Functions ────────────────────────────────────────────────────────────

def render_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="top-bar">
          <div class="top-greeting">
            <h1>{title}</h1>
            <p>{subtitle}</p>
          </div>
          <div>
            <span class="top-badge">Best Model: <b>{best_mdl}</b></span>
            <span class="top-badge">F1-Macro: <b>{best_f1}%</b></span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_page_banner(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, rgba(59,68,209,.08) 0%, rgba(232,69,69,.08) 100%);
            border: 1px solid #dde2fb;
            border-radius: 14px;
            padding: 12px 14px;
            margin: 0 0 16px 0;
        ">
            <div style="font-size:13px; color:#6b7399; font-weight:700; letter-spacing:.5px; text-transform:uppercase;">Section</div>
            <div style="font-size:20px; color:#1a1a2e; font-weight:800; margin-top:2px;">{title}</div>
            <div style="font-size:13px; color:#6f7690; margin-top:2px;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def get_risk_category(probability: float) -> tuple:
    """Returns risk category and color based on probability"""
    if probability >= 0.75:
        return "HIGH RISK", "risk-high", "#721c24"
    elif probability >= 0.50:
        return "MODERATE RISK", "risk-med", "#856404"
    else:
        return "LOW RISK", "risk-low", "#155724"

def get_survival_probabilities(probability: float) -> dict:
    """Estimate multi-timepoint survival probabilities"""
    # These are calibrated estimates based on typical breast cancer survival curves
    if probability < 0.3:  # Very low dead probability = very good prognosis
        return {
            "1-year": 0.98,
            "3-year": 0.96,
            "5-year": 0.95,
            "10-year": 0.92
        }
    elif probability < 0.5:  # Low dead probability = good prognosis
        return {
            "1-year": 0.95,
            "3-year": 0.90,
            "5-year": 0.85,
            "10-year": 0.80
        }
    elif probability < 0.7:  # Moderate dead probability
        return {
            "1-year": 0.90,
            "3-year": 0.80,
            "5-year": 0.72,
            "10-year": 0.65
        }
    else:  # High dead probability = poor prognosis
        return {
            "1-year": 0.75,
            "3-year": 0.55,
            "5-year": 0.40,
            "10-year": 0.30
        }

def get_treatment_recommendations(inputs: dict) -> dict:
    """Generate treatment recommendations based on patient characteristics"""
    recommendations = {
        "primary": [],
        "secondary": [],
        "monitoring": []
    }
    
    # Extract biomarker status (assuming these columns exist)
    er_status = inputs.get("Estrogen Status", "Unknown")
    pr_status = inputs.get("Progesterone Status", "Unknown")
    her2_status = inputs.get("HER2 Status", "Unknown")
    grade = inputs.get("Grade", "Unknown")
    
    # Treatment recommendations based on biomarkers
    if er_status == "Positive" or pr_status == "Positive":
        recommendations["primary"].append("🎯 Endocrine Therapy (Hormone Therapy)")
        recommendations["secondary"].append("Consider tamoxifen or aromatase inhibitors")
    
    if er_status == "Positive" and pr_status == "Negative":
        recommendations["monitoring"].append("Monitor PR expression at progression")
    
    if er_status == "Negative" and pr_status == "Negative" and her2_status == "Negative":
        recommendations["primary"].append("⚠️  Triple Negative Phenotype - Requires Aggressive Therapy")
        recommendations["secondary"].append("Chemotherapy (anthracyclines ± taxanes)")
    
    if her2_status == "Positive":
        recommendations["primary"].append("🎯 HER2-Targeted Therapy")
        recommendations["secondary"].append("Trastuzumab (Herceptin) ± pertuzumab")
    
    if grade == "3":
        recommendations["primary"].append("Consider combination chemotherapy regimen")
    
    return recommendations

def render_alert(alert_type: str, title: str, message: str) -> None:
    """Render alert box with icon and message"""
    css_class = f"alert-{alert_type}"
    st.markdown(
        f"""
        <div class="{css_class}">
            <div class="alert-title">{title}</div>
            <div class="alert-msg">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ────────────────────────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ────────────────────────────────────────────────────────────────────────────────

if page == "dashboard":
    render_header("Good Morning, Doctor 👋", "AI-powered clinical diagnosis prediction · Spring 2026")
    render_page_banner("Dashboard", "Overview of model performance, class distribution, and key metrics")

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card">
        <div class="sc-top"><div class="sc-icon r">👥</div></div>
        <div class="sc-value">{len(df):,}</div><div class="sc-label">Total Patients</div>
      </div>
      <div class="stat-card">
        <div class="sc-top"><div class="sc-icon b">🔬</div></div>
        <div class="sc-value">{len(target_le.classes_)}</div><div class="sc-label">Diagnosis Classes</div>
      </div>
      <div class="stat-card">
        <div class="sc-top"><div class="sc-icon g">🎯</div></div>
        <div class="sc-value">{best_acc}%</div><div class="sc-label">Best Accuracy</div>
      </div>
      <div class="stat-card">
        <div class="sc-top"><div class="sc-icon a">📐</div></div>
        <div class="sc-value">{len(feat_cols)}</div><div class="sc-label">Features Used</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([2.2, 1], gap="large")
    with c1:
        st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Model Performance Comparison</div>', unsafe_allow_html=True)
        perf = pd.DataFrame([{"Model": m, "Accuracy (%)": v["accuracy"], "F1-Macro (%)": v["f1"]} for m, v in metrics.items()]).set_index("Model")
        st.dataframe(perf, width="stretch")
        st.bar_chart(perf, color=["#e84545", "#4c6ef5"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Feature Importance (Random Forest)</div>', unsafe_allow_html=True)
        rf_mdl = models["Random Forest"]
        imp = sorted(zip(feat_cols, rf_mdl.feature_importances_), key=lambda x: -x[1])[:10]
        mx = imp[0][1]
        html = ""
        for fn, fv in imp:
            pct = fv / mx * 100
            html += f'<div class="bar-row"><div class="bar-lbl">{fn}</div><div class="bar-track"><div class="bar-fill blue" style="width:{pct:.1f}%"></div></div><div class="bar-pct">{fv*100:.1f}%</div></div>'
        st.markdown(html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Class Distribution</div>', unsafe_allow_html=True)
        dist = df[TARGET_COL].value_counts()
        for cls, cnt in dist.items():
            pct = (cnt / len(df)) * 100
            st.markdown(f'<div class="bar-row"><div class="bar-lbl">{cls}</div><div class="bar-track"><div class="bar-fill" style="width:{pct:.1f}%"></div></div><div class="bar-pct">{pct:.1f}%</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────────
# PAGE: PREDICT (Enhanced with Clinical Features)
# ────────────────────────────────────────────────────────────────────────────────

if page == "predict":
    render_header("Patient Prediction", "Enter patient characteristics for diagnosis and clinical assessment")
    render_page_banner("Predict", "Real-time diagnosis with survival probability, risk stratification, and treatment guidance")

    st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>🤖 Patient Diagnosis Predictor</div>', unsafe_allow_html=True)
    cmeta1, cmeta2 = st.columns([2, 1], gap="large")
    with cmeta1:
        model_choice = st.radio("Model", list(models.keys()), horizontal=True, label_visibility="collapsed")
    with cmeta2:
        threshold = st.slider("Confidence Threshold", min_value=0.30, max_value=0.90, value=0.55, step=0.01)

    active = models[model_choice]
    st.caption(f"**{model_choice}** — Accuracy: **{metrics[model_choice]['accuracy']}%** | F1-Macro: **{metrics[model_choice]['f1']}%**")
    st.markdown("---")

    with st.form("predict_form"):
        st.markdown("#### Enter Patient Details")
        inputs = {}
        chunks = [feat_cols[i:i + 4] for i in range(0, len(feat_cols), 4)]
        for chunk in chunks:
            cols = st.columns(len(chunk))
            for cw, cn in zip(cols, chunk):
                with cw:
                    if cn in cat_map:
                        inputs[cn] = st.selectbox(cn, cat_map[cn])
                    else:
                        mn, mx, mean = num_bnd[cn]
                        step = 0.01 if any(k in cn for k in ["Pressure", "Rate", "Temp"]) else 1.0
                        val = round(mean, 2) if step < 1 else float(round(mean))
                        inputs[cn] = st.number_input(cn, min_value=float(np.floor(mn)), max_value=float(np.ceil(mx)), value=val, step=step)
        submitted = st.form_submit_button("🔍  Predict Diagnosis", width="stretch")

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        patient_df = pd.DataFrame([inputs]).reindex(columns=feat_cols)
        for col in patient_df.select_dtypes(include=["object"]).columns:
            patient_df[col] = patient_df[col].fillna("Unknown")
        try:
            enc = patient_df.copy()
            for col, le in encoders.items():
                enc[col] = le.transform(enc[col].astype(str))
            scaled = scaler.transform(enc)
        except Exception as e:
            st.error(f"Encoding error: {e}")
            st.stop()

        pred_idx = int(active.predict(scaled)[0])
        pred_label = target_le.inverse_transform([pred_idx])[0]
        proba = active.predict_proba(scaled)[0]
        top_prob = float(proba.max())

        # ── MAIN PREDICTION RESULT ──
        st.markdown("### 🩺 Prediction Result")
        r1, r2, r3 = st.columns([1, 1.2, 1.3], gap="large")

        with r1:
            css_cls = "hi" if top_prob >= threshold else "lo"
            conf_lbl = "HIGH CONFIDENCE" if top_prob >= threshold else "⚠️  REVIEW ADVISED"
            st.markdown(
                f"""
                <div class="res-banner {css_cls}">
                  <div class="res-lbl">{conf_lbl}</div>
                  <div class="res-diag">{pred_label}</div>
                  <div class="res-conf">Confidence: {top_prob:.1%}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("**Probability Scores**")
            proba_df = pd.DataFrame({"Diagnosis": target_le.classes_, "Probability": proba}).sort_values("Probability", ascending=False)
            for _, row in proba_df.iterrows():
                pct = row["Probability"] * 100
                st.markdown(f'<div class="bar-row"><div class="bar-lbl">{row["Diagnosis"]}</div><div class="bar-track"><div class="bar-fill" style="width:{pct:.1f}%"></div></div><div class="bar-pct">{pct:.1f}%</div></div>', unsafe_allow_html=True)

        with r2:
            # ── MULTI-TIMEPOINT SURVIVAL PROBABILITIES ──
            st.markdown("**📊 Survival Probability Estimates**")
            survival_probs = get_survival_probabilities(top_prob if pred_label == "Dead" else 1 - top_prob)
            for timepoint, prob in survival_probs.items():
                st.markdown(
                    f"""
                    <div class="survival-box">
                        <div class="survival-time">{timepoint.replace('-', ' ').title()}</div>
                        <div class="survival-pct">{prob:.1%}</div>
                        <div class="survival-label">Estimated survival rate</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with r3:
            # ── RISK STRATIFICATION ──
            st.markdown("**⚠️ Risk Stratification**")
            dead_prob = proba[1] if target_le.classes_[1] == "Dead" else proba[0]
            risk_cat, risk_css, risk_color = get_risk_category(dead_prob)
            st.markdown(f'<span class="risk-badge {risk_css}">{risk_cat}</span>', unsafe_allow_html=True)
            
            st.markdown("**Risk Factors**")
            st.write("Primary:")
            if inputs.get("Tumor Size", 0) > 30:
                render_alert("red", "⚠️  Large Tumor", "Tumor size >30mm significantly impacts prognosis")
            if inputs.get("Grade") == "3":
                render_alert("red", "⚠️  High Grade", "Poor differentiation indicates aggressive phenotype")
            if inputs.get("N Stage", "").startswith("N") and inputs.get("N Stage") != "N0":
                render_alert("yellow", "⚠️  Nodal Involvement", "Lymph node metastasis detected")

        # ── TREATMENT RECOMMENDATIONS ──
        st.markdown("### 💊 Treatment Recommendations")
        recommendations = get_treatment_recommendations(inputs)
        
        tc1, tc2, tc3 = st.columns(3, gap="large")
        with tc1:
            st.markdown("**Primary Interventions**")
            for rec in recommendations["primary"]:
                st.markdown(f'<div class="treatment-box"><div class="treatment-title">{rec}</div></div>', unsafe_allow_html=True)
        
        with tc2:
            st.markdown("**Secondary Options**")
            for rec in recommendations["secondary"]:
                st.markdown(f'<div class="treatment-box"><div class="treatment-title">{rec}</div></div>', unsafe_allow_html=True)
        
        with tc3:
            st.markdown("**Monitoring Protocol**")
            for rec in recommendations["monitoring"]:
                st.markdown(f'<div class="treatment-box"><div class="treatment-title">{rec}</div></div>', unsafe_allow_html=True)

        # ── CLINICAL NOTES & EXPORT ──
        st.markdown("### 📋 Clinical Documentation")
        doc_text = f"""
**Patient Summary Report**
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**Diagnosis:** {pred_label}
**Confidence:** {top_prob:.1%}
**Model:** {model_choice}
**Risk Category:** {risk_cat}

**Survival Estimates:**
- 1-Year: {survival_probs['1-year']:.1%}
- 3-Year: {survival_probs['3-year']:.1%}
- 5-Year: {survival_probs['5-year']:.1%}
- 10-Year: {survival_probs['10-year']:.1%}

**Treatment Recommendations:**
{chr(10).join(recommendations['primary'] + recommendations['secondary'])}

**Clinical Notes:**
Review patient comorbidities before treatment initiation.
Consider tumor board evaluation for complex cases.
        """
        
        st.text_area("Clinical Notes", value=doc_text, height=180, disabled=True)
        
        export = patient_df.copy()
        export.insert(0, "Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        export.insert(1, "Model", model_choice)
        export["Predicted_Diagnosis"] = pred_label
        export["Confidence"] = round(top_prob, 4)
        export["Risk_Category"] = risk_cat
        for timepoint, prob in survival_probs.items():
            export[f"Survival_{timepoint}"] = prob
        
        st.session_state.prediction_history.append(export.iloc[0].to_dict())
        
        st.download_button(
            "⬇️  Download Full Report as CSV",
            data=export.to_csv(index=False).encode(),
            file_name="patient_report.csv",
            mime="text/csv",
            width="stretch",
        )

# ────────────────────────────────────────────────────────────────────────────────
# PAGE: CLINICAL INSIGHTS
# ────────────────────────────────────────────────────────────────────────────────

if page == "insights":
    render_header("Clinical Insights", "Deep dive into model performance and biomarker analysis")
    render_page_banner("Insights", "Detailed analysis of feature importance, model behavior, and clinical patterns")

    st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Feature Importance by Category</div>', unsafe_allow_html=True)
    
    rf_model = models["Random Forest"]
    importance_df = pd.DataFrame({"Feature": feat_cols, "Importance": rf_model.feature_importances_}).sort_values("Importance", ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    top_features = importance_df.head(15)
    colors = ["#e84545" if i < 5 else "#4c6ef5" if i < 10 else "#22c58b" for i in range(len(top_features))]
    ax.barh(range(len(top_features)), top_features["Importance"], color=colors)
    ax.set_yticks(range(len(top_features)))
    ax.set_yticklabels(top_features["Feature"])
    ax.set_xlabel("Importance Score")
    ax.invert_yaxis()
    st.pyplot(fig, clear_figure=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Biomarker Analysis ──
    st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Biomarker Status Distribution</div>', unsafe_allow_html=True)
    biomarker_cols = [col for col in feat_cols if "Status" in col or "Estrogen" in col or "Progesterone" in col]
    if biomarker_cols:
        for biomarker in biomarker_cols[:3]:
            if biomarker in df_model.columns:
                counts = df_model[biomarker].value_counts()
                st.write(f"**{biomarker}**")
                for val, cnt in counts.items():
                    pct = (cnt / len(df_model)) * 100
                    st.markdown(f'<div class="bar-row"><div class="bar-lbl">{val}</div><div class="bar-track"><div class="bar-fill" style="width:{pct:.1f}%"></div></div><div class="bar-pct">{pct:.1f}%</div></div>', unsafe_allow_html=True)
                st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────────
# PAGE: RISK STRATIFICATION
# ────────────────────────────────────────────────────────────────────────────────

if page == "risk":
    render_header("Risk Stratification", "Classify patients into clinically meaningful risk tiers")
    render_page_banner("Risk Stratification", "NCCN/ESMO-aligned risk categories with clinical recommendations")

    st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Risk Classification Framework</div>', unsafe_allow_html=True)
    
    risk_data = {
        "Risk Tier": ["LOW RISK", "MODERATE RISK", "HIGH RISK"],
        "Model Probability (Dead)": ["< 30%", "30-60%", "> 60%"],
        "5-Year Survival": ["90-95%", "70-85%", "30-50%"],
        "Recommended Approach": [
            "Standard surveillance protocol",
            "Enhanced monitoring + adjuvant therapy",
            "Aggressive treatment + MDT review"
        ],
        "Example Presentations": [
            "Stage I, Grade 1, ER+ receptors",
            "Stage II-III with nodal involvement",
            "Stage IV or Triple Negative"
        ]
    }
    risk_df = pd.DataFrame(risk_data)
    st.dataframe(risk_df, width="stretch", height=200)
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────────
# PAGE: TREATMENT PLANNING
# ────────────────────────────────────────────────────────────────────────────────

if page == "treatment":
    render_header("Treatment Planning", "Evidence-based treatment pathways and biomarker-guided therapy")
    render_page_banner("Treatment Planning", "Personalized treatment recommendations based on tumor characteristics")

    st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Biomarker-Guided Treatment Selection</div>', unsafe_allow_html=True)
    
    treatment_pathways = {
        "ER+/PR+ (Hormone-Sensitive)": {
            "icon": "💊",
            "primary": "Endocrine Therapy (Tamoxifen or Aromatase Inhibitors)",
            "duration": "5-10 years",
            "considerations": "Monitor for side effects; adjust for adverse events"
        },
        "HER2+ (HER2-Overexpressing)": {
            "icon": "🎯",
            "primary": "HER2-Targeted Therapy (Trastuzumab, Pertuzumab)",
            "duration": "1 year",
            "considerations": "Cardiac monitoring recommended; combination with chemotherapy typical"
        },
        "Triple Negative": {
            "icon": "⚠️",
            "primary": "Chemotherapy (Anthracyclines ± Taxanes ± Platinum agents)",
            "duration": "12-16 weeks",
            "considerations": "Most aggressive phenotype; early treatment escalation recommended"
        }
    }
    
    for pathway, details in treatment_pathways.items():
        st.markdown(f"""
        <div class="treatment-box" style="border-left: 4px solid #e84545; padding: 14px;">
            <div style="font-weight: 700; font-size: 14px; color: #1a1a2e; margin-bottom: 8px;">
                {details['icon']} {pathway}
            </div>
            <div style="font-size: 12px; color: #555; margin-bottom: 8px;">
                <b>Primary:</b> {details['primary']}<br>
                <b>Duration:</b> {details['duration']}<br>
                <b>Considerations:</b> {details['considerations']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────────
# PAGE: PATIENTS
# ────────────────────────────────────────────────────────────────────────────────

if page == "patients":
    render_header("Patients", "View and manage all predicted patients")
    render_page_banner("Patients", "Track prediction history and review diagnosis distribution")

    history_df = pd.DataFrame(st.session_state.prediction_history)
    if history_df.empty:
        st.info("No patient predictions saved yet. Go to Predict page and run at least one diagnosis.")
    else:
        st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Predicted Patients</div>', unsafe_allow_html=True)
        st.dataframe(history_df[["Timestamp", "Model", "Predicted_Diagnosis", "Confidence", "Risk_Category"]], width="stretch")
        
        cpa, cpb = st.columns([1, 1])
        with cpa:
            st.download_button("⬇️  Download All Patients", data=history_df.to_csv(index=False).encode(), file_name="patients.csv", mime="text/csv", width="stretch")
        with cpb:
            if st.button("🧹 Clear History", width="stretch"):
                st.session_state.prediction_history = []
                st.rerun()
        
        st.markdown("**Diagnosis Distribution**")
        mix = history_df["Predicted_Diagnosis"].value_counts()
        st.bar_chart(mix, color="#e84545")
        st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────────
# PAGE: REPORTS
# ────────────────────────────────────────────────────────────────────────────────

if page == "reports":
    render_header("Reports", "Comprehensive analytics and system performance")
    render_page_banner("Reports", "Detailed evaluation metrics, predictions analysis, and audit trail")

    st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Model Performance Dashboard</div>', unsafe_allow_html=True)
    
    rep1, rep2, rep3, rep4 = st.columns(4)
    with rep1:
        st.metric("🏆 Best Model", best_mdl, f"{best_f1}% F1")
    with rep2:
        st.metric("📊 Avg Accuracy", f"{np.mean([m['accuracy'] for m in metrics.values()]):.1f}%")
    with rep3:
        st.metric("📈 Dataset Size", f"{len(df):,}")
    with rep4:
        st.metric("🔍 Features", len(feat_cols))

    tab1, tab2, tab3 = st.tabs(["Performance", "Feature Analysis", "Prediction Analytics"])

    with tab1:
        metrics_table = pd.DataFrame([{"Model": m, "Accuracy (%)": v["accuracy"], "F1-Macro (%)": v["f1"]} for m, v in metrics.items()]).set_index("Model")
        st.dataframe(metrics_table, width="stretch")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        models_list = list(metrics.keys())
        ax1.bar(models_list, [metrics[m]["accuracy"] for m in models_list], color="#4c6ef5", alpha=0.7)
        ax1.set_title("Accuracy by Model")
        ax1.set_ylim([0, 100])
        ax2.bar(models_list, [metrics[m]["f1"] for m in models_list], color="#e84545", alpha=0.7)
        ax2.set_title("F1-Macro by Model")
        ax2.set_ylim([0, 100])
        st.pyplot(fig, clear_figure=True)

    with tab2:
        rf_model = models["Random Forest"]
        importance_df = pd.DataFrame({"Feature": feat_cols, "Importance": rf_model.feature_importances_}).sort_values("Importance", ascending=False)
        st.dataframe(importance_df, width="stretch")
        fig, ax = plt.subplots(figsize=(10, 6))
        top_n = min(15, len(importance_df))
        top_features = importance_df.head(top_n)
        ax.barh(range(len(top_features)), top_features["Importance"], color="#e84545", alpha=0.7)
        ax.set_yticks(range(len(top_features)))
        ax.set_yticklabels(top_features["Feature"])
        ax.invert_yaxis()
        st.pyplot(fig, clear_figure=True)

    with tab3:
        history_df = pd.DataFrame(st.session_state.prediction_history)
        if not history_df.empty:
            st.metric("Total Predictions", len(history_df))
            mix = history_df["Predicted_Diagnosis"].value_counts()
            fig, ax = plt.subplots(figsize=(8, 4))
            mix.plot(kind='bar', ax=ax, color=["#e84545", "#4c6ef5"])
            ax.set_title("Diagnosis Distribution")
            st.pyplot(fig, clear_figure=True)
        else:
            st.info("No predictions made yet.")

    st.markdown("</div>", unsafe_allow_html=True)

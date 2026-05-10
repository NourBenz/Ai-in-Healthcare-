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

st.set_page_config(page_title="Medico Diagnosis", layout="wide", page_icon="🏥")

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

with st.sidebar:
    st.markdown("<div class='brand-orb'></div>", unsafe_allow_html=True)
    st.markdown("### 🏥 Medico")
    st.caption("Breast Cancer Diagnosis")
    nav_choice = st.radio(
        "Navigation",
        ["Dashboard", "Dataset", "Predict", "Patients", "Reports"],
        index=["dashboard", "dataset", "predict", "patients", "reports"].index(st.session_state.page) if st.session_state.page in ["dashboard", "dataset", "predict", "patients", "reports"] else 0,
        label_visibility="collapsed",
    )
    

page_map = {
    "Dashboard": "dashboard",
    "Dataset": "dataset",
    "Predict": "predict",
    "Patients": "patients",
    "Reports": "reports"
}
page = page_map.get(nav_choice, "dashboard")
st.session_state.page = page

# ── CSS ─────────────────────────────────────────────────────────────────────────
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
[data-testid="stSidebar"] p {
    font-size: 13px;
}

.brand-orb {
    width: 14px;
    height: 14px;
    border-radius: 4px;
    background: linear-gradient(140deg, #7c86ff 0%, #5c66f5 100%);
    margin-bottom: 8px;
}

.side-link {
    font-size: 13px;
    color: #9ca8c7;
    padding: 7px 8px;
    border-radius: 8px;
    border: 1px solid transparent;
    margin-bottom: 4px;
}

.side-link:hover {
    background: rgba(255,255,255,.04);
    border-color: rgba(255,255,255,.08);
}

/* Push ALL streamlit content right of the fixed nav */
section.main > div.block-container,
.block-container,
[data-testid="stMainBlockContainer"],
div.block-container {
    padding-top: 32px !important;
    padding-bottom: 32px !important;
    padding-left: 36px !important;
    padding-right: 36px !important;
    max-width: 100% !important;
}

/* Remove streamlit's default top padding that hides nav logo */
.stApp > header { display: none !important; }
.stApp { padding-top: 0 !important; margin-top: 0 !important; }

/* ── Fixed Left Nav (legacy styles retained but hidden) ── */
.medai-nav {
    display: none !important;
}
.nav-logo-area {
    padding: 22px 20px 20px;
    border-bottom: 1px solid #f2f2f2;
    display: flex; align-items: center; gap: 10px;
}
.nav-logo-icon {
    width: 36px; height: 36px; border-radius: 10px;
    background: #e84545;
    display: flex; align-items: center; justify-content: center;
    color: #fff; font-weight: 800; font-size: 16px; flex-shrink: 0;
    font-family: 'DM Sans', sans-serif;
}
.nav-logo-name { font-weight: 700; font-size: 15px; color: #1a1a2e; line-height: 1.2; }
.nav-logo-sub  { font-size: 11px; color: #bbb; }
.nav-section   { font-size: 10px; font-weight: 700; color: #ccc; letter-spacing: 1.3px;
                 text-transform: uppercase; padding: 18px 20px 6px; }
.nav-link {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 20px; font-size: 13.5px; font-weight: 500;
    color: #777; border-left: 3px solid transparent;
    transition: all .15s; cursor: pointer; text-decoration: none;
}
.nav-link:hover, .nav-link.active {
    color: #e84545; background: #fff5f5; border-left-color: #e84545;
}
.nav-link .ni { font-size: 15px; width: 18px; text-align: center; }
.nav-spacer { flex: 1; }
.nav-user-area {
    padding: 16px 20px;
    border-top: 1px solid #f2f2f2;
    display: flex; align-items: center; gap: 10px;
}
.nav-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    background: linear-gradient(135deg, #e84545, #ff7676);
    display: flex; align-items: center; justify-content: center;
    color: #fff; font-weight: 800; font-size: 12px; flex-shrink: 0;
}
.nav-uname { font-size: 13px; font-weight: 600; color: #1a1a2e; }
.nav-urole { font-size: 11px; color: #bbb; }

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

.top-mini {
    display: inline-block;
    border: 1px solid #eceff8;
    border-radius: 10px;
    background: #fff;
    padding: 8px 11px;
    font-size: 12px;
    margin-left: 8px;
    color: #6b7185;
}

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
.sc-trend   { font-size: 11px; color: #4caf50; font-weight: 600; }
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

/* ── Bar rows ── */
.bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 9px; }
.bar-lbl { font-size: 12px; font-weight: 500; color: #555; width: 120px; flex-shrink: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bar-track { flex: 1; background: #f2f2f2; border-radius: 99px; height: 8px; overflow: hidden; }
.bar-fill  { height: 100%; border-radius: 99px; background: #e84545; }
.bar-fill.blue { background: linear-gradient(90deg,#4c6ef5,#748ffc); }
.bar-pct   { font-size: 12px; font-weight: 700; color: #333; width: 42px; text-align: right; flex-shrink: 0; }

/* ── Result banner ── */
.res-banner {
    border-radius: 14px; padding: 20px 22px; margin-bottom: 16px; color: #fff;
}
.res-banner.hi { background: linear-gradient(135deg, #e84545 0%, #ff6b6b 100%); }
.res-banner.lo { background: linear-gradient(135deg, #f5a623 0%, #f7c948 100%); }
.res-lbl  { font-size: 10px; font-weight: 700; opacity:.8; letter-spacing:1.2px; text-transform:uppercase; }
.res-diag { font-size: 26px; font-weight: 800; margin: 4px 0 2px; font-family:'DM Serif Display',serif; }
.res-conf { font-size: 13px; opacity:.9; }

/* ── Tip cards ── */
.tip-card {
    display: flex; align-items: flex-start; gap: 12px;
    background: #f9f9fb; border-radius: 12px; padding: 13px; margin-bottom: 10px;
}
.tip-icon {
    width: 32px; height: 32px; border-radius: 8px; background: #fff0f0;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; flex-shrink: 0;
}
.tip-b { display: block; font-size: 12px; color: #1a1a2e; font-weight: 700; margin-bottom: 2px; }
.tip-p { font-size: 11.5px; color: #999; margin: 0; line-height: 1.4; }

/* ── Form overrides ── */
div[data-baseweb="select"] > div {
    border-radius: 10px !important; border-color: #e8e8e8 !important;
    font-size: 13px !important;
}
.stFormSubmitButton > button {
    background: #e84545 !important; color: #fff !important;
    border: none !important; border-radius: 12px !important;
    font-size: 14px !important; font-weight: 700 !important;
    padding: 14px 0 !important;
    box-shadow: 0 4px 16px rgba(232,69,69,.35) !important;
    transition: all .2s !important;
}
.stFormSubmitButton > button:hover {
    background: #d13535 !important;
    box-shadow: 0 6px 22px rgba(232,69,69,.45) !important;
    transform: translateY(-1px) !important;
}
label[data-testid="stWidgetLabel"] p {
    font-size: 11.5px !important; font-weight: 600 !important;
    color: #666 !important; text-transform: uppercase !important;
    letter-spacing: .4px !important;
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

/* Better table container look */
[data-testid="stDataFrame"] {
    border: 1px solid #eceff8;
    border-radius: 12px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# Native Streamlit sidebar is used for navigation to avoid opening new windows.

# ── Data & Training ───────────────────────────────────────────────────────────
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

@st.cache_resource
def train_all(df):
    d = df.drop(columns=DROP_COLS).copy()
    # Fill missing values in categorical columns
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

# ── Top Bar ───────────────────────────────────────────────────────────────────
best_mdl = max(metrics, key=lambda m: metrics[m]["f1"])
best_f1 = metrics[best_mdl]["f1"]
best_acc = metrics[best_mdl]["accuracy"]

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []


def render_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="top-bar">
          <div class="top-greeting">
            <h1>{title}</h1>
            <p>{subtitle}</p>
          </div>
          <div>
                        <span class="top-mini">🔎 Search</span>
                        <span class="top-mini">🔔</span>
                        <span class="top-mini">👤</span>
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


if page == "dashboard":
    render_header("Good Morning, Doctor 👋", "AI-powered clinical diagnosis prediction · Spring 2026")
    render_page_banner("Dashboard", "Overview of model performance, class distribution, and top feature impact")

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card">
        <div class="sc-top"><div class="sc-icon r">👥</div><span class="sc-trend">Dataset</span></div>
        <div class="sc-value">{len(df):,}</div><div class="sc-label">Total Patients</div>
      </div>
      <div class="stat-card">
        <div class="sc-top"><div class="sc-icon b">🔬</div><span class="sc-trend">Stable</span></div>
        <div class="sc-value">{len(target_le.classes_)}</div><div class="sc-label">Diagnosis Classes</div>
      </div>
      <div class="stat-card">
        <div class="sc-top"><div class="sc-icon g">🎯</div><span class="sc-trend">Best Model</span></div>
        <div class="sc-value">{best_acc}%</div><div class="sc-label">Top Accuracy</div>
      </div>
      <div class="stat-card">
        <div class="sc-top"><div class="sc-icon a">📐</div><span class="sc-trend">F1: {best_f1}%</span></div>
        <div class="sc-value">{len(feat_cols)}</div><div class="sc-label">Features Used</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([2.2, 1], gap="large")
    with c1:
        st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Model Performance Comparison</div>', unsafe_allow_html=True)
        t1, t2 = st.tabs(["📊  Metrics", "📈  Class Distribution"])
        with t1:
            perf = pd.DataFrame(
                [{"Model": m, "Accuracy (%)": v["accuracy"], "F1-Macro (%)": v["f1"]} for m, v in metrics.items()]
            ).set_index("Model")
            st.dataframe(perf, width="stretch")
            st.bar_chart(perf, color=["#e84545", "#4c6ef5"])
        with t2:
            dist = df[TARGET_COL].value_counts().reset_index()
            dist.columns = ["Diagnosis", "Count"]
            st.bar_chart(dist.set_index("Diagnosis"), color="#e84545")
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
        st.markdown("""
        <div class="card">
          <div class="card-title"><span class="ct-dot"></span>Clinical Tips</div>
          <div class="tip-card"><div class="tip-icon">💊</div><div><span class="tip-b">Medication Adherence</span><p class="tip-p">Follow prescribed duration for accurate outcome prediction.</p></div></div>
          <div class="tip-card"><div class="tip-icon">🩺</div><div><span class="tip-b">Routine Checkups</span><p class="tip-p">Track blood pressure, heart rate and lab markers regularly.</p></div></div>
          <div class="tip-card"><div class="tip-icon">🧬</div><div><span class="tip-b">Family History</span><p class="tip-p">Consider hereditary risk during early triage decisions.</p></div></div>
          <div class="tip-card"><div class="tip-icon">⚠️</div><div><span class="tip-b">Allergy Profile</span><p class="tip-p">Review known allergies before recommending medication.</p></div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Traffic Source</div>', unsafe_allow_html=True)
        dist = df[TARGET_COL].value_counts()
        donut_colors = ["#5a66f4", "#f59f00", "#22c58b", "#ff6b6b", "#9aa5c2"]
        fig, ax = plt.subplots(figsize=(4.4, 3.2))
        ax.pie(
            dist.values,
            colors=donut_colors[: len(dist)],
            startangle=90,
            counterclock=False,
            wedgeprops={"width": 0.42, "edgecolor": "white"},
        )
        ax.set(aspect="equal")
        st.pyplot(fig, clear_figure=True)
        for cls, cnt in dist.items():
            pct = (cnt / len(df)) * 100
            st.markdown(f'<div class="bar-row"><div class="bar-lbl">{cls}</div><div class="bar-track"><div class="bar-fill blue" style="width:{pct:.1f}%"></div></div><div class="bar-pct">{pct:.1f}%</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if page == "predict":
    render_header("Patient Prediction", "Enter patient characteristics to generate diagnosis and risk confidence")
    render_page_banner("Predict", "Run diagnosis inference with confidence and export patient-level results")

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
                        step = 0.01 if any(k in cn for k in ["Pressure", "Rate", "Temp", "Results", "Conf"]) else 1.0
                        val = round(mean, 2) if step < 1 else float(round(mean))
                        inputs[cn] = st.number_input(
                            cn,
                            min_value=float(np.floor(mn)),
                            max_value=float(np.ceil(mx)),
                            value=val,
                            step=step,
                        )
        submitted = st.form_submit_button("🔍  Predict Diagnosis", width="stretch")

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        patient_df = pd.DataFrame([inputs]).reindex(columns=feat_cols)
        # Fill missing values in categorical columns
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

        proba_df = pd.DataFrame({"Diagnosis": target_le.classes_, "Probability": proba}).sort_values("Probability", ascending=False).reset_index(drop=True)

        st.markdown("### 🩺 Prediction Result")
        r1, r2 = st.columns([1, 1.6], gap="large")

        with r1:
            css_cls = "hi" if top_prob >= threshold else "lo"
            conf_lbl = "HIGH CONFIDENCE" if top_prob >= threshold else "LOW CONFIDENCE — Review Advised"
            st.markdown(
                f"""
                <div class="res-banner {css_cls}">
                  <div class="res-lbl">{conf_lbl}</div>
                  <div class="res-diag">{pred_label}</div>
                  <div class="res-conf">Confidence: {top_prob:.1%} &nbsp;·&nbsp; {model_choice}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("**All Class Probabilities**")
            for _, row in proba_df.iterrows():
                pct = row["Probability"] * 100
                st.markdown(
                    f'<div class="bar-row"><div class="bar-lbl">{row["Diagnosis"]}</div><div class="bar-track"><div class="bar-fill" style="width:{pct:.1f}%"></div></div><div class="bar-pct">{pct:.1f}%</div></div>',
                    unsafe_allow_html=True,
                )

        with r2:
            st.markdown("**Probability Distribution**")
            st.bar_chart(proba_df.set_index("Diagnosis"), color="#e84545")
            export = patient_df.copy()
            export.insert(0, "Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            export.insert(1, "Model", model_choice)
            export["Predicted_Diagnosis"] = pred_label
            export["Confidence"] = round(top_prob, 4)

            for _, row in proba_df.iterrows():
                export[f"Prob_{row['Diagnosis']}"] = round(float(row["Probability"]), 6)

            st.session_state.prediction_history.append(export.iloc[0].to_dict())

            st.download_button(
                "⬇️  Download Prediction as CSV",
                data=export.to_csv(index=False).encode(),
                file_name="prediction.csv",
                mime="text/csv",
                width="stretch",
            )

            st.info("Open the Patients section from the left sidebar to view saved predictions.")

if page == "patients":
    render_header("Patients", "View all predicted patients and export accumulated prediction history")
    render_page_banner("Patients", "Track prediction history and review diagnosis mix across saved patients")

    history_df = pd.DataFrame(st.session_state.prediction_history)
    if history_df.empty:
        st.info("No patient predictions saved yet. Go to Predict page and run at least one diagnosis.")
    else:
        st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Predicted Patients</div>', unsafe_allow_html=True)
        st.dataframe(history_df, width="stretch")

        cpa, cpb = st.columns([1, 1])
        with cpa:
            st.download_button(
                "⬇️  Download All Patients CSV",
                data=history_df.to_csv(index=False).encode(),
                file_name="patients_predictions.csv",
                mime="text/csv",
                width="stretch",
            )
        with cpb:
            if st.button("🧹 Clear Patients History", width="stretch"):
                st.session_state.prediction_history = []
                st.rerun()

        st.markdown("**Predicted Diagnosis Mix**")
        mix = history_df["Predicted_Diagnosis"].value_counts()
        st.bar_chart(mix, color="#e84545")
        st.markdown("</div>", unsafe_allow_html=True)

if page == "dataset":
    render_header("Dataset Exploration", "Comprehensive analysis of Breast Cancer dataset features and distributions")
    render_page_banner("Dataset Info", "Explore feature relationships, missing data, and statistical summaries")

    st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Dataset Overview</div>', unsafe_allow_html=True)
    ds1, ds2, ds3, ds4 = st.columns(4)
    with ds1:
        st.metric("Total Records", len(df))
    with ds2:
        st.metric("Total Features", len(feat_cols))
    with ds3:
        st.metric("Classes", len(target_le.classes_))
    with ds4:
        st.metric("Missing Values", df.isnull().sum().sum())
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>First 10 Records</div>', unsafe_allow_html=True)
    st.dataframe(df.head(10), width="stretch", height=300)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Statistical Summary</div>', unsafe_allow_html=True)
    st.dataframe(df.describe(), width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Data Types</div>', unsafe_allow_html=True)
        dtypes_df = pd.DataFrame({
            "Column": df.columns,
            "Type": df.dtypes.astype(str),
            "Non-Null": df.notna().sum(),
            "Null": df.isna().sum()
        })
        st.dataframe(dtypes_df, width="stretch", height=400)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Target Variable Distribution</div>', unsafe_allow_html=True)
        target_dist = df[TARGET_COL].value_counts()
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(target_dist.index, target_dist.values, color=["#e84545", "#4c6ef5"])
        ax.set_ylabel("Count")
        ax.set_title(TARGET_COL)
        st.pyplot(fig, clear_figure=True)
        
        for cls, cnt in target_dist.items():
            pct = (cnt / len(df)) * 100
            st.markdown(f'<div class="bar-row"><div class="bar-lbl">{cls}</div><div class="bar-track"><div class="bar-fill" style="width:{pct:.1f}%"></div></div><div class="bar-pct">{pct:.1f}%</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Numerical Features Correlation</div>', unsafe_allow_html=True)
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if num_cols:
        corr_matrix = df[num_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax, cbar_kws={'shrink': 0.8})
        st.pyplot(fig, clear_figure=True)
    else:
        st.info("No numerical features to display correlation.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Feature Distributions</div>', unsafe_allow_html=True)
    num_features = df.select_dtypes(include=[np.number]).columns.tolist()
    if num_features:
        selected_features = st.multiselect("Select features to visualize:", num_features, default=num_features[:3])
        if selected_features:
            cols = st.columns(len(selected_features))
            for idx, feature in enumerate(selected_features):
                with cols[idx]:
                    fig, ax = plt.subplots(figsize=(4, 3))
                    ax.hist(df[feature], bins=30, color="#e84545", alpha=0.7, edgecolor="black")
                    ax.set_title(feature)
                    ax.set_ylabel("Frequency")
                    st.pyplot(fig, clear_figure=True)
    st.markdown("</div>", unsafe_allow_html=True)

if page == "reports":
    render_header("Reports & Statistics", "Comprehensive performance analytics and clinical insights")
    render_page_banner("Statistics", "Detailed model evaluation, predictions analysis, and pattern discovery")

    st.markdown('<div class="card"><div class="card-title"><span class="ct-dot"></span>Model Performance Dashboard</div>', unsafe_allow_html=True)
    
    rep1, rep2, rep3, rep4 = st.columns(4)
    with rep1:
        best_model = max(metrics, key=lambda m: metrics[m]["f1"])
        st.metric("🏆 Best Model", best_model, metrics[best_model]["f1"].__str__() + "%")
    with rep2:
        st.metric("📊 Avg Accuracy", f"{np.mean([m['accuracy'] for m in metrics.values()]):.1f}%")
    with rep3:
        st.metric("📈 Avg F1-Macro", f"{np.mean([m['f1'] for m in metrics.values()]):.1f}%")
    with rep4:
        st.metric("🔍 Total Features", len(feat_cols))

    tab1, tab2, tab3 = st.tabs(["Performance Metrics", "Feature Analysis", "Prediction Analytics"])

    with tab1:
        st.subheader("Model Comparison Detailed Metrics")
        metrics_table = pd.DataFrame([
            {"Model": m, "Accuracy (%)": v["accuracy"], "F1-Macro (%)": v["f1"]}
            for m, v in metrics.items()
        ]).set_index("Model")
        st.dataframe(metrics_table, width="stretch")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        models_list = list(metrics.keys())
        accuracies = [metrics[m]["accuracy"] for m in models_list]
        f1s = [metrics[m]["f1"] for m in models_list]
        
        ax1.bar(models_list, accuracies, color="#4c6ef5", alpha=0.7)
        ax1.set_title("Accuracy by Model")
        ax1.set_ylabel("Accuracy (%)")
        ax1.set_ylim([0, 100])
        
        ax2.bar(models_list, f1s, color="#e84545", alpha=0.7)
        ax2.set_title("F1-Macro by Model")
        ax2.set_ylabel("F1-Macro (%)")
        ax2.set_ylim([0, 100])
        
        st.pyplot(fig, clear_figure=True)

    with tab2:
        st.subheader("Feature Importance Analysis")
        rf_model = models["Random Forest"]
        importance_df = pd.DataFrame({
            "Feature": feat_cols,
            "Importance": rf_model.feature_importances_
        }).sort_values("Importance", ascending=False)
        
        st.dataframe(importance_df, width="stretch")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        top_n = min(15, len(importance_df))
        top_features = importance_df.head(top_n)
        ax.barh(range(len(top_features)), top_features["Importance"], color="#e84545", alpha=0.7)
        ax.set_yticks(range(len(top_features)))
        ax.set_yticklabels(top_features["Feature"])
        ax.set_xlabel("Importance Score")
        ax.set_title(f"Top {top_n} Most Important Features")
        ax.invert_yaxis()
        st.pyplot(fig, clear_figure=True)

    with tab3:
        st.subheader("Prediction History Analysis")
        history_df = pd.DataFrame(st.session_state.prediction_history)
        
        if not history_df.empty:
            pred1, pred2 = st.columns(2)
            with pred1:
                st.metric("Total Predictions Made", len(history_df))
            with pred2:
                pred_diagnosis = history_df["Predicted_Diagnosis"].value_counts()
                st.metric("Unique Diagnoses", len(pred_diagnosis))
            
            st.subheader("Diagnosis Distribution")
            fig, ax = plt.subplots(figsize=(8, 4))
            pred_diagnosis.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=["#e84545", "#4c6ef5"])
            st.pyplot(fig, clear_figure=True)
            
            st.subheader("Confidence Score Distribution")
            if "Confidence" in history_df.columns:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(history_df["Confidence"], bins=20, color="#4c6ef5", alpha=0.7, edgecolor="black")
                ax.set_xlabel("Confidence Score")
                ax.set_ylabel("Frequency")
                ax.set_title("Distribution of Prediction Confidence Scores")
                st.pyplot(fig, clear_figure=True)
            
            st.subheader("Model Usage")
            if "Model" in history_df.columns:
                model_counts = history_df["Model"].value_counts()
                fig, ax = plt.subplots(figsize=(8, 4))
                model_counts.plot(kind='bar', ax=ax, color="#e84545", alpha=0.7)
                ax.set_title("Model Usage Frequency")
                ax.set_ylabel("Count")
                st.pyplot(fig, clear_figure=True)
        else:
            st.info("No predictions made yet. Make predictions to see analytics.")
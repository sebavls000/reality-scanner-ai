import streamlit as st
import pandas as pd
import plotly.express as px
from src.rules import score_text, classify

st.set_page_config(page_title="Reality Scanner AI", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    h1, h2, h3 {
        color: #f8fafc !important;
    }
    p, label, div {
        color: #e5e7eb;
    }
    .card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.18);
    }
    .hero {
        background: linear-gradient(135deg, rgba(59,130,246,0.18), rgba(168,85,247,0.16));
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 18px;
    }
    .small-muted {
        color: #cbd5e1 !important;
        font-size: 0.95rem;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #cbd5e1 !important;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []


def normalize_scores(scores: dict) -> dict:
    normalized = {
        "Manipulación": 0,
        "Ciencia": 0,
        "Religión": 0,
        "Filosofía": 0,
    }

    key_map = {
        "manipulation": "Manipulación",
        "manipulacion": "Manipulación",
        "manipulación": "Manipulación",
        "science": "Ciencia",
        "la ciencia": "Ciencia",
        "ciencia": "Ciencia",
        "religion": "Religión",
        "religión": "Religión",
        "la religión": "Religión",
        "philosophy": "Filosofía",
        "filosofia": "Filosofía",
        "filosofía": "Filosofía",
    }

    for k, v in scores.items():
        safe_key = str(k).strip().lower()
        if safe_key in key_map:
            normalized[key_map[safe_key]] = v

    return normalized


def safe_label(label: str) -> str:
    label = str(label).strip().lower()
    if label == "manipulation":
        return "MANIPULACIÓN"
    if label == "science":
        return "CIENCIA"
    if label == "religion":
        return "RELIGIÓN"
    if label == "philosophy":
        return "FILOSOFÍA"
    return str(label).upper()


def render_metric_card(title: str, value: int):
    st.markdown(
        f"""
        <div class="card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    """
    <div class="hero">
        <h1>🧠 Reality Scanner AI</h1>
        <p class="small-muted">
            Detectá manipulación, narrativa y sesgo en segundos. Pegá un texto, compará discursos y observá patrones.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["🔍 Análisis individual", "⚔️ Comparador", "🔥 Tendencias"])

with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    text_input = st.text_area(
        "Ingresá un texto para analizar:",
        height=180,
        placeholder="Ejemplo: La élite controla la verdad y manipula a las masas..."
    )
    analyze_clicked = st.button("ANALIZAR AHORA", use_container_width=True, type="primary")
    st.markdown("</div>", unsafe_allow_html=True)

    if analyze_clicked and text_input.strip():
        raw_scores = score_text(text_input)
        scores = normalize_scores(raw_scores)
        label = safe_label(classify(raw_scores))

        manipulation_score = scores["Manipulación"]
        science_score = scores["Ciencia"]
        religion_score = scores["Religión"]
        philosophy_score = scores["Filosofía"]

        st.markdown("## Resultado")
        st.markdown(f"### {label}")

        total_score = min(100, manipulation_score * 100)

        if manipulation_score >= 1:
            st.warning("🟡 Posible manipulación")
            explanation = "El texto activa señales asociadas a influencia o encuadre narrativo."
        else:
            st.success("🟢 Bajo riesgo")
            explanation = "El texto muestra baja presencia de señales manipulativas explícitas."

        st.progress(total_score / 100)
        st.markdown(f"**Score de manipulación:** {total_score}/100")
        st.caption(explanation)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            render_metric_card("Manipulación", manipulation_score)
        with m2:
            render_metric_card("Ciencia", science_score)
        with m3:
            render_metric_card("Religión", religion_score)
        with m4:
            render_metric_card("Filosofía", philosophy_score)

        df_scores = pd.DataFrame(
            {
                "Categoría": ["Manipulación", "Ciencia", "Religión", "Filosofía"],
                "Valor": [manipulation_score, science_score, religion_score, philosophy_score],
            }
        )

        fig = px.bar(
            df_scores,
            x="Categoría",
            y="Valor",
            color="Categoría",
            text="Valor",
            title="Intensidad narrativa"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            showlegend=False,
            yaxis_title="Valor",
            xaxis_title="Categoría",
            yaxis=dict(range=[0, max(1, df_scores["Valor"].max()) + 1]),
            margin=dict(l=20, r=20, t=60, b=20),
            height=420
        )
        st.plotly_chart(fig, use_container_width=True)

        st.session_state.history.append(
            {
                "texto": text_input,
                "score": total_score,
                "label": label,
            }
        )

    elif analyze_clicked and not text_input.strip():
        st.warning("Pegá un texto antes de analizar.")

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    text_a = col_a.text_area("Texto A", height=150, placeholder="Texto más neutral o científico")
    text_b = col_b.text_area("Texto B", height=150, placeholder="Texto más emocional o manipulativo")
    compare_clicked = st.button("COMPARAR", use_container_width=True, type="primary")
    st.markdown("</div>", unsafe_allow_html=True)

    if compare_clicked and text_a.strip() and text_b.strip():
        raw_scores_a = score_text(text_a)
        raw_scores_b = score_text(text_b)

        scores_a = normalize_scores(raw_scores_a)
        scores_b = normalize_scores(raw_scores_b)

        manip_a = scores_a["Manipulación"]
        manip_b = scores_b["Manipulación"]

        st.markdown("## Comparación")

        top1, top2 = st.columns(2)
        with top1:
            render_metric_card("Puntuación Texto A", manip_a)
        with top2:
            render_metric_card("Puntuación Texto B", manip_b)

        df_compare = pd.DataFrame(
            {
                "Texto": ["Texto A", "Texto B"],
                "Manipulación": [manip_a, manip_b],
            }
        )

        fig2 = px.bar(
            df_compare,
            x="Texto",
            y="Manipulación",
            color="Texto",
            text="Manipulación",
            title="Comparación de manipulación"
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(
            showlegend=False,
            yaxis_title="Manipulación",
            xaxis_title="Texto",
            yaxis=dict(range=[0, max(1, df_compare["Manipulación"].max()) + 1]),
            margin=dict(l=20, r=20, t=60, b=20),
            height=420
        )
        st.plotly_chart(fig2, use_container_width=True)

        if manip_a > manip_b:
            st.error("Texto A es más manipulador")
        elif manip_b > manip_a:
            st.error("Texto B es más manipulador")
        else:
            st.success("Empate")

    elif compare_clicked:
        st.warning("Completá los dos textos antes de comparar.")

with tab3:
    st.markdown("## Tendencias")
    if len(st.session_state.history) > 0:
        df_hist = pd.DataFrame(st.session_state.history)
        st.dataframe(df_hist, use_container_width=True)

        df_hist = df_hist.reset_index(drop=True)
        df_hist["Análisis"] = df_hist.index + 1

        fig3 = px.line(
            df_hist,
            x="Análisis",
            y="score",
            markers=True,
            title="Evolución de manipulación"
        )
        fig3.update_layout(
            xaxis_title="Análisis",
            yaxis_title="Score",
            yaxis=dict(range=[0, 100]),
            margin=dict(l=20, r=20, t=60, b=20),
            height=420
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Todavía no hay historial. Hacé al menos un análisis individual.")

st.markdown("## 📊 Dataset de ejemplo")
df = pd.read_csv("data/sample_texts.csv")
st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown("**Reality Scanner AI** — by Sebastian Valles")
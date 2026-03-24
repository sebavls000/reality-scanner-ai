import streamlit as st
import pandas as pd
import plotly.express as px
from src.rules import score_text, classify

st.set_page_config(page_title="Reality Scanner AI", page_icon="🧠", layout="wide")

# ====== ESTILO ======
st.markdown("""
<style>
.stApp {background: linear-gradient(180deg, #0f172a 0%, #111827 100%);}
.block-container {max-width: 1100px; padding-top: 2rem;}
h1,h2,h3 {color:#f8fafc !important;}
p,div,label {color:#e5e7eb;}
.card {
    background: rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:16px;
    padding:16px;
    margin-bottom:12px;
}
.hero {
    background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(168,85,247,0.2));
    border-radius:18px;
    padding:20px;
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

# ====== STATE ======
if "history" not in st.session_state:
    st.session_state.history = []

# ====== FUNCIONES ======
def normalize(scores):
    return {
        "Manipulación": scores.get("manipulation", 0),
        "Ciencia": scores.get("science", 0),
        "Religión": scores.get("religion", 0),
        "Filosofía": scores.get("philosophy", 0),
    }

def label_map(label):
    return {
        "manipulation":"MANIPULACIÓN",
        "science":"CIENCIA",
        "religion":"RELIGIÓN",
        "philosophy":"FILOSOFÍA"
    }.get(label, label.upper())

# ====== HEADER ======
st.markdown("""
<div class="hero">
<h1>🧠 Reality Scanner AI</h1>
<p>Analizá textos, detectá manipulación y compará narrativas en segundos.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔍 Analizar", "⚔️ Comparar", "🔥 Tendencias"])

# ====== ANALISIS ======
with tab1:
    text = st.text_area("Texto:", height=150)

    if st.button("Analizar"):
        if text.strip():
            raw = score_text(text)
            scores = normalize(raw)
            label = label_map(classify(raw))

            st.subheader(label)

            manip = scores["Manipulación"]
            score100 = min(100, manip * 100)

            st.progress(score100 / 100)

            if manip >= 1:
                st.warning("Posible manipulación")
            else:
                st.success("Bajo riesgo")

            col1,col2,col3,col4 = st.columns(4)
            col1.metric("Manipulación", scores["Manipulación"])
            col2.metric("Ciencia", scores["Ciencia"])
            col3.metric("Religión", scores["Religión"])
            col4.metric("Filosofía", scores["Filosofía"])

            df = pd.DataFrame({
                "Categoría": scores.keys(),
                "Valor": scores.values()
            })

            fig = px.bar(df, x="Categoría", y="Valor", color="Categoría", text="Valor")
            fig.update_layout(showlegend=False, yaxis=dict(range=[0, max(1,max(df["Valor"]))+1]))
            st.plotly_chart(fig, use_container_width=True)

            st.session_state.history.append({
                "texto": text,
                "score": score100
            })

# ====== COMPARADOR ======
with tab2:
    a = st.text_area("Texto A")
    b = st.text_area("Texto B")

    if st.button("Comparar"):
        if a.strip() and b.strip():
            sa = normalize(score_text(a))["Manipulación"]
            sb = normalize(score_text(b))["Manipulación"]

            df = pd.DataFrame({
                "Texto":["A","B"],
                "Manipulación":[sa,sb]
            })

            fig = px.bar(df, x="Texto", y="Manipulación", text="Manipulación")
            fig.update_layout(yaxis=dict(range=[0,max(1,max(df["Manipulación"]))+1]))
            st.plotly_chart(fig, use_container_width=True)

            if sa > sb:
                st.error("A más manipulador")
            elif sb > sa:
                st.error("B más manipulador")
            else:
                st.success("Empate")

# ====== HISTORIAL ======
with tab3:
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)

        df["n"] = df.index + 1
        fig = px.line(df, x="n", y="score", markers=True)
        fig.update_layout(yaxis=dict(range=[0,100]))
        st.plotly_chart(fig, use_container_width=True)

# ====== DATASET ======
st.markdown("## Dataset")
st.dataframe(pd.read_csv("data/sample_texts.csv"))

st.markdown("---")
st.markdown("Reality Scanner AI — by Sebastian Valles")
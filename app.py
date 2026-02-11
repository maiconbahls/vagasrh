import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import os
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# URL de Exportação CSV (ajustada para o novo formato)
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1Vmg9SJzq_Hq9u5CpeLgt4X5qJPVai9LGH6ajpsR7m_I/export?format=csv"

# =========================================================
# 1. SETUP MODERN PREMIUM
# =========================================================
st.set_page_config(
    page_title="Cocal Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === PALETA DE CORES ===
COR_BG_DARK = "#050A14"
COR_BG_CARD = "rgba(20, 30, 50, 0.7)"
COR_PRIMARY = "#76B82A" # Verde Cocal
COR_SECONDARY = "#4a7c1b"
COR_SUCCESS = "#76B82A"
COR_WARNING = "#EF7D00"
COR_DANGER  = "#EF4444"
COR_TEXT_HEAD = "#FFFFFF"
COR_TEXT_BODY = "#E2E8F0"
COR_CHART_BLUE = "#30515F"
COR_CHART_GRAY = "#475569"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp {{
        background-color: {COR_BG_DARK};
        background: radial-gradient(circle at 50% 0%, #1a2c4e 0%, #050a14 70%);
        font-family: 'Outfit', sans-serif;
    }}
    
    .stDeployButton {{display: none !important;}}
    [data-testid="stStatusWidget"] {{display: none !important;}}
    header {{visibility: hidden !important;}}
    footer {{display: none !important;}}
    #MainMenu {{display: none !important;}}

    .header-container {{
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 20px; padding: 15px 25px;
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px; backdrop-filter: blur(10px);
    }}
    
    .app-title {{
        font-size: 26px; font-weight: 800; background: linear-gradient(90deg, #fff, #94a3b8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        display: flex; align-items: center; gap: 12px;
    }}

    .metric-card {{
        background: {COR_BG_CARD}; border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px; padding: 24px; height: 100%; transition: all 0.3s ease;
    }}
    .metric-card:hover {{ transform: translateY(-4px); background: rgba(30, 41, 59, 0.8); }}
    
    .metric-title {{ font-size: 11px; font-weight: 700; color: {COR_TEXT_BODY}; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.8; }}
    .metric-value {{ font-size: 42px; font-weight: 800; color: {COR_TEXT_HEAD}; font-family: 'JetBrains Mono', monospace; margin: 10px 0; }}

    .stButton > button {{
        border-radius: 6px; font-weight: 600; border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.02); color: {COR_TEXT_BODY}; font-size: 11px; padding: 6px 16px;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. ENGINE DE DADOS (NOVO FORMATO COLUNAR)
# =========================================================
def get_data():
    try:
        df = pd.read_csv(GSHEET_URL)
        # Limpeza básica de nomes de colunas caso haja espaços extras
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = get_data()

# Seção de navegação
if 'page' not in st.session_state: st.session_state.page = 'Dashboard'
if 'filtro' not in st.session_state: st.session_state.filtro = 'GERAL'

# --- HEADER ---
st.markdown(f'<div class="header-container"><div class="app-title">📊 EVOLUÇÃO VAGAS | COCAL</div></div>', unsafe_allow_html=True)

# --- FILTROS ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🌍 CONSOLIDADO", use_container_width=True, type="primary" if st.session_state.filtro == "GERAL" else "secondary"):
        st.session_state.filtro = "GERAL"; st.rerun()
with col2:
    if st.button("🏢 SÃO PAULO (SP)", use_container_width=True, type="primary" if st.session_state.filtro == "SP" else "secondary"):
        st.session_state.filtro = "SP"; st.rerun()
with col3:
    if st.button("🌾 MATO GROSSO (MS)", use_container_width=True, type="primary" if st.session_state.filtro == "MS" else "secondary"):
        st.session_state.filtro = "MS"; st.rerun()

if not df.empty:
    filtro = st.session_state.filtro
    
    if filtro == "SP":
        abertas = df['VAGAS ABERTAS SP'].sum() + df['SP_Saldo_Periodo'].fillna(0).max()
        fechadas = df['VAGAS FECHADAS SP'].sum()
    elif filtro == "MS":
        abertas = df['VAGAS ABERTA MS'].sum() + df['MS_Saldo_Periodo'].fillna(0).max()
        fechadas = df['VAGAS FECHADAS MS'].sum()
    else:
        abertas = (df['VAGAS ABERTAS SP'].sum() + df['VAGAS ABERTA MS'].sum() + 
                   df['SP_Saldo_Periodo'].fillna(0).max() + df['MS_Saldo_Periodo'].fillna(0).max())
        fechadas = df['VAGAS FECHADAS SP'].sum() + df['VAGAS FECHADAS MS'].sum()

    saldo = abertas - fechadas
    efic = (fechadas / abertas * 100) if abertas > 0 else 0

    # CARDS
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-card"><div class="metric-title">VOLUME</div><div class="metric-value">{int(abertas)}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card"><div class="metric-title">CONTRATOS</div><div class="metric-value">{int(fechadas)}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card"><div class="metric-title">BACKLOG</div><div class="metric-value">{int(saldo)}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card"><div class="metric-title">EFICIÊNCIA</div><div class="metric-value">{efic:.1f}%</div></div>', unsafe_allow_html=True)

    # GRÁFICO (WATERFALL)
    st.markdown('<br>', unsafe_allow_html=True)
    
    # Preparar dados para o Waterfall baseado no filtro
    fig = go.Figure()
    
    meses = df['Mês'].tolist()
    if filtro == "SP":
        y_ent = df['VAGAS ABERTAS SP'].fillna(0).tolist()
        y_sai = (-df['VAGAS FECHADAS SP'].fillna(0)).tolist()
        inicial = df['SP_Saldo_Periodo'].fillna(0).max()
    elif filtro == "MS":
        y_ent = df['VAGAS ABERTA MS'].fillna(0).tolist()
        y_sai = (-df['VAGAS FECHADAS MS'].fillna(0)).tolist()
        inicial = df['MS_Saldo_Periodo'].fillna(0).max()
    else:
        y_ent = (df['VAGAS ABERTAS SP'].fillna(0) + df['VAGAS ABERTA MS'].fillna(0)).tolist()
        y_sai = (-(df['VAGAS FECHADAS SP'].fillna(0) + df['VAGAS FECHADAS MS'].fillna(0))).tolist()
        inicial = df['SP_Saldo_Periodo'].fillna(0).max() + df['MS_Saldo_Periodo'].fillna(0).max()

    x_labels = ["INICIAL"]; y_vals = [inicial]; measure = ["absolute"]
    for m, e, s in zip(meses, y_ent, y_sai):
        x_labels.extend([f"{m} (New)", f"{m} (Fech)"])
        y_vals.extend([e, s])
        measure.extend(["relative", "relative"])
    
    x_labels.append("TOTAL"); y_vals.append(0); measure.append("total")

    fig.add_trace(go.Waterfall(
        x=x_labels, y=y_vals, measure=measure,
        increasing={"marker":{"color": COR_PRIMARY}},
        decreasing={"marker":{"color": COR_WARNING}},
        totals={"marker":{"color": COR_CHART_BLUE}}
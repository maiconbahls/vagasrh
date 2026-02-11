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
        position: relative; overflow: hidden;
    }}
    .metric-card::before {{
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 4px;
    }}
    .card-orange::before {{ background: {COR_WARNING}; box-shadow: 0 2px 10px rgba(239, 125, 0, 0.3); }}
    .card-green::before {{ background: {COR_SUCCESS}; box-shadow: 0 2px 10px rgba(123, 189, 66, 0.3); }}
    .card-blue::before {{ background: {COR_CHART_BLUE}; box-shadow: 0 2px 10px rgba(45, 67, 80, 0.3); }}

    .metric-card:hover {{ transform: translateY(-4px); background: rgba(30, 41, 59, 0.8); }}
    
    .metric-title {{ font-size: 11px; font-weight: 700; color: {COR_TEXT_BODY}; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.8; }}
    .metric-value {{ font-size: 42px; font-weight: 800; color: {COR_TEXT_HEAD}; font-family: 'JetBrains Mono', monospace; margin: 10px 0; }}

    /* Estilo dos Botões de Filtro */
    .stButton > button {{
        border-radius: 6px; font-weight: 600; border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.02); color: {COR_TEXT_BODY}; font-size: 11px; padding: 6px 16px;
        transition: all 0.3s ease;
    }}

    /* Botão Selecionado (Primary) */
    .stButton > button[kind="primary"] {{
        background: {COR_SUCCESS} !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(123, 189, 66, 0.4) !important;
    }}

    .stButton > button:hover {{
        border-color: {COR_SUCCESS};
        background: rgba(123, 189, 66, 0.05);
    }}

    /* Estilo para tornar o fundo do Toggle transparente */
    div[data-testid="stCheckbox"], div[data-testid="stToggleButton"] {{
        background-color: transparent !important;
        border: none !important;
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

    # 1. CARDS
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-card card-orange"><div class="metric-title">VOLUME</div><div class="metric-value">{int(abertas)}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card card-green"><div class="metric-title">CONTRATOS</div><div class="metric-value">{int(fechadas)}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card card-blue"><div class="metric-title">BACKLOG</div><div class="metric-value">{int(saldo)}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card card-green"><div class="metric-title">EFICIÊNCIA</div><div class="metric-value">{efic:.1f}%</div></div>', unsafe_allow_html=True)


    # 3. GRÁFICO (WATERFALL)
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

    x_labels = ["SALDO INICIAL"]; y_vals = [inicial]; measure = ["absolute"]
    for m, e, s in zip(meses, y_ent, y_sai):
        m_short = str(m)[:3].upper()
        x_labels.extend([f"{m_short}<br>Abertas", f"{m_short}<br>Fechadas"])
        y_vals.extend([e, s])
        measure.extend(["relative", "relative"])
    
    # Calcular saldo final para o texto da última barra
    saldo_final = inicial + sum(y_ent) + sum(y_sai)
    x_labels.append("SALDO<br>PENDENTE"); y_vals.append(saldo_final); measure.append("total")

    fig.add_trace(go.Waterfall(
        x=x_labels, y=y_vals, measure=measure,
        text=y_vals,
        texttemplate='%{text:,.0f}',
        increasing={"marker":{"color": COR_WARNING}},
        decreasing={"marker":{"color": COR_PRIMARY}},
        totals={"marker":{"color": COR_CHART_BLUE}},
        connector = {"line":{"color":"rgba(255,255,255,0.2)"}},
        textposition = "outside",
        showlegend = False # REMOVE O TRACE 0
    ))

    # Adicionando legendas manuais
    fig.add_trace(go.Bar(x=[None], y=[None], name='Abertas', marker_color=COR_WARNING))
    fig.add_trace(go.Bar(x=[None], y=[None], name='Fechadas', marker_color=COR_PRIMARY))
    fig.add_trace(go.Bar(x=[None], y=[None], name='Saldo Pende.', marker_color=COR_CHART_BLUE))

    # --- MODO DE IMPRESSÃO (DINÂMICO PARA A PÁGINA TODA) ---
    st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
    modo_print = st.toggle("📥 Modo Impressão (Visualizar Relatório #FAF9F9)", help="Ative para transformar o fundo do site em cinza claro e preparar para o download.")

    if modo_print:
        # Muda o fundo de TODO o site para o cinza solicitado
        st.markdown(f"""
            <style>
            .stApp {{
                background: #FAF9F9 !important;
            }}
            /* Ajusta textos para preto no modo claro */
            .stMarkdown, p, span, label, .stMetric {{ color: #333333 !important; }}
            .app-title {{ background: #30515F !important; -webkit-text-fill-color: #30515F !important; }}
            </style>
        """, unsafe_allow_html=True)

    # Cores dinâmicas
    bg_color = "rgba(0,0,0,0)" # Transparente no site para mostrar o fundo da página
    txt_color = "#333333" if modo_print else "white"
    grid_color = "rgba(0,0,0,0.03)" if modo_print else "rgba(255,255,255,0.02)"
    cor_txt_titulo = COR_CHART_BLUE if modo_print else "white"

    fig.update_layout(
        title={
            'text': f"<span style='color:{cor_txt_titulo}'>Abertas Acumulada: <b>{int(abertas)}</b></span> &nbsp;&nbsp; | &nbsp;&nbsp; <span style='color:{cor_txt_titulo}'>Fechadas Acumulada: <b>{int(fechadas)}</b></span> &nbsp;&nbsp; | &nbsp;&nbsp; <span style='color:{COR_SUCCESS}'>Evolução: <b>{efic:.1f}%</b></span>",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18, 'family': 'JetBrains Mono'}
        },
        template="plotly_dark" if not modo_print else None,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=txt_color),
        height=550,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(size=12, color=txt_color)),
        margin=dict(t=120, b=100),
        yaxis=dict(
            title="Quantidade de Vagas", 
            gridcolor=grid_color, 
            tickfont=dict(color=txt_color),
            title_font=dict(color=txt_color)
        ),
        xaxis=dict(gridcolor=grid_color, tickfont=dict(color=txt_color))
    )
    
    config = {
        'toImageButtonOptions': {
            'format': 'png', 
            'filename': 'Relatorio_Cocal_Vagas', 
            'scale': 2,
            'height': 600,
            'width': 1200,
            'backgroundColor': '#FAF9F9' if modo_print else 'rgba(0,0,0,0)' 
        }
    }
    
    st.plotly_chart(fig, use_container_width=True, config=config)

    # DICA: No Plotly, o botão da câmera é um 'print' da tela. 
    # Para ter cores diferentes só no download, o ideal é usar o fundo sólido que já colocamos (#111111), 
    # pois ele garante que os textos brancos apareçam em qualquer lugar.

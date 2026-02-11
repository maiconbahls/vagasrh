import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import os
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# URL de Exportação CSV que funcionou no teste
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

# === PALETA DE CORES INSTITUCIONAL (COCAL DARK) ===
COR_BG_DARK = "#050A14"      # Almost Black Blue
COR_BG_CARD = "rgba(20, 30, 50, 0.7)" # Deep Blue Glass
COR_BORDER  = "rgba(118, 184, 42, 0.3)" # Cocal Green border hint

# Cores da Marca (Institucionais Vibrantes para Dark Mode)
COR_PRIMARY = "#76B82A"      # Cocal Green (Destaque Principal)
COR_SECONDARY = "#4a7c1b"    # Dark Green (Harmônico)
COR_SUCCESS = "#76B82A"      # Cocal Green
COR_WARNING = "#EF7D00"      # Cocal Orange
COR_DANGER  = "#EF4444"      # Red
COR_TEXT_HEAD = "#FFFFFF"    # Pure White
COR_TEXT_BODY = "#E2E8F0"    # Gray 200

# Mapeamento para gráficos 
COR_CHART_GREEN = "#76B82A"  # Cocal Green
COR_CHART_ORANGE = "#EF7D00" # Cocal Orange
COR_CHART_BLUE = "#30515F"   # Cocal Blue Original (Totais)
COR_CHART_GRAY = "#475569"   # Slate

# Compatibilidade
COR_COCAL_GREEN = COR_CHART_GREEN
COR_COCAL_ORANGE = COR_CHART_ORANGE
COR_COCAL_BLUE = COR_CHART_BLUE
COR_COCAL_GRAY = COR_CHART_GRAY
COR_NEON_GREEN = COR_SUCCESS
COR_NEON_RED = COR_DANGER

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* === RESET & BACKGROUND === */
    .stApp {{
        background-color: {COR_BG_DARK};
        background: radial-gradient(circle at 50% 0%, #1a2c4e 0%, #050a14 70%);
        font-family: 'Outfit', sans-serif;
    }}
    
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 95% !important;
        margin: 0 auto !important;
    }}

    /* Remove Streamlit Default Elements (Ocultar Deploy definitivamente) */
    .stDeployButton {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    header {visibility: hidden !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}

    /* === HEADER === */
    .header-container {{
        display: flex; 
        align-items: center; 
        justify-content: space-between;
        margin-bottom: 20px;
        padding: 15px 25px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }}
    
    .app-title {{
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    
    .app-subtitle {{
        font-weight: 400;
        color: {COR_TEXT_BODY};
        font-size: 14px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        opacity: 0.8;
    }}

    /* === CARDS METRICOS === */
    .metric-card {{
        background: {COR_BG_CARD};
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }}
    
    .metric-card::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, {COR_PRIMARY}, {COR_SECONDARY});
        opacity: 0.8;
    }}

    .metric-card:hover {{
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        background: rgba(30, 41, 59, 0.8);
    }}
    
    .metric-title {{
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: {COR_TEXT_BODY};
        margin-bottom: 8px;
        display: flex; 
        align-items: center;
        gap: 8px;
        opacity: 0.8;
    }}
    
    .metric-value {{
        font-size: 48px;
        font-weight: 800;
        color: {COR_TEXT_HEAD};
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -2px;
        margin: 10px 0;
        text-shadow: 0 0 40px rgba(59, 130, 246, 0.2);
    }}
    
    .metric-footer {{
        font-size: 13px;
        display: flex; 
        align-items: center; 
        gap: 6px;
        padding: 6px 12px;
        background: rgba(255,255,255,0.05);
        border-radius: 6px;
        width: fit-content;
        color: {COR_TEXT_BODY};
        border: 1px solid rgba(255,255,255,0.05);
    }}

    /* Indicadores de Status (Bolinhas) */
    .status-dot {{ width: 8px; height: 8px; border-radius: 50%; display: inline-block; }}
    .dot-blue   {{ background-color: {COR_PRIMARY}; box-shadow: 0 0 10px {COR_PRIMARY}; }}
    .dot-green  {{ background-color: {COR_SUCCESS}; box-shadow: 0 0 10px {COR_SUCCESS}; }}
    .dot-orange {{ background-color: {COR_WARNING}; box-shadow: 0 0 10px {COR_WARNING}; }}
    .dot-red    {{ background-color: {COR_DANGER};  box-shadow: 0 0 10px {COR_DANGER}; }}

    /* === PAINEL DE GRÁFICOS === */
    .chart-panel {{
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
    }}
    
    .panel-header {{
        display: flex;
        align-items: center;
        margin-bottom: 25px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding-bottom: 15px;
    }}
    
    .panel-title {{
        font-size: 18px;
        font-weight: 700;
        color: {COR_TEXT_HEAD};
        letter-spacing: -0.5px;
    }}

    /* === CUSTOM COMPONENTS === */
    /* Labels de Inputs */
    .stTextInput > label, .stSelectbox > label, .stNumberInput > label {{
        color: #FFFFFF !important;
    }}

    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.02);
        color: {COR_TEXT_BODY};
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 11px;
        padding: 6px 16px; /* Reduzido para ficar mais fino */
        height: auto;
        min-height: 0;
    }
    
    .stButton > button:hover {{
        background: rgba(255,255,255,0.08);
        border-color: rgba(255,255,255,0.2);
        color: white;
    }}
    
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {COR_PRIMARY} 0%, {COR_SECONDARY} 100%);
        border: 1px solid {COR_PRIMARY};
        color: #FFFFFF;
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(118, 184, 42, 0.4);
    }}
    .stButton > button[kind="primary"]:hover {{
        box-shadow: 0 8px 25px rgba(74, 124, 27, 0.5);
        transform: translateY(-2px);
        color: #FFFFFF;
        border-color: {COR_SECONDARY};
    }}

    hr {{ margin: 2rem 0; border-color: rgba(255,255,255,0.1); opacity: 1; }}
    
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. ENGINE DE DADOS
# =========================================================
if 'page' not in st.session_state: 
    st.session_state.page = 'Dashboard'
if 'filtro_view' not in st.session_state:
    st.session_state.filtro_view = 'GERAL'

# Conexão com Google Sheets (Usado na área Adm)
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    try:
        # Lê os dados via CSV (Padrão para carregamento rápido e estável)
        return pd.read_csv(GSHEET_URL)
    except Exception as e:
        # Tenta fallback via conexão se o CSV direto falhar
        try:
            return conn.read(spreadsheet=GSHEET_URL, ttl=0)
        except Exception as e2:
            st.error(f"Erro ao conectar via CSV: {e}")
            return pd.DataFrame({
                'Mes_Ref': ['Erro'], 'Estado': ['SP'], 'Entrada': [0], 'Saida': [0], 'Saldo_Inicial': [0]
            })

# =========================================================
# 3. GRÁFICOS MODERNOS
# =========================================================
def plot_waterfall(df, saldo_ini):
    x = ["INICIAL"]; y = [saldo_ini]; measure = ["absolute"]; text = [f"<b>{saldo_ini}</b>"]
    for _, row in df.iterrows():
        m = str(row['Mes_Ref'])[:3].upper()
        x.append(f"{m}<br>Entrada"); y.append(row['Entrada']); measure.append("relative"); text.append(f"+{row['Entrada']}")
        x.append(f"{m}<br>Saída"); y.append(-row['Saida']); measure.append("relative"); text.append(str(row['Saida']))
    final = saldo_ini + df['Entrada'].sum() - df['Saida'].sum()
    x.append("FINAL"); y.append(0); measure.append("total"); text.append(f"<b>{final}</b>")
    
    fig = go.Figure(go.Waterfall(
        name="Fluxo", orientation="v", measure=measure, x=x, y=y, text=text, textposition="outside",
        connector={"line":{"color": COR_COCAL_GRAY, "width": 2}},
        decreasing={"marker":{"color": COR_COCAL_ORANGE, "line":{"width":0}}},
        increasing={"marker":{"color": COR_COCAL_GREEN, "line":{"width":0}}},
        totals={"marker":{"color": COR_COCAL_BLUE, "line":{"color":"#FFFFFF", "width":1}}}
    ))
    fig.update_traces(cliponaxis=False)
    
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=10, color=COR_COCAL_GREEN, symbol='square'), showlegend=True, name='Entradas (+)'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=10, color=COR_COCAL_ORANGE, symbol='square'), showlegend=True, name='Saídas (-)'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=10, color=COR_COCAL_BLUE, symbol='square'), showlegend=True, name='Totais'))
    
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Outfit', 'color': '#FFFFFF', 'size': 12}, margin=dict(t=60,b=0,l=0,r=0), height=500,
        showlegend=True, legend=dict(orientation="h", yanchor="top", y=1.15, xanchor="center", x=0.5,
        bgcolor='rgba(5, 10, 20, 0.8)', bordercolor='rgba(255, 255, 255, 0.2)', borderwidth=1, font=dict(color='#FFFFFF')),
        xaxis=dict(showgrid=False, color='#FFFFFF', tickfont=dict(color='#FFFFFF')), 
        yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.1)', color='#FFFFFF', tickfont=dict(color='#FFFFFF'))
    )
    return fig

def plot_evolution_bars(df):
    unique_months = df['Mes_Ref'].unique()
    df_sp = df[df['Estado'] == 'SP']
    sp_vals, sp_ent, sp_sai = [], [], []
    if not df_sp.empty:
        curr = df_sp.iloc[0]['Saldo_Inicial']
        for _, row in df_sp.iterrows():
            new_curr = curr + row['Entrada'] - row['Saida']
            sp_vals.append(new_curr)
            sp_ent.append(row['Entrada'])
            sp_sai.append(row['Saida'])
            curr = new_curr
            
    df_ms = df[df['Estado'] == 'MS']
    ms_vals, ms_ent, ms_sai = [], [], []
    if not df_ms.empty:
        curr = df_ms.iloc[0]['Saldo_Inicial']
        for _, row in df_ms.iterrows():
            new_curr = curr + row['Entrada'] - row['Saida']
            ms_vals.append(new_curr)
            ms_ent.append(row['Entrada'])
            ms_sai.append(row['Saida'])
            curr = new_curr

    fig = go.Figure()
    fig.add_trace(go.Bar(name='SP', x=unique_months, y=sp_vals, marker_color=COR_CHART_BLUE,
        text=[f"<b>{v}</b>" for v in sp_vals], textposition='outside', cliponaxis=False))
    fig.add_trace(go.Bar(name='MS', x=unique_months, y=ms_vals, marker_color=COR_PRIMARY,
        text=[f"<b>{v}</b>" for v in ms_vals], textposition='outside', cliponaxis=False))

    fig.update_layout(title="Evolução de Saldo", barmode='group', template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'family': 'Outfit', 'color': '#FFFFFF'},
        showlegend=True, legend=dict(orientation="h", y=1.1, x=1),
        xaxis=dict(showgrid=False, color='#FFFFFF'), yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.1)'),
        margin=dict(t=100, b=40, l=40, r=40), height=450)
    return fig

def plot_gauge(val):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=val, 
        number={'suffix':"%", 'font':{'size':40, 'color':'#FFFFFF', 'family': 'JetBrains Mono'}},
        gauge={'axis':{'range':[None, 100]}, 'bar':{'color': COR_COCAL_GREEN}, 'bgcolor':"rgba(255,255,255,0.05)"}))
    fig.update_layout(height=350, margin=dict(t=20,b=20,l=30,r=30), paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Outfit', 'color': '#FFFFFF'})
    return fig

# --- FRONT-END ---
st.markdown(f"""
<div class="header-container">
    <div class="app-title"><span style="font-size: 32px">📊</span> EVOLUÇÃO VAGAS | COCAL</div>
    <div class="app-subtitle">Painel de Gestão de Vagas</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.page == 'Dashboard':
    if st.button("⚙️ IR PARA ÁREA ADM", type='secondary'): 
        st.session_state.page = 'Admin'
        st.rerun()
else:
    if st.button("⬅️ VOLTAR AO DASHBOARD", type='primary'): 
        st.session_state.page = 'Dashboard'
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.page == 'Dashboard':
    st.markdown("### Visão Geral")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌍 CONSOLIDADO", use_container_width=True, type="primary" if st.session_state.filtro_view == "GERAL" else "secondary"):
            st.session_state.filtro_view = "GERAL"; st.rerun()
    with col2:
        if st.button("🏢 SÃO PAULO (SP)", use_container_width=True, type="primary" if st.session_state.filtro_view == "SP" else "secondary"):
            st.session_state.filtro_view = "SP"; st.rerun()
    with col3:
        if st.button("🌾 MATO GROSSO (MS)", use_container_width=True, type="primary" if st.session_state.filtro_view == "MS" else "secondary"):
            st.session_state.filtro_view = "MS"; st.rerun()
            
    st.markdown("<hr>", unsafe_allow_html=True)
    
    df = get_data()
    filtro = st.session_state.filtro_view
    if filtro == "SP": 
        df_view = df[df['Estado'] == 'SP']
        saldo_ini = df_view['Saldo_Inicial'].max() if not df_view.empty else 0
    elif filtro == "MS": 
        df_view = df[df['Estado'] == 'MS']
        saldo_ini = df_view['Saldo_Inicial'].max() if not df_view.empty else 0
    else: 
        df_view = df
        saldo_ini = (df[df['Estado'] == 'SP']['Saldo_Inicial'].max() or 0) + (df[df['Estado'] == 'MS']['Saldo_Inicial'].max() or 0)

    k_abertas = saldo_ini + df_view['Entrada'].sum()
    k_fechadas = df_view['Saida'].sum()
    k_saldo = k_abertas - k_fechadas
    k_efic = (k_fechadas/k_abertas*100) if k_abertas > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-card"><div class="metric-title"><span class="status-dot dot-blue"></span> VOLUME</div><div class="metric-value">{int(k_abertas) if pd.notna(k_abertas) else 0}</div><div class="metric-footer">Acumulado</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card"><div class="metric-title"><span class="status-dot dot-green"></span> CONTRATOS</div><div class="metric-value">{int(k_fechadas) if pd.notna(k_fechadas) else 0}</div><div class="metric-footer">{k_efic:.1f}% Eficiência</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card"><div class="metric-title"><span class="status-dot dot-orange"></span> BACKLOG</div><div class="metric-value">{int(k_saldo) if pd.notna(k_saldo) else 0}</div><div class="metric-footer">Em Aberto</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card"><div class="metric-title"><span class="status-dot dot-red"></span> SLA</div><div class="metric-value">41d</div><div class="metric-footer">Tempo Médio</div></div>', unsafe_allow_html=True)
        
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    df_chart = df_view.groupby('Mes_Ref', sort=False)[['Entrada', 'Saida']].sum().reset_index()
    st.plotly_chart(plot_waterfall(df_chart, saldo_ini), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_gauge, col_trend = st.columns(2)
    with col_gauge:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.plotly_chart(plot_gauge(k_efic), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_trend:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        st.plotly_chart(plot_evolution_bars(df), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="chart-panel" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#FFF;">🔐 Gestão de Dados</h2>', unsafe_allow_html=True)
    senha = st.text_input("SENHA", type="password")
    if senha == "gestao":
        df_atual = get_data()
        df_editado = st.data_editor(df_atual, num_rows="dynamic", use_container_width=True)
        if st.button("💾 SALVAR NO SHEETS", type="primary"):
            try:
                conn.update(spreadsheet=GSHEET_URL, data=df_editado, worksheet="FlowData")
                st.success("SALVO COM SUCESSO!"); st.rerun()
            except Exception as e: st.error(f"Erro: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

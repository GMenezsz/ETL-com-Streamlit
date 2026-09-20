import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Dashboard Faturamento | NorthPeak Retail Co.",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SELETOR DE TEMA (Dark / Light / System)
# ============================================================
with st.sidebar:
    st.markdown("### 🎨 Aparência")
    tema_escolhido = st.radio(
        "Tema do dashboard",
        options=["🌙 Dark", "☀️ Light", "💻 System"],
        index=0,
        horizontal=True,
        help="Escolha entre tema escuro, claro ou seguir o sistema operacional.",
    )

def detectar_tema_sistema():
    try:
        return st.context.theme.type  # "dark" ou "light"
    except Exception:
        return "dark"

if tema_escolhido == "🌙 Dark":
    tema_ativo = "dark"
elif tema_escolhido == "☀️ Light":
    tema_ativo = "light"
else:
    tema_ativo = detectar_tema_sistema()

# ============================================================
# PALETAS POR TEMA
# ============================================================
if tema_ativo == "dark":
    CORES = {
        "bg_app": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
        "bg_sidebar": "linear-gradient(180deg, #1e293b 0%, #0f172a 100%)",
        "card_bg": "rgba(255, 255, 255, 0.05)",
        "card_border": "rgba(255, 255, 255, 0.1)",
        "card_hover_border": "rgba(139, 92, 246, 0.5)",
        "card_hover_shadow": "rgba(139, 92, 246, 0.2)",
        "text_primary": "#ffffff",
        "text_secondary": "#94a3b8",
        "text_muted": "#64748b",
        "sidebar_text": "#e2e8f0",
        "plot_template": "plotly_dark",
        "plot_bg": "rgba(0,0,0,0)",
        "plot_font": "#e2e8f0",
        "plot_line": "#0f172a",
        "tab_bg": "rgba(255,255,255,0.03)",
        "tab_text": "#94a3b8",
        "dataframe_border": "rgba(255,255,255,0.08)",
    }
else:
    CORES = {
        "bg_app": "linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%)",
        "bg_sidebar": "linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%)",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "card_border": "rgba(99, 102, 241, 0.15)",
        "card_hover_border": "rgba(139, 92, 246, 0.6)",
        "card_hover_shadow": "rgba(139, 92, 246, 0.15)",
        "text_primary": "#0f172a",
        "text_secondary": "#475569",
        "text_muted": "#64748b",
        "sidebar_text": "#1e293b",
        "plot_template": "plotly_white",
        "plot_bg": "rgba(0,0,0,0)",
        "plot_font": "#0f172a",
        "plot_line": "#ffffff",
        "tab_bg": "rgba(15,23,42,0.04)",
        "tab_text": "#64748b",
        "dataframe_border": "rgba(15,23,42,0.08)",
    }

# ============================================================
# CSS DINÂMICO
# ============================================================
st.markdown(f"""
<style>
    .stApp {{
        background: {CORES['bg_app']};
    }}
    
    .main-header {{
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        padding: 2rem 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
    }}
    .main-header h1 {{
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        color: #ffffff !important;
    }}
    .main-header p {{
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-size: 1.1rem;
        color: #ffffff !important;
    }}
    
    .kpi-card {{
        background: {CORES['card_bg']};
        backdrop-filter: blur(10px);
        border: 1px solid {CORES['card_border']};
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        height: 100%;
    }}
    .kpi-card:hover {{
        transform: translateY(-5px);
        border-color: {CORES['card_hover_border']};
        box-shadow: 0 15px 30px {CORES['card_hover_shadow']};
    }}
    .kpi-label {{
        color: {CORES['text_secondary']};
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }}
    .kpi-value {{
        color: {CORES['text_primary']};
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .kpi-sub {{
        color: {CORES['text_muted']};
        font-size: 0.8rem;
        margin-top: 0.3rem;
    }}
    
    .section-title {{
        color: {CORES['text_primary']};
        font-size: 1.5rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        padding-left: 1rem;
        border-left: 4px solid #8b5cf6;
    }}
    .section-desc {{
        color: {CORES['text_secondary']};
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
        padding-left: 1rem;
    }}
    
    [data-testid="stSidebar"] {{
        background: {CORES['bg_sidebar']};
        border-right: 1px solid {CORES['dataframe_border']};
    }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {{
        color: {CORES['sidebar_text']};
    }}
    
    .stDownloadButton > button {{
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }}
    .stDownloadButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
        color: white !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: {CORES['tab_bg']};
        padding: 8px;
        border-radius: 12px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 8px;
        color: {CORES['tab_text']} !important;
        font-weight: 600;
        padding: 8px 20px;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white !important;
    }}
    .stTabs [aria-selected="true"] p {{
        color: white !important;
    }}
    
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {{
        color: {CORES['text_primary']};
    }}
    
    [data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid {CORES['dataframe_border']};
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CARREGAMENTO
# ============================================================
@st.cache_data
def carregar_dados():
    df = pd.read_csv("train.csv", encoding="utf-8")
    return df

try:
    tabela = carregar_dados()
except FileNotFoundError:
    st.error("❌ Arquivo `train.csv` não encontrado. Coloque o arquivo na mesma pasta do `app.py`.")
    st.stop()

# ============================================================
# PROCESSAMENTO
# ============================================================
df = tabela.drop(columns=["Ship Date", "Ship Mode", "Customer ID", 
                          "Segment", "Postal Code", "Product ID"])

faturamento_total = tabela["Sales"].sum()
venda_por_pedido = tabela.groupby("Order ID")["Sales"].sum()
ticket_medio = venda_por_pedido.mean()
total_pedidos = tabela["Order ID"].nunique()
total_clientes = tabela["Customer Name"].nunique() if "Customer Name" in tabela.columns else 0
total_produtos = tabela["Product Name"].nunique() if "Product Name" in tabela.columns else 0

fat_categoria = df[["Category", "Sales"]].groupby("Category").sum().reset_index()
fat_categoria = fat_categoria.sort_values("Sales", ascending=False)

fat_regiao = df[["Region", "Sales"]].groupby("Region").sum().reset_index()
fat_regiao = fat_regiao.sort_values("Sales", ascending=False)

df_moveis = df[df["Category"] == "Furniture"]
vendas_subcat_moveis = (
    df_moveis.groupby("Sub-Category")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

# ============================================================
# HELPERS
# ============================================================
def to_csv_bytes(dataframe: pd.DataFrame) -> bytes:
    return dataframe.to_csv(index=False).encode("utf-8-sig")

def fmt_moeda(valor):
    """Formata valor em Reais (R$)."""
    return f"R$ {valor:,.2f}"

def aplicar_tema_plotly(fig, titulo_size=16, altura=420, mostrar_legenda=False):
    fig.update_layout(
        template=CORES["plot_template"],
        paper_bgcolor=CORES["plot_bg"],
        plot_bgcolor=CORES["plot_bg"],
        font=dict(color=CORES["plot_font"], size=13),
        title_font_size=titulo_size,
        height=altura,
        showlegend=mostrar_legenda,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>📊 Dashboard Faturamento</h1>
    <p><b>NorthPeak Retail Co.</b> — Análise estratégica de vendas, categorias e desempenho regional</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR — FILTROS
# ============================================================
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🎛️ Filtros")
    st.markdown("Refine os dados para uma análise personalizada")
    
    categorias_disponiveis = sorted(df["Category"].unique().tolist())
    categorias_sel = st.multiselect(
        "Categorias", categorias_disponiveis, default=categorias_disponiveis
    )
    
    regioes_disponiveis = sorted(df["Region"].unique().tolist())
    regioes_sel = st.multiselect(
        "Regiões", regioes_disponiveis, default=regioes_disponiveis
    )
    
    st.markdown("---")
    st.markdown("### ℹ️ Sobre")
    st.markdown(
        "Dashboard desenvolvido com **Streamlit** + **Plotly** para análise interativa."
    )
    st.markdown(f"**Registros carregados:** {len(tabela):,}")
    st.markdown(f"**Tema ativo:** `{tema_ativo}`")

df_filt = df[
    (df["Category"].isin(categorias_sel)) & (df["Region"].isin(regioes_sel))
]

if df_filt.empty:
    st.warning("⚠️ Nenhum dado corresponde aos filtros selecionados.")
    st.stop()

# ============================================================
# KPIs
# ============================================================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">💰 Faturamento Total</div>
        <div class="kpi-value">{fmt_moeda(faturamento_total)}</div>
        <div class="kpi-sub">Soma global de todas as vendas</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">🎯 Ticket Médio</div>
        <div class="kpi-value">{fmt_moeda(ticket_medio)}</div>
        <div class="kpi-sub">Valor médio por pedido</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">🛒 Total de Pedidos</div>
        <div class="kpi-value">{total_pedidos:,}</div>
        <div class="kpi-sub">Pedidos únicos realizados</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">👥 Clientes Únicos</div>
        <div class="kpi-value">{total_clientes:,}</div>
        <div class="kpi-sub">Base de clientes ativos</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# ABAS
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🏷️ Categorias", 
    "🌎 Regiões", 
    "🪑 Móveis (Subcategoria)",
    "📋 Dados Brutos"
])

# ------------------------------------------------------------
# ABA 1 — CATEGORIAS
# ------------------------------------------------------------
with tab1:
    st.markdown('<div class="section-title">Faturamento por Categoria</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Distribuição do faturamento entre as categorias de produtos.</div>', unsafe_allow_html=True)
    
    fat_cat_filt = df_filt[["Category", "Sales"]].groupby("Category").sum().reset_index()
    fat_cat_filt = fat_cat_filt.sort_values("Sales", ascending=False)
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        fig_donut = px.pie(
            fat_cat_filt,
            names="Category",
            values="Sales",
            hole=0.55,
            title="Distribuição percentual por categoria",
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig_donut.update_traces(
            textposition="outside",
            textinfo="percent+label",
            textfont_size=13,
            marker=dict(line=dict(color=CORES["plot_line"], width=2)),
            hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
        )
        aplicar_tema_plotly(fig_donut, altura=420, mostrar_legenda=True)
        fig_donut.update_layout(legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_donut, use_container_width=True)
    
    with col_b:
        fig_bar_cat = px.bar(
            fat_cat_filt,
            x="Category",
            y="Sales",
            color="Category",
            text="Sales",
            title="Faturamento absoluto por categoria",
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig_bar_cat.update_traces(
            texttemplate="R$ %{text:,.0f}",
            textposition="outside",
            marker_line_color=CORES["plot_line"],
            marker_line_width=1.5,
            hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>",
        )
        aplicar_tema_plotly(fig_bar_cat, altura=420)
        fig_bar_cat.update_layout(yaxis_title="Faturamento (R$)", xaxis_title="")
        st.plotly_chart(fig_bar_cat, use_container_width=True)
    
    st.markdown("##### 📄 Tabela detalhada")
    fat_cat_display = fat_cat_filt.copy()
    fat_cat_display["Sales"] = fat_cat_display["Sales"].apply(fmt_moeda)
    st.dataframe(fat_cat_display, use_container_width=True, hide_index=True)
    
    st.download_button(
        "⬇️ Baixar CSV — Faturamento por Categoria",
        data=to_csv_bytes(fat_cat_filt),
        file_name="Faturamento_categoria.csv",
        mime="text/csv",
        key="dl_categoria",
    )

# ------------------------------------------------------------
# ABA 2 — REGIÕES
# ------------------------------------------------------------
with tab2:
    st.markdown('<div class="section-title">Faturamento por Região</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Comparativo do desempenho de vendas em cada região geográfica.</div>', unsafe_allow_html=True)
    
    fat_reg_filt = df_filt[["Region", "Sales"]].groupby("Region").sum().reset_index()
    fat_reg_filt = fat_reg_filt.sort_values("Sales", ascending=True)
    
    fig_bar_reg = px.bar(
        fat_reg_filt,
        x="Sales",
        y="Region",
        orientation="h",
        color="Sales",
        text="Sales",
        title="Faturamento por região",
        color_continuous_scale="Viridis",
    )
    fig_bar_reg.update_traces(
        texttemplate="R$ %{text:,.0f}",
        textposition="outside",
        marker_line_color=CORES["plot_line"],
        marker_line_width=1.5,
        hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f}<extra></extra>",
    )
    aplicar_tema_plotly(fig_bar_reg, altura=400)
    fig_bar_reg.update_layout(coloraxis_showscale=False, xaxis_title="Faturamento (R$)", yaxis_title="")
    st.plotly_chart(fig_bar_reg, use_container_width=True)
    
    st.markdown("##### 📄 Tabela detalhada")
    fat_reg_display = fat_reg_filt.sort_values("Sales", ascending=False).copy()
    fat_reg_display["Sales"] = fat_reg_display["Sales"].apply(fmt_moeda)
    st.dataframe(fat_reg_display, use_container_width=True, hide_index=True)
    
    st.download_button(
        "⬇️ Baixar CSV — Faturamento por Região",
        data=to_csv_bytes(fat_reg_filt.sort_values("Sales", ascending=False)),
        file_name="Faturamento_regiao.csv",
        mime="text/csv",
        key="dl_regiao",
    )

# ------------------------------------------------------------
# ABA 3 — MÓVEIS
# ------------------------------------------------------------
with tab3:
    st.markdown('<div class="section-title">Vendas de Móveis por Subcategoria</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Detalhamento das vendas dentro da categoria <b>Furniture</b>.</div>', unsafe_allow_html=True)
    
    df_mov_filt = df_filt[df_filt["Category"] == "Furniture"]
    
    if df_mov_filt.empty:
        st.info("ℹ️ Nenhum dado de móveis para os filtros selecionados.")
    else:
        subcat_filt = (
            df_mov_filt.groupby("Sub-Category")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
        )
        
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            fig_bar_mov = px.bar(
                subcat_filt.sort_values("Sales", ascending=True),
                x="Sales",
                y="Sub-Category",
                orientation="h",
                color="Sales",
                text="Sales",
                title="Faturamento por subcategoria de móveis",
                color_continuous_scale="Plasma",
            )
            fig_bar_mov.update_traces(
                texttemplate="R$ %{text:,.0f}",
                textposition="outside",
                marker_line_color=CORES["plot_line"],
                marker_line_width=1.5,
                hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f}<extra></extra>",
            )
            aplicar_tema_plotly(fig_bar_mov, altura=430)
            fig_bar_mov.update_layout(coloraxis_showscale=False, xaxis_title="Faturamento (R$)", yaxis_title="")
            st.plotly_chart(fig_bar_mov, use_container_width=True)
        
        with col2:
            fig_donut_mov = px.pie(
                subcat_filt,
                names="Sub-Category",
                values="Sales",
                hole=0.5,
                title="Participação das subcategorias",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig_donut_mov.update_traces(
                textposition="outside",
                textinfo="percent+label",
                textfont_size=12,
                marker=dict(line=dict(color=CORES["plot_line"], width=2)),
                hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
            )
            aplicar_tema_plotly(fig_donut_mov, altura=430)
            st.plotly_chart(fig_donut_mov, use_container_width=True)
        
        st.markdown("##### 📄 Tabela detalhada")
        subcat_display = subcat_filt.copy()
        subcat_display["Sales"] = subcat_display["Sales"].apply(fmt_moeda)
        st.dataframe(subcat_display, use_container_width=True, hide_index=True)
        
        st.download_button(
            "⬇️ Baixar CSV — Vendas de Móveis",
            data=to_csv_bytes(subcat_filt),
            file_name="relatorio_moveis.csv",
            mime="text/csv",
            key="dl_moveis",
        )

# ------------------------------------------------------------
# ABA 4 — DADOS BRUTOS
# ------------------------------------------------------------
with tab4:
    st.markdown('<div class="section-title">Base de Dados Filtrada</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Visualize e baixe os dados já filtrados pela sidebar.</div>', unsafe_allow_html=True)
    
    st.dataframe(df_filt, use_container_width=True, height=500)
    
    st.download_button(
        "⬇️ Baixar CSV — Base Filtrada Completa",
        data=to_csv_bytes(df_filt),
        file_name="base_filtrada.csv",
        mime="text/csv",
        key="dl_base",
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown(f"""
<div style="text-align:center; color:{CORES['text_muted']}; padding:2rem 0 1rem 0; font-size:0.85rem;">
    📊 <b>NorthPeak Retail Co.</b> — Dashboard de Faturamento · 
    Desenvolvido com Streamlit + Plotly
</div>
""", unsafe_allow_html=True)
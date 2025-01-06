import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial da página
st.set_page_config(
    page_title="Dashboard Interativa",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar dados
def carregar_dados(caminho):
    return pd.read_excel(caminho)

df = carregar_dados("dados.xlsx")

# Título da Dashboard
st.title("Dashboard Interativa de Análise de Dados")

# Sidebar para filtros
st.sidebar.header("Filtros")

# Filtro por categorias (assumindo que existe uma coluna 'Categoria')
categorias = st.sidebar.multiselect(
    "Selecione as categorias:",
    options=df['Categoria'].unique(),
    default=df['Categoria'].unique()
)

# Filtro por período (assumindo que existe uma coluna 'Data')
data_inicio = st.sidebar.date_input(
    "Data inicial:",
    value=pd.to_datetime(df['Data']).min()
)
data_fim = st.sidebar.date_input(
    "Data final:",
    value=pd.to_datetime(df['Data']).max()
)

# Aplicar filtros aos dados
filtro_df = df[(df['Categoria'].isin(categorias)) &
               (pd.to_datetime(df['Data']) >= data_inicio) &
               (pd.to_datetime(df['Data']) <= data_fim)]

# Visualização de KPIs
st.subheader("Indicadores principais")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Vendas", f"R$ {filtro_df['Vendas'].sum():,.2f}")

with col2:
    st.metric("Média de Vendas", f"R$ {filtro_df['Vendas'].mean():,.2f}")

with col3:
    st.metric("Registros", filtro_df.shape[0])

# Gráficos interativos
st.subheader("Análises Visuais")

# Gráfico de Barras
fig_bar = px.bar(
    filtro_df,
    x='Categoria',
    y='Vendas',
    color='Categoria',
    title="Vendas por Categoria",
    labels={'Vendas': 'Total de Vendas', 'Categoria': 'Categoria'},
    template="plotly_white"
)
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de Linha (Assumindo que há uma coluna 'Data')
fig_line = px.line(
    filtro_df,
    x='Data',
    y='Vendas',
    title="Tendência de Vendas ao Longo do Tempo",
    template="plotly_white",
    markers=True
)
st.plotly_chart(fig_line, use_container_width=True)

# Tabela de dados filtrados
st.subheader("Dados Filtrados")
st.dataframe(filtro_df)

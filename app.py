
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from io import BytesIO

# Carregando os dados
df = pd.read_excel("produtividadeGifDetalhe - 2025-04-08T173820.091.xlsx")
df["Data Auditoria"] = pd.to_datetime(df["Data Auditoria"], errors='coerce', dayfirst=True)

# Sidebar - Filtros
st.sidebar.header("Filtros")
convenios = st.sidebar.multiselect("Convênio", options=df['Convenio'].unique(), default=df['Convenio'].unique())
auditores = st.sidebar.multiselect("Auditor", options=df['Auditor'].unique(), default=df['Auditor'].unique())
motivos = st.sidebar.multiselect("Motivo Auditoria", options=df['Motivo Auditoria'].unique(), default=df['Motivo Auditoria'].unique())
data_inicio = st.sidebar.date_input("Data Inicial", value=df["Data Auditoria"].min().date())
data_fim = st.sidebar.date_input("Data Final", value=df["Data Auditoria"].max().date())

# Aplicando os filtros
filtro_df = df[(df['Convenio'].isin(convenios)) &
               (df['Auditor'].isin(auditores)) &
               (df['Motivo Auditoria'].isin(motivos)) &
               (df['Data Auditoria'].dt.date >= data_inicio) &
               (df['Data Auditoria'].dt.date <= data_fim)]

# Dados processados
auditoria_por_convenio = filtro_df['Convenio'].value_counts().reset_index()
auditoria_por_convenio.columns = ['Convenio', 'Total Auditorias']

valores_totais = filtro_df[['Valor de Inclusoes', 'Valor Maior', 'Valor Menor', 'Valor Exclusoes']].sum()

tipo_acao_freq = filtro_df['Tipo de acao'].value_counts().reset_index()
tipo_acao_freq.columns = ['Tipo de Ação', 'Frequência']

motivos_freq = filtro_df['Motivo Auditoria'].value_counts().head(10).reset_index()
motivos_freq.columns = ['Motivo', 'Frequência']

# Streamlit app
st.set_page_config(layout="wide")
st.title("Painel de Eficiência da Auditoria")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Convênios por Auditorias")
    st.bar_chart(auditoria_por_convenio.head(10).set_index("Convenio"))

with col2:
    st.subheader("Totais Financeiros Auditados")
    st.bar_chart(valores_totais)

st.subheader("Tipos de Ação Mais Frequentes")
st.bar_chart(tipo_acao_freq.set_index("Tipo de Ação"))

st.subheader("Top 10 Motivos de Auditoria")
st.bar_chart(motivos_freq.set_index("Motivo"))

# Exportação dos dados filtrados
st.sidebar.markdown("---")
st.sidebar.subheader("Exportar Dados")

@st.cache_data
def to_excel(dataframe):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    dataframe.to_excel(writer, index=False, sheet_name='Dados Filtrados')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

excel_data = to_excel(filtro_df)
st.sidebar.download_button(label="📥 Baixar Excel", data=excel_data, file_name='auditoria_filtrada.xlsx')

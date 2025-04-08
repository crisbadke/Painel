import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from io import BytesIO
import re

st.set_page_config(layout="wide")
st.title("Painel de Eficiência da Auditoria")

# Upload do arquivo
uploaded_file = st.sidebar.file_uploader("📁 Envie seu arquivo Excel de auditoria", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, dtype=str)

    # Traduz os meses abreviados em português para números
    meses_pt = {
        "jan": "01", "fev": "02", "mar": "03", "abr": "04",
        "mai": "05", "jun": "06", "jul": "07", "ago": "08",
        "set": "09", "out": "10", "nov": "11", "dez": "12"
    }

    def traduz_data_pt(data_str):
    if isinstance(data_str, str):
        data_str = data_str.lower()
        data_str = re.sub(r"de", "", data_str)  # remove "de"
        data_str = re.sub(r"[.]", "", data_str)  # remove ponto final
        for mes_pt, num in meses_pt.items():
            data_str = re.sub(f"\b{mes_pt}\b", num, data_str)
        return data_str.strip()
    return data_str

    if "Data Auditoria" in df.columns:
        df["Data Auditoria"] = df["Data Auditoria"].apply(traduz_data_pt)
        try:
            df["Data Auditoria"] = pd.to_datetime(df["Data Auditoria"], errors='coerce', dayfirst=True)
        except Exception as e:
            st.error(f"Erro ao converter datas: {e}")

        if df["Data Auditoria"].notna().sum() == 0:
            st.error("⚠️ Nenhuma data válida encontrada na coluna 'Data Auditoria'. Verifique o arquivo.")
        else:
            # Sidebar - Filtros
            st.sidebar.header("Filtros")
            convenios = st.sidebar.multiselect("Convênio", options=df['Convenio'].unique(), default=df['Convenio'].unique())
            auditores = st.sidebar.multiselect("Auditor", options=df['Auditor'].unique(), default=df['Auditor'].unique())
            motivos = st.sidebar.multiselect("Motivo Auditoria", options=df['Motivo Auditoria'].unique(), default=df['Motivo Auditoria'].unique())

            data_min = df["Data Auditoria"].min().date()
            data_max = df["Data Auditoria"].max().date()
            data_inicio = st.sidebar.date_input("Data Inicial", value=data_min)
            data_fim = st.sidebar.date_input("Data Final", value=data_max)

            # Aplicando os filtros
            filtro_df = df[(df['Convenio'].isin(convenios)) &
                           (df['Auditor'].isin(auditores)) &
                           (df['Motivo Auditoria'].isin(motivos)) &
                           (df['Data Auditoria'].dt.date >= data_inicio) &
                           (df['Data Auditoria'].dt.date <= data_fim)]

            # Dados processados
            auditoria_por_convenio = filtro_df['Convenio'].value_counts().reset_index()
            auditoria_por_convenio.columns = ['Convenio', 'Total Auditorias']

            valores_totais = filtro_df[['Valor de Inclusoes', 'Valor Maior', 'Valor Menor', 'Valor Exclusoes']].apply(pd.to_numeric, errors='coerce').sum()

            tipo_acao_freq = filtro_df['Tipo de acao'].value_counts().reset_index()
            tipo_acao_freq.columns = ['Tipo de Ação', 'Frequência']

            motivos_freq = filtro_df['Motivo Auditoria'].value_counts().head(10).reset_index()
            motivos_freq.columns = ['Motivo', 'Frequência']

            # Layout visual
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
    else:
        st.error("❌ A coluna 'Data Auditoria' não foi encontrada no arquivo. Verifique o cabeçalho.")
else:
    st.warning("⚠️ Por favor, envie um arquivo Excel para visualizar o painel.")

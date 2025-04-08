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
def traduz_data_pt(data_str):
    if isinstance(data_str, str):
        data_str = data_str.lower()
        data_str = re.sub(r"de", "", data_str)  # remove "de"
        data_str = re.sub(r"[.]", "", data_str)  # remove ponto final
        for mes_pt, num in meses_pt.items():
            data_str = re.sub(f"\\b{mes_pt}\\b", num, data_str)
        return data_str.strip()
    return data_str

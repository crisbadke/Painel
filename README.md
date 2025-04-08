# 📊 Painel de Eficiência da Auditoria

Este painel interativo em Streamlit permite visualizar e filtrar auditorias por convênio, auditor, motivo e período, além de exportar os dados filtrados.

---

## ▶️ Como rodar

### 1. Instale o Streamlit e dependências

```bash
pip install -r requirements.txt
```

### 2. Rode o painel

```bash
streamlit run app.py
```

---

## 📥 Funcionalidades

- Filtros por:
  - Convênio
  - Auditor
  - Motivo da Auditoria
  - Período da Auditoria
- Upload direto de arquivos `.xlsx` (Excel)
- Gráficos interativos com Streamlit
- Exportação para Excel dos dados filtrados

---

## ⚠️ Como usar no Streamlit Cloud

1. Crie um repositório no GitHub com os arquivos deste projeto
2. Acesse [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Clique em **“New app”**, selecione o repositório e o arquivo `app.py`
4. Após o deploy, o usuário poderá fazer upload do seu próprio Excel pelo navegador

---

## 📝 Observação

Seu Excel deve conter pelo menos as seguintes colunas:

- `Convenio`
- `Auditor`
- `Motivo Auditoria`
- `Data Auditoria`
- `Valor de Inclusoes`, `Valor Maior`, `Valor Menor`, `Valor Exclusoes`
- `Tipo de acao`


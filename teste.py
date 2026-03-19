import streamlit as st
import pandas as pd
from datetime import timedelta

# carregar dados
url = "https://docs.google.com/spreadsheets/d/1UyhCy0dHzduhWemsv7Mc2OzeRAPQGM3Zahp1y4CXH0k/export?format=csv&gid=1612666831"
df = pd.read_csv(url)

df.columns = ['codigo','hub','transportadora','qnt','data','drive','observacao']
df['observacao'] = df['observacao'].fillna(0)

df = df.dropna()

df['qnt'] = df['qnt'].astype(int)
df['data'] = pd.to_datetime(df['data'] + "/2026", format="%d/%m/%Y")
df['qnt'] = df['qnt'].astype(int)

st.title("Dashboard de Romaneios")

# -----------------------
# FILTRO DE PERÍODO
# -----------------------

periodo = st.selectbox(
    "Período",
    ["Hoje","Últimos 7 dias","Últimos 30 dias","Personalizado"]
)

hoje = df["data"].max()

if periodo == "Hoje":
    data_inicio = hoje
    data_fim = hoje

elif periodo == "Últimos 7 dias":
    data_inicio = hoje - timedelta(days=7)
    data_fim = hoje

elif periodo == "Últimos 30 dias":
    data_inicio = hoje - timedelta(days=30)
    data_fim = hoje

else:
    data_inicio, data_fim = st.date_input(
        "Selecione o período",
        (df["data"].min(), df["data"].max())
    )
    data_inicio = pd.to_datetime(data_inicio)
    data_fim = pd.to_datetime(data_fim)

df_filtrado = df[
    (df["data"] >= data_inicio) &
    (df["data"] <= data_fim)
]

# -----------------------
# MÉTRICAS
# -----------------------

col1, col2, col3 = st.columns(3)

col1.metric("Total de Romaneios", len(df_filtrado))
col2.metric("Total de Volumes", df_filtrado["qnt"].sum())
col3.metric("Transportadoras", df_filtrado["transportadora"].nunique())

# -----------------------
# GRÁFICO
# -----------------------

st.subheader("Volumes por Transportadora")

grafico = (
    df_filtrado
    .groupby("transportadora")["qnt"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(grafico)

# -----------------------
# TABELA
# -----------------------

st.subheader("Tabela de Romaneios")

st.dataframe(
    df_filtrado.sort_values("data", ascending=False),
    use_container_width=True
)
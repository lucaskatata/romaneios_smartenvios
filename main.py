# %%
import pandas as pd
import streamlit as st
from datetime import timedelta

url = 'https://docs.google.com/spreadsheets/d/1UyhCy0dHzduhWemsv7Mc2OzeRAPQGM3Zahp1y4CXH0k/export?format=csv&gid=1612666831#gid=1612666831'
# %%
st.title('Romaneios')
df = pd.read_csv(url)

df.columns = ['codigo', 'hub', 'transportadora', 'qnt', 'data', 'drive', 'observacao', 'coluna1']
df = df.drop(columns=['coluna1'])

df['data'] = pd.to_datetime(df['data'] + "/2026", format='%d/%m/%Y')
# df['data_formatada'] = df['data'].dt.strftime("%d/%m/%Y")

df['observacao'] = df['observacao'].fillna(0)

df = df.dropna()

df['qnt'] = df['qnt'].astype(int)

# %%
datas = sorted(df['data'].unique(),reverse=True)

# dia = col1.selectbox('Dia', datas, format_func=lambda x: x.strftime("%d/%m/%Y"))

# dia = '2026-03-12'
# %%
periodo = st.selectbox(
    'Período',
    ['Hoje', 'Últimos 7 dias', 'Últimos 30 dias', 'Personalizado']
)

hoje = df['data'].max()

if periodo == 'Hoje':
    data_inicio = hoje
    data_final = hoje

elif periodo == 'Últimos 7 dias':
    data_inicio = hoje - timedelta(days = 7)
    data_final = hoje

elif periodo == 'Últimos 30 dias':
    data_inicio = hoje - timedelta(days = 30)
    data_final = hoje

elif periodo == 'Personalizado':
    data_inicio, data_final = st.date_input(
        'Selecione o período',
        (df['data'].min(), df['data'].max())
    )
    data_inicio = pd.to_datetime(data_inicio)
    data_final = pd.to_datetime(data_final)

df_filtrado_dia = df[
    (df['data'] >= pd.to_datetime(data_inicio)) & 
    (df['data'] <=  pd.to_datetime(data_final))]

if periodo == 'Hoje':
    st.subheader(f'Dados de {hoje.strftime('%d/%m/%Y')}')
else:
    st.subheader(
        f"Dados de {data_inicio.strftime('%d/%m/%Y')} até {data_final.strftime('%d/%m/%Y')}"
    )

col1, col2, col3, col4 = st.columns(4)

quantidade_romaneio = df_filtrado_dia['codigo'].count()

transportadoras = sorted(df_filtrado_dia['transportadora'].unique())
for transportadora in transportadoras:
    quantidade = df_filtrado_dia[df_filtrado_dia['transportadora'] == transportadora]['qnt'].sum()
    st.text(f'{transportadora.title()}: {quantidade}')
col1.metric(label='Total', value=df_filtrado_dia['qnt'].sum())
col2.metric(label='Quantidade de romaneios', value=quantidade_romaneio)
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Dados",
    page_icon="🏃🏼",
    layout="wide"
)

df = st.session_state["data"]

tipos='Todos'
tipos = np.append(tipos,df["Data"].unique())
tipo = st.sidebar.selectbox("Data", tipos)
st.sidebar.markdown("Desenvolvido por Vinicius P. Silva [LinkedIn](https://www.linkedin.com/in/-vini-silva/)")

if tipo == 'Todos':
    df_filtered = df
else:
    df_filtered = df[(df["Data"]==tipo)]

#df_filtered
st.dataframe(df_filtered,
             column_config={
                 "Data": st.column_config.ProgressColumn(
                     "Data", format="%f", min_value=0, max_value=int(df_filtered["Data"].max()))
                 })
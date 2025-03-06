import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.app_logo import add_logo

if "data" not in st.session_state:
    df = pd.read_excel("software_inteligencia_mercado.xlsx", index_col=None)
    df = df.sort_values(by="Reach", ascending=False)
    st.session_state["data"] = df

# Configuração da página
st.set_page_config(page_title="Vinicius P Silva", layout="wide")
st.sidebar.markdown("Desenvolvido por Vinicius P. Silva [LinkedIn](https://www.linkedin.com/in/-vini-silva/)")

# Adicionando logo com streamlit-extras
# add_logo("logo.jpeg")

# Adicionando o logo
st.logo("eu.jpg")

# Adicionando o logo no body
st.image("eu.jpg", width=150)

st.title("Vinicius P. Silva")
st.write("Bem-vindo ao meu portfólio! Aqui você encontra projetos de Data Science, Machine Learning e Estatística. Fique à vontade para explorar e entrar em contato para mais informações.")

st.write("## Projetos")

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Dados",
    page_icon="🏃🏼",
    layout="wide"
)

st.logo("eu.jpg")

# Adicionando o logo no body
st.image("eu.jpg", width=150)


st.write("## Experiências 🎯")
st.write("""
#### Dublagem em inglês: 
Gravadora Argila

---
#### Child Care: 
Pan American Christian Academy 

---
#### Teacher assistant:
Chapel School

---
#### Sites e Web Development: 
Freelance 

---
#### Sonoplastia:
PIBS

---
""")

st.write("## Projetos 🛠")
st.write("""

Veja meus projetos
[GitHub](https://github.com/vinirex)

---

""")

st.write("## Idiomas 🌎")
st.write("""
- Português(Nativo)
- Inglês(Fluente)
- Fraçes(Básico)
""")
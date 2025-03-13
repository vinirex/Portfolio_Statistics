import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotnine import *


if "data" not in st.session_state:
    df = pd.read_excel("Exportação_Brasileira_Anual.xlsx", index_col=None)
    df = df.sort_values(by="Data", ascending=False)
    st.session_state["data"] = df

# Configuração da página
st.set_page_config(page_title="Dashboard de Distribuições Probabilísticas", layout="wide")

# Adicionando o logo
st.logo("eu.jpg")

# Adicionando o logo
st.image("eu.jpg", width=150)

# Criando as sub-abas (pages)
pages = st.sidebar.selectbox("Escolha o que quer ver:", [
    "Dados",
    "Analise seus Dados"
])

st.sidebar.markdown("Desenvolvido por Vinicius P. Silva [LinkedIn](https://www.linkedin.com/in/-vini-silva/)")

# Função para exibir gráfico Plotly
def plot_distribution(x, y, title, xlabel, ylabel):
    fig = go.Figure(data=[go.Bar(x=x, y=y)])
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel)
    st.plotly_chart(fig)



if pages == "Dados":

        st.title("Apresentação dos dados")
        df = st.session_state["data"]

        tipos='Todos'
        tipos = np.append(tipos,df["Data"].unique())
        tipo = st.sidebar.selectbox("Filtros", tipos)

        if tipo == 'Todos':
            df_filtered = df
        else:
            df_filtered = df[(df["Data"]==tipo)]

        #df_filtered
        st.dataframe(df_filtered,
                    column_config={
                        "Valor_BK": st.column_config.ProgressColumn(
                            "Valor_BK", format="%.2f", min_value=0, max_value=int(df_filtered["Valor_BK"].max()))
                        })

        st.write("""
        # Explicação sobre o conjunto de dados
        O conjunto de dados contém informações sobre a exportação brasileira anual. Cada linha representa um ano e inclui valores financeiros e variações percentuais associadas a diferentes categorias de exportação.

        ## Identificação do tipo das variáveis
        - **Data (Ano)**: Variável **quantitativa discreta**, representa o ano de referência.
        - **Valor_BK, Valor_BI, Valor_BC, Valor_CL**: Variáveis **quantitativas contínuas**, representam valores monetários de diferentes categorias de exportação.
        - **VarBK, VarBI, VarBC, VarCL**: Variáveis **quantitativas contínuas**, representam a variação percentual anual de cada categoria.
        - **Part_BK, Part_BI, Part_BC, Part_CL**: Variáveis **quantitativas contínuas**, representam a participação percentual de cada categoria no total.

        ## Principais perguntas de análise
        1. Como evoluíram os valores das exportações ao longo dos anos?
        2. Quais setores apresentaram maior crescimento ou queda em determinados períodos?
        3. Como as variações percentuais refletem mudanças econômicas no Brasil?
        4. Qual categoria tem maior participação nas exportações ao longo do tempo?
        5. Existem padrões cíclicos ou tendências de longo prazo nos dados?
        """)



elif pages == "Analise seus Dados":
    st.header("Análisando os Dados")
    
    df = pd.read_excel("Exportação_Brasileira_Anual.xlsx", index_col=None)
    st.write("Amostra dos dados:")
    st.write(df.head())


    st.write("""

    ## Escolha de Distribuições Estatísticas📊

    Com base no conjunto de dados, foram excolhidas as distribuições **Normal** e **Poisson** para análise.

    ### Justificativa das escolhas  

    1. **Distribuição Normal**  
    - Os valores das exportações (**Valor_BK, Valor_BI, etc.**) representam grandezas contínuas e podem seguir uma distribuição aproximadamente normal, especialmente se considerarmos um grande período de tempo.  
    - Muitas variáveis econômicas tendem a seguir uma distribuição normal devido ao efeito da soma de múltiplos fatores independentes (Teorema do Limite Central).  

    2. **Distribuição de Poisson**  
    - Se estivermos analisando eventos raros, como crises econômicas que afetam drasticamente as exportações, a distribuição de Poisson pode ser útil.  
    - Essa distribuição é usada para modelar a contagem de eventos que ocorrem em um intervalo de tempo, o que pode ser interessante para estudar a frequência de anos com quedas abruptas nas exportações.

    ### Veja abaixo a análise 👇🏾


    """)

    
        
    colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    if colunas_numericas:
        coluna_escolhida = st.selectbox("Escolha uma coluna: ", "Valor_BK")
        
        if coluna_escolhida:
            st.write("Resumo dos dados:")
            st.write(df[coluna_escolhida].describe())
            
            dist = st.selectbox("Escolha a distribuição para análise:", ["Poisson", "Normal"])
            
            if dist == "Poisson":
                
                col1, col2 = st.columns([0.3,0.7])
                
                lambda_est = df[coluna_escolhida].mean()

                x_min = col1.number_input("Número mínimo de eventos",value=11000)
                x_max = col1.number_input("Número máximo de eventos desejado",value= 14000)
                
                x = np.arange(x_min, x_max)
                y = stats.poisson.pmf(x, lambda_est)
                y_cdf = stats.poisson.cdf(x,lambda_est)

                df_poisson = pd.DataFrame({"X": x, "P(X)": y, "P(X ≤ k) (Acumulado)": np.cumsum(y),"P(X > k) (Acumulado Cauda Direita)": 1-np.cumsum(y)}).set_index("X")

                col2.write("Tabela de probabilidades:")
                col2.write(df_poisson)
                
                st.subheader(f"Estimativa de λ (Taxa média de Ocorrência): {lambda_est:.2f}")
                prob_acum = st.toggle("Probabilidade Acumulada")
                if prob_acum:
                    st.write("Probabilidades 'somadas' desde a origem!")
                    y_selec = y_cdf
                    fig = go.Figure(data=[go.Line(x=x, y=y_selec)])
                    fig.update_layout(title="Distribuição de Poisson Acumulada", xaxis_title="Número de eventos", yaxis_title="Probabilidade Acumulada")
                    st.plotly_chart(fig)
                else:
                    y_selec = y
                    plot_distribution(x, y_selec, "Distribuição de Poisson", "Número de eventos", "Probabilidade")
                


                
            elif dist == "Normal":
                
                n = df[coluna_escolhida].count()
                mu_est = df[coluna_escolhida].mean()
                sigma_est = df[coluna_escolhida].std()
                st.subheader(f"Estimativa de μ: {mu_est:.2f}, σ: {sigma_est:.2f}")


                # Create distplot with custom bin_size
                #colunas_categoricas = df.select_dtypes(include=[np.character]).#columns.tolist()
                
                #st.selectbox("Escolha uma variável qualitativa",colunas_categoricas)


                hist_data = [df[coluna_escolhida].dropna().tolist()]
                group_labels=['distplot']
                b_size = st.number_input("Largura de Classe - Histograma",min_value=0.1,value=10000.0)

                fig = ff.create_distplot(
                    hist_data, group_labels, bin_size=b_size)
                
                teorica = True
                if teorica:

                    # Adicionando a curva da distribuição normal teórica com média e desvio padrão da amostra
                    x = np.linspace(mu_est - 4*sigma_est, mu_est + 4*sigma_est, 100)
                    y = stats.norm.pdf(x, mu_est, sigma_est)

                    # Criando um trace da curva normal
                    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Curva Normal', line=dict(color='red')))
                
                st.plotly_chart(fig)

                p = ggplot(df, aes(sample=coluna_escolhida)) + geom_qq(size=3,colour='red',alpha=0.7) + geom_qq_line()+theme_bw()+labs(x="Quantis Teóricos",y = "Quantis Amostrais", title="Gráfico QQPlot")
                st.pyplot(ggplot.draw(p))
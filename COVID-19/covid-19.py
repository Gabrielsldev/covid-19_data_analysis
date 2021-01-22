import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

import sys
import os
#
# if not os.path.exists("imagens"):
#     os.mkdir("imagens")

lista_completa_args = sys.argv
lista_args = lista_completa_args[1:]

if len(lista_args) == 2:
    arquivo_csv = lista_args[0]
    condicao_mapa = lista_args[1]
elif len(lista_args) == 1:
    arquivo_csv = lista_args[0]
else:
    print("Erro: Forneça o nome do arquivo CSV como primeiro argumento.")
    print("Caso queria o mapa do Brasil com o número de óbitos, insira o argumento -mapa")
    exit()


# Após análise do arquivo CSV, é necessário utilizar o parâmetro "sep=';'", pois o separador utilizado é o ;
df = pd.read_csv(arquivo_csv, sep=";")
df_copy = df.copy()

# Pega a última data disponível no dataset e atribui a uma variável que será usada em algumas funções.
ultima_data = df_copy["data"].iloc[-1]


# Cria um dataframe com os casos acumulados no Brasil


def CasosAcumuladosBr():
    casos_acumulados_br = df_copy[["regiao", "casosAcumulado", "data"]]
    casos_acumulados_br = casos_acumulados_br[casos_acumulados_br["regiao"] == "Brasil"].rename(columns={
        "casosAcumulado":"Casos Acumulados (Brasil)", "data":"Data"})
    casos_acumulados_br.set_index("Data", inplace=True)

    return casos_acumulados_br


# Cria um gráfico de linha com os casos acumulados no país.


def GraficoCasosAcumBR():
    fig = px.line(x=CasosAcumuladosBr().index,
                  y=CasosAcumuladosBr()["Casos Acumulados (Brasil)"],
                  title='Casos Acumulados de COVID-19 no Brasil')
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Casos Acumulados (Brasil)")

    return fig.show()

# Cria um dataframe com os novos casos no Brasil.


def CasosNovosBr():
    casos_novos_br = df_copy[["regiao", "casosNovos", "data"]]
    casos_novos_br = casos_novos_br[casos_novos_br["regiao"] == "Brasil"].rename(columns={
        "casosNovos":"Casos Novos (Brasil)", "data":"Data"})
    casos_novos_br.set_index("Data", inplace=True)

    return casos_novos_br


# Cria um gráfico de linha com os novos casos no país.


def GraficoCasosNovosBR():
    fig = px.bar(x=CasosNovosBr().index, y=CasosNovosBr()["Casos Novos (Brasil)"],
                 title='Casos Novos de COVID-19 no Brasil')
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Casos Novos (Brasil)")

    return fig.show()


# Cria um dataframe com os óbitos acumulados por estado.


def ObitosAcumuladosUF():
    obitos_acumulados_UF = df_copy[["estado", "obitosAcumulado", "data"]]
    obitos_acumulados_UF = obitos_acumulados_UF[
        obitos_acumulados_UF["data"] == ultima_data].rename(
        columns={"obitosAcumulado":"Óbitos Acumulados (Estados)", "data":"Data"})
    obitos_acumulados_UF.set_index("Data", inplace=True)
    obitos_acumulados_UF = obitos_acumulados_UF.iloc[1:28].sort_values(by=["estado"])

    return obitos_acumulados_UF


# Cria um gráfico do mapa do Brasil com os óbitos acumulados por estado.


def MapaObitosAcumUF():
    info_estados = gpd.read_file("bcim_2016_21_11_2018.gpkg", layer="lim_unidade_federacao_a")
    info_estados.rename({"sigla":"estado"}, axis=1, inplace=True)
    obitos_estados = info_estados.merge(ObitosAcumuladosUF(), on="estado", how="left")


    obitos_estados.plot(column="Óbitos Acumulados (Estados)",
                 cmap="Reds",
                 legend=True,
                 figsize=(32,20),
                 edgecolor="black")

    # plt.savefig('imagens/obitos_por_estado_mapa.png', dpi=300)

    return plt.savefig('imagens/obitos_por_estado_mapa.png', dpi=300)
        # plt.show()


# Cria um gráfico de barras com os óbitos acumulados por estado.


def GraficoObitosAcumUF():
    fig = px.bar(ObitosAcumuladosUF(), x=ObitosAcumuladosUF()["estado"],
                 y=ObitosAcumuladosUF()["Óbitos Acumulados (Estados)"], title="Óbitos Acumulados (Estados)")
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Óbitos Acumulados (Estados)")

    return fig.show()


# Cria um dataframe com o número de casos acumulados por estado, levando em conta a população.


def CasosPorPop():
    casos_por_pop = df_copy[["estado", "populacaoTCU2019","casosAcumulado", "data"]]
    casos_por_pop = casos_por_pop[
        casos_por_pop["data"] == ultima_data].rename(
        columns={"populacaoTCU2019":"População Estado", "data":"Data",
                "casosAcumulado":"Casos Acumulados (por estado)"})
    casos_por_pop.set_index("Data", inplace=True)
    casos_por_pop = casos_por_pop.iloc[1:28].sort_values(by=["estado"])

    return casos_por_pop


# Cria um scatter plot com número de casos acumulados por estado, levando em conta a população.


def GraficoCasosPop():
    fig = px.scatter(x=CasosPorPop()["População Estado"], y=CasosPorPop()["Casos Acumulados (por estado)"],
                 color=CasosPorPop()["estado"], size=CasosPorPop()["Casos Acumulados (por estado)"])

    fig.update_layout(
    xaxis_title="População",
    yaxis_title="Casos Acumulados (por estado)")

    return fig.show()


# Cria uma regrassão linear simples entre número de casos e população


def RegLinCasosPop():
    # Regressão linear
    X = CasosPorPop()["População Estado"]
    Y = CasosPorPop()["Casos Acumulados (por estado)"]

    linear_regressor = LinearRegression()  # create object for the class

    X = X.values.reshape(-1, 1)  # values converts it into a numpy array
    Y = Y.values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column

    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions

    CasosPorPop().plot(x="População Estado", y="Casos Acumulados (por estado)",
               kind="scatter", title="Casos por estado x População (Regressão Linear)")
    plt.scatter(X, Y)
    plt.plot(X, Y_pred, color='red')
    plt.savefig('imagens/reg_linear_casos_por_pop.png', dpi=300)

    # fig.write_image("imagens/casos_por_pop.png", width=3840, height=2160)

    return fig.write_image("imagens/casos_por_pop.png", width=3840, height=2160)
        # plt.show()


# Comparação entre número de casos e número de óbitos por estado.

def Comparativo():
    comparativo_df = CasosPorPop().merge(ObitosAcumuladosUF(), on="estado", how="left")
    comparativo_df["Casos/População"] = comparativo_df["Casos Acumulados (por estado)"] / comparativo_df[
        "População Estado"]
    comparativo_df["Óbitos/Casos"] = comparativo_df["Óbitos Acumulados (Estados)"] / comparativo_df[
        "Casos Acumulados (por estado)"]

    return comparativo_df


# Cria dois graicos com número de casos e número de óbitos por estado.


def GraficoComparacao():
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    fig.add_trace(go.Bar(x=Comparativo()["estado"], y=Comparativo()["Casos/População"],
                         name="Casos/População"), row=1, col=1)

    fig.add_trace(go.Bar(x=Comparativo()["estado"], y=Comparativo()["Óbitos/Casos"],
                         name="Óbitos/Casos"), row=2, col=1)

    fig.update_layout(height=600, width=800, title_text="Casos/População e Óbitos/Casos")
    return fig.show()


ObitosAcumuladosUF()
Comparativo()
GraficoComparacao()

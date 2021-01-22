import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def CriaDataframe(arquivo):
    # Após análise do arquivo CSV, é necessário utilizar o parâmetro "sep=';'", pois o separador utilizado é o ;
    df = pd.read_csv(arquivo, sep=";")
    df_copy = df.copy()

    return df_copy


# Pega a última data disponível no dataset e atribui a uma variável que será usada em algumas funções.


def UltimoDia(dataframe_covid):
    ultima_data = dataframe_covid["data"].iloc[-1]

    return ultima_data


# Cria um dataframe com os casos acumulados no BrasilObitosAcumuladosUF()


def CasosAcumuladosBr(dataframe_covid):
    casos_acumulados_br = dataframe_covid[["regiao", "casosAcumulado", "data"]]
    casos_acumulados_br = casos_acumulados_br[casos_acumulados_br["regiao"] == "Brasil"].rename(columns={
        "casosAcumulado":"Casos Acumulados (Brasil)", "data":"Data"})
    casos_acumulados_br.set_index("Data", inplace=True)

    return casos_acumulados_br


# Cria um gráfico de linha com os casos acumulados no país.


def GraficoCasosAcumBR(dados_grafico):
    fig = px.line(x=dados_grafico.index,
                  y=dados_grafico["Casos Acumulados (Brasil)"],
                  title='Casos Acumulados de COVID-19 no Brasil')
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Casos Acumulados (Brasil)")

    return fig.show()

# Cria um dataframe com os novos casos no Brasil.


def CasosNovosBr(dataframe_covid):
    casos_novos_br = dataframe_covid[["regiao", "casosNovos", "data"]]
    casos_novos_br = casos_novos_br[casos_novos_br["regiao"] == "Brasil"].rename(columns={
        "casosNovos":"Casos Novos (Brasil)", "data":"Data"})
    casos_novos_br.set_index("Data", inplace=True)

    return casos_novos_br


# Cria um gráfico de linha com os novos casos no país.


def GraficoCasosNovosBR(dados_grafico):
    fig = px.bar(x=dados_grafico.index, y=dados_grafico["Casos Novos (Brasil)"],
                 title='Casos Novos de COVID-19 no Brasil')
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Casos Novos (Brasil)")

    return fig.show()


# Cria um dataframe com os óbitos acumulados por estado.


def ObitosAcumuladosUF(dataframe_covid, ultima_data):
    obitos_acumulados_UF = dataframe_covid[["estado", "obitosAcumulado", "data"]]
    obitos_acumulados_UF = obitos_acumulados_UF[
        obitos_acumulados_UF["data"] == ultima_data].rename(
        columns={"obitosAcumulado":"Óbitos Acumulados (Estados)", "data":"Data"})
    obitos_acumulados_UF.set_index("Data", inplace=True)
    obitos_acumulados_UF = obitos_acumulados_UF.iloc[1:28].sort_values(by=["estado"])

    return obitos_acumulados_UF


# Cria um gráfico do mapa do Brasil com os óbitos acumulados por estado.


def MapaObitosAcumUF(dados_grafico):
    info_estados = gpd.read_file("bcim_2016_21_11_2018.gpkg", layer="lim_unidade_federacao_a")
    info_estados.rename({"sigla":"estado"}, axis=1, inplace=True)
    obitos_estados = info_estados.merge(dados_grafico, on="estado", how="left")


    obitos_estados.plot(column="Óbitos Acumulados (Estados)",
                 cmap="Reds",
                 legend=True,
                 figsize=(32,20),
                 edgecolor="black")

    return plt.savefig('imagens/obitos_por_estado_mapa.png', dpi=300)


# Cria um gráfico de barras com os óbitos acumulados por estado.


def GraficoObitosAcumUF(dados_grafico):
    fig = px.bar(x=dados_grafico["estado"],
                 y=dados_grafico["Óbitos Acumulados (Estados)"],
                 title="Óbitos Acumulados (Estados)")
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Óbitos Acumulados (Estados)")

    return fig.show()


# Cria um dataframe com o número de casos acumulados por estado, levando em conta a população.


def CasosPorPop(dataframe_covid, ultima_data):
    casos_por_pop = dataframe_covid[["estado", "populacaoTCU2019","casosAcumulado", "data"]]
    casos_por_pop = casos_por_pop[
        casos_por_pop["data"] == ultima_data].rename(
        columns={"populacaoTCU2019":"População Estado", "data":"Data",
                "casosAcumulado":"Casos Acumulados (por estado)"})
    casos_por_pop.set_index("Data", inplace=True)
    casos_por_pop = casos_por_pop.iloc[1:28].sort_values(by=["estado"])

    return casos_por_pop


# Cria um scatter plot com número de casos acumulados por estado, levando em conta a população.


def GraficoCasosPop(dados_grafico):
    fig = px.scatter(x=dados_grafico["População Estado"], y=dados_grafico["Casos Acumulados (por estado)"],
                 color=dados_grafico["estado"], size=dados_grafico["Casos Acumulados (por estado)"])

    fig.update_layout(
    xaxis_title="População",
    yaxis_title="Casos Acumulados (por estado)")

    return fig.show()


# Cria uma regrassão linear simples entre número de casos e população


def RegLinCasosPop(dados_grafico):
    # Regressão linear
    X = dados_grafico["População Estado"]
    Y = dados_grafico["Casos Acumulados (por estado)"]

    linear_regressor = LinearRegression()  # create object for the class

    X = X.values.reshape(-1, 1)  # values converts it into a numpy array
    Y = Y.values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column

    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions

    dados_grafico.plot(x="População Estado", y="Casos Acumulados (por estado)",
               kind="scatter", title="Casos por estado x População (Regressão Linear)")
    plt.scatter(X, Y)
    plt.plot(X, Y_pred, color='red')

    return plt.savefig('imagens/reg_linear_casos_por_pop.png', dpi=300)


# Comparação entre número de casos e número de óbitos por estado.

def Comparativo(casos_por_populacao, dados_obitos_uf):
    comparativo_df = casos_por_populacao.merge(dados_obitos_uf, on="estado", how="left")
    comparativo_df["Casos/População"] = comparativo_df["Casos Acumulados (por estado)"] / comparativo_df[
        "População Estado"]
    comparativo_df["Óbitos/Casos"] = comparativo_df["Óbitos Acumulados (Estados)"] / comparativo_df[
        "Casos Acumulados (por estado)"]

    return comparativo_df


# Cria dois graicos com número de casos e número de óbitos por estado.


def GraficoComparacao(dados_grafico):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    fig.add_trace(go.Bar(x=dados_grafico["estado"], y=dados_grafico["Casos/População"],
                         name="Casos/População"), row=1, col=1)

    fig.add_trace(go.Bar(x=dados_grafico["estado"], y=dados_grafico["Óbitos/Casos"],
                         name="Óbitos/Casos"), row=2, col=1)

    fig.update_layout(height=600, width=800, title_text="Casos/População e Óbitos/Casos")
    return fig.show()
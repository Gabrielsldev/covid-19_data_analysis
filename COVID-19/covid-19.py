import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

import os

if not os.path.exists("imagens"):
    os.mkdir("imagens")

# Após análise do arquivo CSV, é necessário utilizar o parâmetro "sep=';'", pois o separador utilizado é o ;
df = pd.read_csv("HIST_PAINEL_COVIDBR_19jan2021.csv", sep=";")
df_copy = df.copy()

ultima_data = df_copy["data"].iloc[-1]


def CasosAcumuladosBr():
    casos_acumulados_br = df_copy[["regiao", "casosAcumulado", "data"]]
    casos_acumulados_br = casos_acumulados_br[casos_acumulados_br["regiao"] == "Brasil"].rename(columns={
        "casosAcumulado":"Casos Acumulados (Brasil)", "data":"Data"})
    casos_acumulados_br.set_index("Data", inplace=True)

    return casos_acumulados_br


fig = px.line(x=CasosAcumuladosBr().index,
              y=CasosAcumuladosBr()["Casos Acumulados (Brasil)"],
              title='Casos Acumulados de COVID-19 no Brasil')
fig.update_layout(
    xaxis_title="Data",
    yaxis_title="Casos Acumulados (Brasil)")


fig.show()

def CasosNovosBr():
    casos_novos_br = df_copy[["regiao", "casosNovos", "data"]]
    casos_novos_br = casos_novos_br[casos_novos_br["regiao"] == "Brasil"].rename(columns={
        "casosNovos":"Casos Novos (Brasil)", "data":"Data"})
    casos_novos_br.set_index("Data", inplace=True)

    return casos_novos_br

fig = px.bar(x=CasosNovosBr().index, y=CasosNovosBr()["Casos Novos (Brasil)"],
             title='Casos Novos de COVID-19 no Brasil')
fig.update_layout(
    xaxis_title="Data",
    yaxis_title="Casos Novos (Brasil)")

fig.show()


def ObitosAcumuladosBr():
    obitos_acumulados_br = df_copy[["estado", "obitosAcumulado", "data"]]
    obitos_acumulados_br = obitos_acumulados_br[
        obitos_acumulados_br["data"] == ultima_data].rename(
        columns={"obitosAcumulado":"Óbitos Acumulados (Brasil)", "data":"Data"})
    obitos_acumulados_br.set_index("Data", inplace=True)
    obitos_acumulados_br = obitos_acumulados_br.iloc[1:28].sort_values(by=["estado"])

    return obitos_acumulados_br

info_estados = gpd.read_file("bcim_2016_21_11_2018.gpkg", layer="lim_unidade_federacao_a")
info_estados.rename({"sigla":"estado"}, axis=1, inplace=True)
obitos_estados = info_estados.merge(ObitosAcumuladosBr(), on="estado", how="left")


obitos_estados.plot(column="Óbitos Acumulados (Brasil)",
             cmap="Reds",
             legend=True,
             figsize=(32,20),
             edgecolor="black")

plt.savefig('imagens/obitos_por_estado_mapa.png', dpi=300)

fig = px.bar(ObitosAcumuladosBr(), x=ObitosAcumuladosBr()["estado"], y=ObitosAcumuladosBr()["Óbitos Acumulados (Brasil)"], title="Óbitos Acumulados (Brasil)")
fig.update_layout(
    xaxis_title="Data",
    yaxis_title="Casos Novos (Brasil)")

fig.show()

def CasosPorPop():
    casos_por_pop = df_copy[["estado", "populacaoTCU2019","casosAcumulado", "data"]]
    casos_por_pop = casos_por_pop[
        casos_por_pop["data"] == ultima_data].rename(
        columns={"populacaoTCU2019":"População Estado", "data":"Data",
                "casosAcumulado":"Casos Acumulados (por estado)"})
    casos_por_pop.set_index("Data", inplace=True)
    casos_por_pop = casos_por_pop.iloc[1:28].sort_values(by=["estado"])

    return casos_por_pop

# Regressão linear
X = CasosPorPop()["População Estado"]
Y = CasosPorPop()["Casos Acumulados (por estado)"]

linear_regressor = LinearRegression()  # create object for the class

X = X.values.reshape(-1, 1)  # values converts it into a numpy array
Y = Y.values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column

linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)  # make predictions

fig = px.scatter(x=CasosPorPop()["População Estado"], y=CasosPorPop()["Casos Acumulados (por estado)"],
                 color=CasosPorPop()["estado"], size=CasosPorPop()["Casos Acumulados (por estado)"])

fig.update_layout(
    xaxis_title="População",
    yaxis_title="Casos Acumulados (por estado)")

fig.show()

CasosPorPop().plot(x="População Estado", y="Casos Acumulados (por estado)",
               kind="scatter", title="Casos por estado x População (Regressão Linear)")
plt.scatter(X, Y)
plt.plot(X, Y_pred, color='red')

plt.savefig('imagens/reg_linear_casos_por_pop.png', dpi=300)
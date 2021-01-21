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


fig.write_image("imagens/casos_acumulados_pais.png", width=3840, height=2160)



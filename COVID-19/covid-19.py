import covid_modulo as covid

import sys
import os

if not os.path.exists("imagens"):
    os.mkdir("imagens")

lista_completa_args = sys.argv
lista_args = lista_completa_args[1:]

if len(lista_args) == 2:
    arquivo_csv = lista_args[0]
    condicao_mapa = lista_args[1]
elif len(lista_args) == 1:
    arquivo_csv = lista_args[0]
    condicao_mapa = False
else:
    print("Erro: Forneça o nome do arquivo CSV como primeiro argumento.")
    print("Caso queria o mapa do Brasil com o número de óbitos, insira o argumento -mapa")
    exit()


# Dataframe e as variáveis necessários para as funções

dataframe_covid = covid.CriaDataframe(arquivo=arquivo_csv)
ultimo_dia = covid.UltimoDia(dataframe_covid=dataframe_covid)

# Cria od dataframes necessários para a formação dos gráficos

dataframe_casos_acum_br = covid.CasosAcumuladosBr(dataframe_covid=dataframe_covid)
dataframe_casos_novos_br = covid.CasosNovosBr(dataframe_covid=dataframe_covid)
dataframe_obitos_acum_uf = covid.ObitosAcumuladosUF(dataframe_covid=dataframe_covid, ultima_data=ultimo_dia)
dataframe_casos_pop = covid.CasosPorPop(dataframe_covid=dataframe_covid, ultima_data=ultimo_dia)
dataframe_comparativo = covid.Comparativo(casos_por_populacao=dataframe_casos_pop, dados_obitos_uf=dataframe_obitos_acum_uf)

# Gráficos

covid.GraficoCasosAcumBR(dados_grafico=dataframe_casos_acum_br)
covid.GraficoCasosNovosBR(dados_grafico=dataframe_casos_novos_br)
covid.GraficoObitosAcumUF(dados_grafico=dataframe_obitos_acum_uf)
covid.GraficoCasosPop(dados_grafico=dataframe_casos_pop)
covid.RegLinCasosPop(dados_grafico=dataframe_casos_pop)
covid.GraficoComparacao(dados_grafico=dataframe_comparativo)

if condicao_mapa == "-mapa":
    covid.MapaObitosAcumUF(dados_grafico=dataframe_obitos_acum_uf)
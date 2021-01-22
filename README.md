# TESTE MEU TUDO
## _Vaga: Data Scientist_
###### Desenvolvido por Gabriel Sobreira Lopes

### Descrição

A aplicação cria gráficos interativos com informações sobre a COVID-19.
* Os dados utilizados estão disponibilizados para download no site [Coronavírus Brasil](https://covid.saude.gov.br/), no botão **Arquivo CSV**.
* A aplicação foi desenvolvida utilizando **Python 3.8.5** no sistema **Ubuntu 20.04**.
* O arquivo a ser executado é o `covid-19.py`, através de linha de comando e com argumentos, conforme especificado abaixo.
  * O arquivo `covid_modulo.py` contém as funções que são importadas no arquivo `covid-19.py`.
  * Foi adicionado o arquivo `covid-19_notebook.ipynb` caso o usuário queira executar o programa no Jupyter Notebook.

**NOTA:** Para a utilização da aplicação, é necessário o download do arquivo `.csv` no site [Coronavírus Brasil](https://covid.saude.gov.br/), disponível no botão **Arquivo CSV**. O arquivo `.csv` deve estar no mesmo diretório da aplicação principal `covid-19.py`.

***
### Instruções de Uso

* Clone o repositório utilizando `$ git clone https://github.com/Gabrielsldev/teste_meutudo.git`.
* Faça o download do arquivo `.csv` no site [Coronavírus Brasil](https://covid.saude.gov.br/), disponível no botão **Arquivo CSV**. O arquivo `.csv` deve estar no mesmo diretório da aplicação principal `covid-19.py`.
* Os módulos necessários para a execução da aplicação estão no arquivo [requirements.txt](https://github.com/Gabrielsldev/teste_meutudo/blob/main/requirements.txt).
* O usuário deverá criar um ambiente virtual e instalar os módulos contidos no arquivo `requirements.txt` com o comando `pip install -r requirements.txt` para que seja possível executar o programa.

**NOTA:** A aplicação deverá ser executada através de linha de comando fornecendo como argumento o nome do arquivo `.csv` a ser utilizado. A aplicação aceita dois argumentos:

`$ python covid-19.py nome_do_arquivo.csv -mapa`

* A aplicação aceita dois argumentos:
  * O **primeiro argumento** é **obrigatório** e deve ser o nome do arquivo `.csv` retirado do site [Coronavírus Brasil](https://covid.saude.gov.br/).
  * O **segundo argumento** é **opcional**. Caso o argumento `-mapa` seja passado, será criado um arquivo `.png` com o mapa do Brasil e o número de óbitos por estado.
    * A criação do mapa pode diminuir a performance da aplicação, por isso foi deixado como padrão a não criação do mapa.

**NOTA:** Para a criação do mapa, é necessário fazer o download do arquivo `bcim_2016_21_11_2018.gpkg` no site do [IBGE](https://www.ibge.gov.br/geociencias/downloads-geociencias.html). O arquivo está neste [link](https://www.ibge.gov.br/geociencias/downloads-geociencias.html), e poderá ser encontrado na árvore de arquivos conforme figura abaixo:
![IBGE](https://github.com/Gabrielsldev/teste_meutudo/blob/main/COVID-19/imagens/mapa_ibge.jpg)
* **O arquivo** `bcim_2016_21_11_2018.gpkg` **deve estar no mesmo diretório da aplicação principal** `covid-19.py`.

***
### Resultados Esperados

Quando a aplicação for executada, serão abertos gráficos no navegar com informações sobre a COVID-19. Os gráficos e suas principais conclusões podem ser vistas abaixo.
* Também foi feita uma regressão linear para exemplificar sua aplicação, cujo gráfico será criado na pasta `imagens` em formato `.png`.
* Caso o argumento `-mapa` seja passado, será criado um mapa do Brasil na pasta `imagens`, em formato `.png`, com os dados dos óbitos por estado.

***
### Problemas e Insights

Algumas das questões que podemos fazer sobre a pandemia da COVID-19 são:
* **Estamos em um momento de aceleração ou de desaceleração do número de contaminações?**
* **É esperado que estados mais populosos tenham mais casos e óbitos em números absolutos. Mas como os estados se saem em termos relativos?**
* **Estados com maior número de contaminados possuem, proporcionalmente, maior número de óbitos?**

De acordo com os gráficos gerados podemos tirar algumas conclusões (os dados apresentados vão até o dia 19/01/2021, mas é possível baixar um dataset mais atualizado no site [Coronavírus Brasil](https://covid.saude.gov.br/)):

O primeiro gráfico mostra o **número de casos acumulados no Brasil:**
![Casos Acumulados no Brasil](https://github.com/Gabrielsldev/teste_meutudo/blob/main/COVID-19/imagens/casos_acum_br.png)
* Podemos observar que a linha encontra-se em plena ascensão, ou seja, o número de casos acumulados no país está crescendo de forma acelerada.
  * Isso nos mostra que não houve desaceleração da pandemia nas últimas semanas, o que justifica as medidas de isolamento social, o uso de máscara e os demais instrumentos utilizados pelos governos estaduais para tentar conter as contaminações.

O segundo gráfico mostra o **número de casos casos novos no Brasil:**
![Número de casos novos no Brasil](https://github.com/Gabrielsldev/teste_meutudo/blob/main/COVID-19/imagens/casos_novos_br.png)
* Podemos ver que, após uma queda dos casos novos entre outubro e novembro de 2020, houve uma retomada no número de contaminações a partir de dezembro.
  * Essa informação é corroborada pelo primeiro gráfico apresentado, em que é demonstrado que o número total de casos vem crescendo de forma acelerada.
  * Observa-se gaps nesse gráfico. Acredita-se que isso se deve pelo atraso na publicação dos casos em determinados dias da semana, como sábados, domingos e feriados.


**Assim, fica demonstrado que o número de casos está aumentando e que a pandemia ainda está em estágio de aceleração.**

O terceiro gráfico é interessante, apesar de mostrar uma informação que é esperada. A **concentração do número de óbitos por estado:**
![Mapa - Óbitos por estado](https://github.com/Gabrielsldev/teste_meutudo/blob/main/COVID-19/imagens/obitos_por_estado_mapa.png)
* Como é esperado, estados mais populosos concentram um maior número de óbitos. Podemos observar que estados do sudeste como SP, RJ e MG estão entre os estados com maior número de óbitos.
* A mesma informação pode ser vista no gráfico de barras abaixo:
![Número de Óbitos por Estado](https://github.com/Gabrielsldev/teste_meutudo/blob/main/COVID-19/imagens/casos_acum_uf.png)

O quarto gráfico também mostra uma informação que é esperada. O **número de casos acumulados por estado e que, quanto maior a população, maior o número de casos:**

![Casos Acumulados por Estado](https://github.com/Gabrielsldev/teste_meutudo/blob/main/COVID-19/imagens/casos_uf.png)
* Aplicou-se uma **regressão linear nessa relação**, que nos mostra o que é esperado:
![Regressão Linear](https://github.com/Gabrielsldev/teste_meutudo/blob/main/COVID-19/imagens/reg_linear_casos_por_pop.png)

Assim, podemos confirmar que o número de casos e que o número de óbitos é maior quando a população do estado também é maior. Mas e em **termos relativos, como os estados estão se saindo?**

### O quinto gráfico faz uma comparação proporcional entre **casos/população e óbitos/casos em cada estado:**
![Comparação entre número de casos e número de óbitos nos estados.](https://github.com/Gabrielsldev/teste_meutudo/blob/main/COVID-19/imagens/comparacao_casos_obitos.png)
* De acordo com o gráfico acima, podemos observar que, apesar de SP ser o estado com o maior número absoluto de casos, possui uma baixa proporção entre número de casos e sua população.
  * Isso pode ser resultado de uma política de maior rigor em termos de distanciamento social e lockdown.
* Podemos observar também que o RJ, apesar de ter um dos menores índices de casos/população, possui o maior índice de óbitos/casos. Ou seja, há um nível baixo de contaminação da população, mas um alto índice de óbitos por contaminados.
* Já RR apresenta o comportamento oposto. Apesar de ter o maior índice de casos/população, é o segundo menor em óbitos/casos. Ou seja, há um alto nível de contaminação da população, mas um baixo índice de óbitos por casos.

***
### Conclusões

Podemos concluir que:
* A pandemia está em plena aceleração.
* Estados mais populosos possuem um maior número absoluto de casos, mas isso não se reflete em termos relativos.
* Estados com maior índice de casos/população não necessariamente possuem um alto índice de óbitos/casos.
* Assim como estados com baixo índice de casos/população não necessariamente possuem um alto índice de óbitos/casos.
  * **Esses resultados mostram que políticas públicas diferentes geram resultados diferentes no nível de contaminação e de óbitos na população, o que reforça a importância da atuação do Estado e das políticas públicas para a contenção da pandemia da COVID-19.**
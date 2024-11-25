# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="../../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Statistical Computing with R (SCR)

## Integrantes:
- [Jose Andre Filho](https://www.linkedin.com/in/joseandrefilho)

## Professores:
### Tutor
- [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)
### Coordenador
- [André Godoi Chiovato](https://www.linkedin.com/in/profandregodoi/)

# Análise Estatística de Tarifas de Energia - ANEEL

## Descrição
Este projeto realiza uma análise exploratória das tarifas homologadas das distribuidoras de energia elétrica no Brasil, utilizando dados abertos da ANEEL. O objetivo é identificar padrões de consumo energético e oportunidades de transição para fontes sustentáveis, integrando aspectos de inovação, justiça social, crescimento econômico e preservação ambiental.

## Estrutura do Projeto
```
2_SCR/
├── main.R           # Script principal que orquestra a execução
├── part1.R          # Configurações e funções auxiliares
├── part2.R          # Análises estatísticas
├── part3.R          # Visualizações e insights
├── data/            # Dados brutos da ANEEL
└── resultados/      # Resultados gerados
    ├── dados/       # Arquivos CSV com análises
    └── graficos/    # Visualizações geradas
```

## Conjunto de Dados
- **Fonte**: [ANEEL - Dados Abertos](https://dadosabertos.aneel.gov.br)
- **Dataset**: Tarifas Homologadas das Distribuidoras de Energia Elétrica
- **Formato**: CSV (separado por ponto e vírgula)
- **Encoding**: Latin1

## Funcionalidades

### 1. Análise Estatística Descritiva
- Medidas de tendência central (média, mediana, moda)
- Medidas de dispersão (desvio padrão, coeficiente de variação)
- Separatrizes (quartis, decis, percentis)
- Tabelas de distribuição de frequência

### 2. Visualizações
- Distribuição das tarifas com medidas de tendência central
- Boxplots por classe de consumo
- Análise de disparidade regional
- Evolução temporal das tarifas (quando aplicável)

### 3. Análises Integradas
- Padrões de consumo por região
- Disparidades tarifárias
- Oportunidades para energia sustentável
- Impacto social das tarifas

## Insights e Recomendações
O projeto gera insights em quatro pilares principais:

1. **Inovação**
   - Identificação de áreas para implementação de smart grids
   - Oportunidades para sistemas de armazenamento distribuído
   - Sugestão de tecnologias emergentes que podem ser aplicadas para melhorar a eficiência da rede elétrica, como IoT e sensores inteligentes

2. **Justiça Social**
   - Análise de disparidades tarifárias regionais
   - Recomendações para equalização tarifária
   - Identificação de grupos vulneráveis mais impactados pelas tarifas altas e sugestões de políticas públicas para apoio

3. **Crescimento Econômico**
   - Impacto das tarifas por setor
   - Oportunidades para eficiência energética
   - Avaliação do impacto econômico de investimentos em infraestrutura energética, como a modernização de redes de distribuição

4. **Preservação Ambiental**
   - Potencial para energia solar
   - Áreas prioritárias para transição energética
   - Proposta de incentivos para adoção de energias renováveis em regiões com alto potencial solar ou eólico

## Requisitos
- R (versão >= 4.0.0)
- Pacotes R:
  - ggplot2
  - dplyr
  - tidyr
  - readr
  - scales
  - gridExtra

## Instalação
```R
# Instalar pacotes necessários
install.packages(c("ggplot2", "dplyr", "tidyr", "readr", "scales", "gridExtra"))
```

## Uso
1. Clone o repositório
2. Configure o diretório de trabalho em `main.R`
3. Coloque o arquivo de dados em `data/`
4. Execute o script principal:
```R
source("main.R")
```

## Resultados
Os resultados são gerados em dois formatos:

1. **Arquivos CSV** (`resultados/dados/`)
   - estatisticas_gerais.csv
   - distribuicao_frequencia.csv
   - analise_por_classe.csv
   - disparidade_regional.csv
   - insights_integrados.csv

2. **Gráficos** (`resultados/graficos/`)
   - distribuicao_tarifas.png
   - boxplot_classes.png
   - disparidade_regional.png
   - evolucao_temporal.png

## Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

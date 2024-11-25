# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="../../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Statistical Computing with R (SCR)

## Integrantes: 
- <a href="https://www.linkedin.com/in/joseandrefilho">Jose Andre Filho</a>

## Professores:
### Tutor 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>
### Coordenador
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi Chiovato</a>

# Análise Estatística de Tarifas de Energia - ANEEL

## Descrição
Este projeto realiza uma análise exploratória das tarifas homologadas das distribuidoras de energia elétrica no Brasil, utilizando dados abertos da ANEEL. O objetivo é identificar padrões de consumo energético e oportunidades de transição para fontes sustentáveis, integrando aspectos de inovação, justiça social, crescimento econômico e preservação ambiental.

## Estrutura do Projeto
```
projeto/
├── main.R           # Script principal que orquestra a execução
├── R/               # Scripts de análise
│   ├── part1.R     # Configurações e funções auxiliares
│   ├── part2.R     # Análises estatísticas
│   └── part3.R     # Visualizações e insights
├── data/           # Dados brutos da ANEEL
└── resultados/     # Resultados gerados
    ├── dados/      # Arquivos CSV com análises
    └── graficos/   # Visualizações geradas
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

2. **Justiça Social**
   - Análise de disparidades tarifárias regionais
   - Recomendações para equalização tarifária

3. **Crescimento Econômico**
   - Impacto das tarifas por setor
   - Oportunidades para eficiência energética

4. **Preservação Ambiental**
   - Potencial para energia solar
   - Áreas prioritárias para transição energética

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

## Contribuição
Para contribuir com o projeto:
1. Faça um Fork
2. Crie sua Feature Branch
3. Faça commit de suas alterações
4. Envie um Pull Request

## Licença
Este projeto está sob a licença MIT.

## Contato
[Seu Nome] - [seu.email@dominio.com]

## Agradecimentos
- ANEEL pelos dados abertos
- Comunidade R

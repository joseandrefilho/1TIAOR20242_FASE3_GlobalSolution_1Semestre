# ===========================================================================
# ANÁLISE ESTATÍSTICA DE TARIFAS DE ENERGIA ELÉTRICA - ANEEL
# Objetivo: Analisar padrões de consumo e identificar oportunidades sustentáveis
# Fonte: https://dadosabertos.aneel.gov.br
# ===========================================================================

# Carregamento dos pacotes necessários
library(ggplot2)   # Para visualizações
library(dplyr)     # Para manipulação de dados
library(tidyr)     # Para organização de dados
library(readr)     # Para leitura de dados
library(scales)    # Para formatação de escalas
library(gridExtra) # Para organização de múltiplos gráficos

# ===========================================================================
# 1. FUNÇÕES AUXILIARES
# ===========================================================================

# Função para calcular a moda
calcular_moda <- function(x) {
  # Remove NA
  x <- x[!is.na(x)]
  # Encontra valores únicos e suas frequências
  contagem <- table(x)
  # Retorna o(s) valor(es) mais frequente(s)
  valores_moda <- as.numeric(names(contagem[contagem == max(contagem)]))
  return(valores_moda)
}

# Função para criar tabela de frequência
criar_tabela_frequencia <- function(dados, n_classes = 10) {
  # Calcula os limites das classes
  limites <- seq(min(dados, na.rm = TRUE), 
                 max(dados, na.rm = TRUE), 
                 length.out = n_classes + 1)
  
  # Cria a tabela de frequência
  freq <- table(cut(dados, breaks = limites, include.lowest = TRUE))
  
  # Calcula frequências relativas e acumuladas
  freq_rel <- prop.table(freq)
  freq_acum <- cumsum(freq_rel)
  
  # Cria dataframe com resultados
  tabela_freq <- data.frame(
    Classe = names(freq),
    Frequencia = as.numeric(freq),
    Freq_Relativa = as.numeric(freq_rel) * 100, # Convertido para percentual
    Freq_Acumulada = as.numeric(freq_acum) * 100 # Convertido para percentual
  )
  
  return(tabela_freq)
}

# Função para calcular separatrizes
calcular_separatrizes <- function(dados) {
  quartis <- quantile(dados, probs = c(0.25, 0.5, 0.75), na.rm = TRUE)
  decis <- quantile(dados, probs = seq(0.1, 0.9, by = 0.1), na.rm = TRUE)
  percentis <- quantile(dados, probs = c(0.01, 0.05, 0.95, 0.99), na.rm = TRUE)
  
  return(list(
    quartis = quartis,
    decis = decis,
    percentis = percentis
  ))
}

# ===========================================================================
# 2. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ===========================================================================

# Define o caminho do arquivo
file_path <- "data/tarifas-homologadas-distribuidoras-energia-eletrica.csv"

# Leitura do arquivo CSV
data <- read.csv(file_path, sep = ";", fileEncoding = "latin1")

# Conversão das colunas de tarifa
data$VlrTUSD <- as.numeric(gsub(",", ".", data$VlrTUSD))
data$VlrTE <- as.numeric(gsub(",", ".", data$VlrTE))

# Verifica dados ausentes
missing_data <- sapply(data, function(x) sum(is.na(x)))
print("\nQuantidade de dados ausentes por coluna:")
print(missing_data)

# Criação de diretórios para resultados
dir.create("resultados", showWarnings = FALSE)
dir.create("resultados/dados", showWarnings = FALSE)
dir.create("resultados/graficos", showWarnings = FALSE)
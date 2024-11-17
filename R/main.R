# Carregar bibliotecas necessárias
library(dplyr)
library(ggplot2)

# Definir o caminho da pasta onde estão os arquivos
caminho_pasta <- "data"

# Listar todos os arquivos CSV dentro da pasta
arquivos <- list.files(path = caminho_pasta, pattern = "*.csv", full.names = TRUE)

# Criar uma lista para armazenar os dados carregados
lista_dados <- lapply(arquivos, function(arquivo) {
  dados <- read.csv(arquivo, sep = ";")
  dados$Origem <- basename(arquivo) # Adiciona o nome do arquivo como uma nova coluna
  return(dados)
})

# Combinar os dados de todos os arquivos em um único dataframe (se tiverem a mesma estrutura)
dados <- bind_rows(lista_dados)

# Limpar a lista de arquivos da memória após a combinação
rm(lista_dados)
rm(arquivos)

# Filtrar dados para indicadores DEC e FEC
dados_dec_fec <- dados %>%
  filter(SigIndicador %in% c("DEC", "FEC"))

# Limpar o dataframe original, mantendo apenas dados_dec_fec
rm(dados)
gc()  # Garbage collection para liberar a memória

# Substituir vírgulas por pontos no formato brasileiro e converter para numérico
dados_dec_fec$VlrIndiceEnviado <- gsub(",", ".", dados_dec_fec$VlrIndiceEnviado)
dados_dec_fec$VlrIndiceEnviado <- as.numeric(dados_dec_fec$VlrIndiceEnviado)

# Converter colunas numéricas e datas, se necessário
dados_dec_fec$AnoIndice <- as.numeric(dados_dec_fec$AnoIndice)
dados_dec_fec$VlrIndiceEnviado <- as.numeric(dados_dec_fec$VlrIndiceEnviado)

# Remover linhas onde VlrIndiceEnviado é NA devido a conversão
dados_dec_fec <- dados_dec_fec %>% filter(!is.na(VlrIndiceEnviado))

# 1. Análise Descritiva: Estatísticas Básicas para DEC e FEC
estatisticas <- dados_dec_fec %>%
  group_by(SigIndicador, AnoIndice) %>%
  summarise(
    Media = mean(VlrIndiceEnviado, na.rm = TRUE),
    Mediana = median(VlrIndiceEnviado, na.rm = TRUE),
    Desvio_Padrao = sd(VlrIndiceEnviado, na.rm = TRUE),
    Q1 = quantile(VlrIndiceEnviado, 0.25, na.rm = TRUE),
    Q3 = quantile(VlrIndiceEnviado, 0.75, na.rm = TRUE)
  )

print(estatisticas)

# 2. Tabelas de Frequência para DEC e FEC
tabela_frequencia <- table(dados_dec_fec$SigIndicador)
print(tabela_frequencia)

# 3. Visualizações de Distribuição e Comparação entre Indicadores

# Histograma para observar a distribuição dos valores de DEC e FEC
ggplot(dados_dec_fec, aes(x = VlrIndiceEnviado, fill = SigIndicador)) +
  geom_histogram(binwidth = 5, alpha = 0.7, position = "dodge") +
  labs(title = "Distribuição dos Indicadores DEC e FEC", x = "Valor do Indicador", y = "Frequência")

# Boxplot para comparar a variação entre DEC e FEC
ggplot(dados_dec_fec, aes(x = SigIndicador, y = VlrIndiceEnviado, fill = SigIndicador)) +
  geom_boxplot() +
  labs(title = "Comparação de Indicadores DEC e FEC", x = "Indicador", y = "Valor do Indicador")

# 4. Análise Temporal: Tendência dos Indicadores DEC e FEC ao longo dos anos
ggplot(dados_dec_fec, aes(x = AnoIndice, y = VlrIndiceEnviado, color = SigIndicador)) +
  geom_line() +
  labs(title = "Tendência dos Indicadores DEC e FEC ao Longo dos Anos", x = "Ano", y = "Valor do Indicador")

# 5. Análise de Correlação entre DEC e FEC

# Filtrar os dados para DEC e FEC separadamente e juntar por AnoIndice
dados_dec <- dados_dec_fec %>% filter(SigIndicador == "DEC")
dados_fec <- dados_dec_fec %>% filter(SigIndicador == "FEC")
dados_correlacao <- inner_join(dados_dec, dados_fec, by = "AnoIndice", suffix = c("_DEC", "_FEC"))

# Calcular a correlação entre DEC e FEC
correlacao_dec_fec <- cor(dados_correlacao$VlrIndiceEnviado_DEC, dados_correlacao$VlrIndiceEnviado_FEC, use = "complete.obs")
print(paste("Correlação entre DEC e FEC:", correlacao_dec_fec))

# 6. Identificação de Outliers

# Calcular outliers para DEC e FEC com base em 1.5 * IQR acima do terceiro quartil
outliers <- dados_dec_fec %>%
  group_by(SigIndicador) %>%
  filter(VlrIndiceEnviado > quantile(VlrIndiceEnviado, 0.75) + 1.5 * IQR(VlrIndiceEnviado))

print("Outliers Identificados:")
print(outliers)

# 7. Insights para Sustentabilidade

# Tabela Resumo das Distribuidoras com Altos Valores de DEC e FEC
resumo_altos_valores <- dados_dec_fec %>%
  group_by(SigIndicador, SigAgente) %>%
  summarise(Media_Indicador = mean(VlrIndiceEnviado, na.rm = TRUE),
            Desvio_Padrao = sd(VlrIndiceEnviado, na.rm = TRUE)) %>%
  filter(Media_Indicador > quantile(dados_dec_fec$VlrIndiceEnviado, 0.75))

print("Resumo de Distribuidoras com Altos Valores de DEC e FEC:")
print(resumo_altos_valores)

# Visualização final: Distribuidoras com maiores valores de DEC e FEC
ggplot(resumo_altos_valores, aes(x = SigAgente, y = Media_Indicador, fill = SigIndicador)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Distribuidoras com Maiores Valores Médios de DEC e FEC", x = "Distribuidora", y = "Média do Indicador") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

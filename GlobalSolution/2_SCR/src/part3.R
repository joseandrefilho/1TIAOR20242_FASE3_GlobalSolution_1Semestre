# ===========================================================================
# 4. VISUALIZAÇÕES
# ===========================================================================

# 1. Distribuição das Tarifas com Medidas de Tendência Central
grafico_distribuicao <- ggplot(data, aes(x = VlrTE)) +
  geom_histogram(aes(y = ..density..), binwidth = 10, 
                 fill = "skyblue", color = "black", alpha = 0.7) +
  geom_density(color = "red", size = 1) +
  geom_vline(aes(xintercept = mean(VlrTE, na.rm = TRUE)), 
             color = "blue", linetype = "dashed", size = 1) +
  geom_vline(aes(xintercept = median(VlrTE, na.rm = TRUE)), 
             color = "green", linetype = "dashed", size = 1) +
  geom_vline(aes(xintercept = calcular_moda(VlrTE)[1]), 
             color = "red", linetype = "dashed", size = 1) +
  annotate("text", x = mean(data$VlrTE, na.rm = TRUE), y = 0, 
           label = "Média", color = "blue", angle = 90, vjust = -1) +
  annotate("text", x = median(data$VlrTE, na.rm = TRUE), y = 0, 
           label = "Mediana", color = "green", angle = 90, vjust = -1) +
  annotate("text", x = calcular_moda(data$VlrTE)[1], y = 0, 
           label = "Moda", color = "red", angle = 90, vjust = -1) +
  labs(
    title = "Distribuição das Tarifas de Energia",
    subtitle = "Com medidas de tendência central",
    x = "Tarifa de Energia (R$/MWh)",
    y = "Densidade"
  ) +
  theme_minimal()

# 2. Boxplot com Separatrizes por Classe
grafico_boxplot_classe <- ggplot(data, aes(x = reorder(DscClasse, VlrTE, FUN = median), 
                                           y = VlrTE)) +
  geom_boxplot(fill = "lightblue", alpha = 0.7) +
  labs(
    title = "Distribuição das Tarifas por Classe de Consumo",
    subtitle = "Análise de separatrizes e outliers",
    x = "Classe de Consumidor",
    y = "Tarifa de Energia (R$/MWh)"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# 3. Disparidade Regional
grafico_disparidade <- ggplot(disparidade_regional %>% top_n(15, Media_Total), 
                              aes(x = reorder(SigAgente, Media_Total), y = Media_Total)) +
  geom_bar(stat = "identity", fill = "coral", alpha = 0.7) +
  geom_errorbar(aes(ymin = Media_Total - DesvioPadrao, 
                    ymax = Media_Total + DesvioPadrao),
                width = 0.2) +
  labs(
    title = "Disparidade Regional das Tarifas",
    subtitle = "15 distribuidoras com maiores tarifas médias (com desvio padrão)",
    x = "Distribuidora",
    y = "Tarifa Total Média (R$/MWh)"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# 4. Evolução Temporal (se disponível)
if("DatInicioVigencia" %in% names(data)) {
  data$DatInicioVigencia <- as.Date(data$DatInicioVigencia)
  
  grafico_temporal <- data %>%
    group_by(DatInicioVigencia) %>%
    summarise(
      Media_Total = mean(VlrTE + VlrTUSD, na.rm = TRUE),
      DP = sd(VlrTE + VlrTUSD, na.rm = TRUE)
    ) %>%
    ggplot(aes(x = DatInicioVigencia, y = Media_Total)) +
    geom_line(color = "blue", size = 1) +
    geom_ribbon(aes(ymin = Media_Total - DP, 
                    ymax = Media_Total + DP),
                alpha = 0.2) +
    labs(
      title = "Evolução Temporal das Tarifas",
      subtitle = "Média e variabilidade ao longo do tempo",
      x = "Data de Início de Vigência",
      y = "Tarifa Média Total (R$/MWh)"
    ) +
    theme_minimal()
}

# Exibição dos gráficos
print("\n=== VISUALIZAÇÕES ESTATÍSTICAS ===")
print("\n1. Distribuição das Tarifas")
print(grafico_distribuicao)

print("\n2. Boxplot por Classe de Consumo")
print(grafico_boxplot_classe)

print("\n3. Disparidade Regional")
print(grafico_disparidade)

if(exists("grafico_temporal")) {
  print("\n4. Evolução Temporal")
  print(grafico_temporal)
}

# ===========================================================================
# 5. ANÁLISE INTEGRADA E INSIGHTS
# ===========================================================================

# Análise de oportunidades sustentáveis
analise_oportunidades <- disparidade_regional %>%
  mutate(
    Potencial_Solar = case_when(
      Media_Total > quantile(Media_Total, 0.75) ~ "Alto",
      Media_Total > quantile(Media_Total, 0.5) ~ "Médio",
      TRUE ~ "Baixo"
    ),
    Prioridade_Acao = case_when(
      CV > quantile(CV, 0.75) ~ "Alta",
      CV > quantile(CV, 0.5) ~ "Média",
      TRUE ~ "Baixa"
    )
  )

# Criação do dataframe de insights
insights <- data.frame(
  Pilar = c(
    "Inovação",
    "Inovação",
    "Justiça Social",
    "Justiça Social",
    "Crescimento Econômico",
    "Crescimento Econômico",
    "Preservação Ambiental",
    "Preservação Ambiental"
  ),
  
  Achado = c(
    paste("Maior variabilidade tarifária encontrada em", 
          disparidade_regional$SigAgente[which.max(disparidade_regional$CV)]),
    paste("Tarifa média mais alta:", 
          round(max(disparidade_regional$Media_Total), 2), "R$/MWh"),
    paste("Classe mais impactada:", 
          classe_analysis$DscClasse[which.max(classe_analysis$Media_TE)]),
    paste("Diferença entre quartis:", 
          round(separatrizes_te$quartis[3] - separatrizes_te$quartis[1], 2), "R$/MWh"),
    paste("CV médio do setor:", 
          round(mean(disparidade_regional$CV), 2), "%"),
    paste("Número de distribuidoras analisadas:", nrow(disparidade_regional)),
    paste("Regiões com alto potencial solar:", 
          sum(analise_oportunidades$Potencial_Solar == "Alto")),
    paste("Distribuidoras prioritárias:", 
          sum(analise_oportunidades$Prioridade_Acao == "Alta"))
  ),
  
  Recomendacao = c(
    "Implementar smart grids nas áreas de maior variabilidade",
    "Desenvolver sistemas de armazenamento distribuído",
    "Criar programas específicos de tarifa social",
    "Estabelecer mecanismos de equalização tarifária",
    "Fomentar eficiência energética industrial",
    "Expandir mercado livre para pequenos consumidores",
    "Incentivar geração distribuída solar",
    "Priorizar transição para matriz renovável"
  ),
  
  Impacto = c("Alto", "Médio", "Alto", "Alto", "Médio", "Alto", "Alto", "Alto")
)

# Exportação dos insights
write.csv(insights, "resultados/dados/insights_integrados.csv", row.names = FALSE)

# Salvamento dos gráficos
ggsave("resultados/graficos/distribuicao_tarifas.png", 
       grafico_distribuicao, width = 12, height = 6, dpi = 300)

ggsave("resultados/graficos/boxplot_classes.png", 
       grafico_boxplot_classe, width = 12, height = 6, dpi = 300)

ggsave("resultados/graficos/disparidade_regional.png", 
       grafico_disparidade, width = 12, height = 6, dpi = 300)

if(exists("grafico_temporal")) {
  ggsave("resultados/graficos/evolucao_temporal.png", 
         grafico_temporal, width = 12, height = 6, dpi = 300)
}

# Exibição dos insights
print("\n=== INSIGHTS E RECOMENDAÇÕES ===")
print(insights)

print("\nAnálise concluída!")
print("Todos os resultados foram salvos em:")
print("- Dados: resultados/dados/")
print("- Gráficos: resultados/graficos/")
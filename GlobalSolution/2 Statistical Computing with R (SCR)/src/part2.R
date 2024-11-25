# ===========================================================================
# 3. ANÁLISE ESTATÍSTICA DESCRITIVA
# ===========================================================================

# Cálculo de estatísticas descritivas completas
estatisticas_tarifas <- data %>%
  summarise(
    # Estatísticas TE
    TE_N = sum(!is.na(VlrTE)),
    TE_Media = mean(VlrTE, na.rm = TRUE),
    TE_Mediana = median(VlrTE, na.rm = TRUE),
    TE_Moda = list(calcular_moda(VlrTE)),
    TE_DesvioPadrao = sd(VlrTE, na.rm = TRUE),
    TE_CV = sd(VlrTE, na.rm = TRUE)/mean(VlrTE, na.rm = TRUE)*100,
    TE_Min = min(VlrTE, na.rm = TRUE),
    TE_Max = max(VlrTE, na.rm = TRUE),
    
    # Estatísticas TUSD
    TUSD_N = sum(!is.na(VlrTUSD)),
    TUSD_Media = mean(VlrTUSD, na.rm = TRUE),
    TUSD_Mediana = median(VlrTUSD, na.rm = TRUE),
    TUSD_Moda = list(calcular_moda(VlrTUSD)),
    TUSD_DesvioPadrao = sd(VlrTUSD, na.rm = TRUE),
    TUSD_CV = sd(VlrTUSD, na.rm = TRUE)/mean(VlrTUSD, na.rm = TRUE)*100,
    TUSD_Min = min(VlrTUSD, na.rm = TRUE),
    TUSD_Max = max(VlrTUSD, na.rm = TRUE)
  )

# Tabelas de frequência
tabela_freq_te <- criar_tabela_frequencia(data$VlrTE)
tabela_freq_tusd <- criar_tabela_frequencia(data$VlrTUSD)

# Cálculo das separatrizes
separatrizes_te <- calcular_separatrizes(data$VlrTE)
separatrizes_tusd <- calcular_separatrizes(data$VlrTUSD)

# Análise por classe de consumidor
classe_analysis <- data %>%
  group_by(DscClasse) %>%
  summarise(
    Quantidade = n(),
    Media_TE = mean(VlrTE, na.rm = TRUE),
    Mediana_TE = median(VlrTE, na.rm = TRUE),
    Moda_TE = list(calcular_moda(VlrTE)),
    Q1_TE = quantile(VlrTE, 0.25, na.rm = TRUE),
    Q3_TE = quantile(VlrTE, 0.75, na.rm = TRUE),
    DesvioPadrao_TE = sd(VlrTE, na.rm = TRUE),
    CV_TE = DesvioPadrao_TE/Media_TE*100
  ) %>%
  arrange(desc(Quantidade))

# Análise de disparidade regional
disparidade_regional <- data %>%
  group_by(SigAgente) %>%
  summarise(
    Quantidade = n(),
    Media_Total = mean(VlrTE + VlrTUSD, na.rm = TRUE),
    DesvioPadrao = sd(VlrTE + VlrTUSD, na.rm = TRUE),
    CV = DesvioPadrao/Media_Total*100,
    Q1 = quantile(VlrTE + VlrTUSD, 0.25, na.rm = TRUE),
    Q3 = quantile(VlrTE + VlrTUSD, 0.75, na.rm = TRUE)
  ) %>%
  arrange(desc(Media_Total))

# Exibição dos resultados estatísticos
print("\n=== ESTATÍSTICAS DESCRITIVAS ===")
print("\nTarifa de Energia (TE):")
print(paste("Número de observações:", estatisticas_tarifas$TE_N))
print(paste("Média:", round(estatisticas_tarifas$TE_Media, 2), "R$/MWh"))
print(paste("Mediana:", round(estatisticas_tarifas$TE_Mediana, 2), "R$/MWh"))
print(paste("Moda:", paste(round(unlist(estatisticas_tarifas$TE_Moda), 2), collapse=", "), "R$/MWh"))
print(paste("Desvio Padrão:", round(estatisticas_tarifas$TE_DesvioPadrao, 2)))
print(paste("Coeficiente de Variação:", round(estatisticas_tarifas$TE_CV, 2), "%"))
print(paste("Mínimo:", round(estatisticas_tarifas$TE_Min, 2), "R$/MWh"))
print(paste("Máximo:", round(estatisticas_tarifas$TE_Max, 2), "R$/MWh"))

print("\nSeparatrizes TE:")
print("Quartis:")
print(round(separatrizes_te$quartis, 2))
print("Decis:")
print(round(separatrizes_te$decis, 2))
print("Percentis (1%, 5%, 95%, 99%):")
print(round(separatrizes_te$percentis, 2))

print("\n=== ANÁLISE POR CLASSE DE CONSUMIDOR ===")
print(classe_analysis)

print("\n=== DISPARIDADE REGIONAL (Top 10 maiores tarifas) ===")
print(head(disparidade_regional, 10))

# Ajuste das estatísticas para exportação
estatisticas_export <- data.frame(
  # Estatísticas TE
  TE_N = estatisticas_tarifas$TE_N,
  TE_Media = estatisticas_tarifas$TE_Media,
  TE_Mediana = estatisticas_tarifas$TE_Mediana,
  TE_Moda = paste(unlist(estatisticas_tarifas$TE_Moda), collapse = ";"),
  TE_DesvioPadrao = estatisticas_tarifas$TE_DesvioPadrao,
  TE_CV = estatisticas_tarifas$TE_CV,
  TE_Min = estatisticas_tarifas$TE_Min,
  TE_Max = estatisticas_tarifas$TE_Max,
  
  # Estatísticas TUSD
  TUSD_N = estatisticas_tarifas$TUSD_N,
  TUSD_Media = estatisticas_tarifas$TUSD_Media,
  TUSD_Mediana = estatisticas_tarifas$TUSD_Mediana,
  TUSD_Moda = paste(unlist(estatisticas_tarifas$TUSD_Moda), collapse = ";"),
  TUSD_DesvioPadrao = estatisticas_tarifas$TUSD_DesvioPadrao,
  TUSD_CV = estatisticas_tarifas$TUSD_CV,
  TUSD_Min = estatisticas_tarifas$TUSD_Min,
  TUSD_Max = estatisticas_tarifas$TUSD_Max
)

# Salvando as estatísticas em CSV
write.csv(estatisticas_export, 
          "resultados/dados/estatisticas_gerais.csv", 
          row.names = FALSE)

write.csv(tabela_freq_te, 
          "resultados/dados/distribuicao_frequencia_te.csv", 
          row.names = FALSE)

# Ajuste similar para análise por classe
classe_analysis_export <- classe_analysis %>%
  mutate(
    Moda_TE = sapply(Moda_TE, function(x) paste(x, collapse = ";"))
  )

# Salvando análise por classe
write.csv(classe_analysis_export, 
          "resultados/dados/analise_por_classe.csv", 
          row.names = FALSE)


write.csv(disparidade_regional, 
          "resultados/dados/disparidade_regional.csv", 
          row.names = FALSE)
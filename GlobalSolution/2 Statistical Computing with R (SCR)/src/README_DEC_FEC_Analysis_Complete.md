
# Projeto de Análise de Indicadores de Continuidade de Distribuição (DEC e FEC)

## Introdução

Este projeto tem como objetivo avaliar a continuidade e a qualidade da distribuição de energia elétrica no Brasil, utilizando os indicadores de continuidade **DEC (Duração Equivalente de Interrupção por Unidade Consumidora)** e **FEC (Frequência Equivalente de Interrupção por Unidade Consumidora)**. Esses indicadores são cruciais para entender a confiabilidade do sistema elétrico e para identificar áreas que necessitam de melhorias na infraestrutura de distribuição.

## Conjunto de Dados

Os dados utilizados para essa análise incluem:

1. **Indicadores de Continuidade Coletivos por Período**:
   - Arquivos CSV para os períodos 2000-2009, 2010-2019, e 2020-2029, contendo os valores dos indicadores DEC e FEC.
   - Estes arquivos fornecem uma visão histórica da evolução dos indicadores de continuidade.

2. **Compensação por Interrupções**:
   - Dados de compensação para os períodos de 2000-2009 e 2010-2019, detalhando o valor das compensações pagas aos consumidores por interrupções.
   - Permitem uma análise financeira do impacto das interrupções.

3. **Limites de Continuidade**:
   - Dados que definem os limites regulamentados para os indicadores DEC e FEC, possibilitando uma comparação dos resultados com os padrões exigidos.

4. **Dicionários de Dados**:
   - Dicionários que descrevem os campos dos arquivos, auxiliando na interpretação correta dos dados.

### Campos Principais

- **DEC**: Representa a duração total das interrupções por unidade consumidora.
- **FEC**: Indica o número de interrupções experimentadas por unidade consumidora.
- **SigAgente**: Sigla da distribuidora de energia responsável.
- **AnoIndice**: Ano de referência dos dados.
- **VlrIndiceEnviado**: Valor do índice enviado para análise.

## Metodologia da Análise

1. **Limpeza e Pré-processamento dos Dados**
   - Verificação da consistência dos dados, conversão de datas e tratamento de valores ausentes para garantir a integridade do conjunto de dados.

2. **Análise Estatística**
   - **Cálculo de Medidas de Tendência Central e Dispersão**: Cálculo de médias, medianas e desvios padrão para os indicadores DEC e FEC por região e distribuidora.
   - **Análise Temporal**: Estudo da evolução dos indicadores ao longo dos anos para identificar tendências e mudanças de performance.

3. **Análise Comparativa entre Regiões e Distribuidoras**
   - Comparação dos indicadores DEC e FEC entre diferentes distribuidoras e regiões, possibilitando a identificação de áreas que enfrentam mais problemas de continuidade.

## Visualizações

Para facilitar a interpretação dos dados, serão utilizadas as seguintes visualizações:

- **Gráficos de Linha**: Mostrarão a tendência dos indicadores DEC e FEC ao longo do tempo, destacando períodos de melhora ou piora.
- **Gráficos de Barras**: Permitirão comparar o desempenho das distribuidoras em um ano específico.
- **Boxplots**: Serão utilizados para comparar a variabilidade dos indicadores entre as distribuidoras.

## Geração de Insights

Com base na análise dos indicadores DEC e FEC, será possível:

- Identificar as distribuidoras e regiões com os piores desempenhos em termos de continuidade de energia.
- Propor melhorias para aumentar a continuidade e reduzir o impacto das interrupções, como manutenção preventiva e investimentos em infraestrutura.
- Avaliar o impacto financeiro das interrupções por meio dos dados de compensação.

## Exemplo de Código em R

Abaixo está um exemplo de código em R para realizar uma análise inicial dos dados:

```r
# Carregar os dados
dados_continuidade <- read.csv("caminho/para/o/arquivo.csv")

# Verificar a estrutura dos dados
str(dados_continuidade)

# Converter o campo de data e outros campos necessários
dados_continuidade$DatGeracaoConjuntoDados <- as.Date(dados_continuidade$DatGeracaoConjuntoDados)
dados_continuidade$AnoIndice <- as.numeric(dados_continuidade$AnoIndice)

# Filtrar por DEC e FEC e calcular a média por ano e por distribuidora
library(dplyr)
dec_fec_medias <- dados_continuidade %>%
  filter(SigIndicador %in% c("DEC", "FEC")) %>%
  group_by(SigAgente, AnoIndice, SigIndicador) %>%
  summarise(Media_Indicador = mean(VlrIndiceEnviado, na.rm = TRUE))

# Visualizar a tendência do DEC e FEC ao longo do tempo
library(ggplot2)
ggplot(dec_fec_medias, aes(x = AnoIndice, y = Media_Indicador, color = SigIndicador)) +
  geom_line() +
  facet_wrap(~ SigAgente) +
  labs(title = "Tendência dos Indicadores DEC e FEC por Distribuidora", x = "Ano", y = "Média do Indicador")

# Comparar distribuidoras em um ano específico (exemplo: 2020)
comparacao_2020 <- dec_fec_medias %>% filter(AnoIndice == 2020)
ggplot(comparacao_2020, aes(x = reorder(SigAgente, Media_Indicador), y = Media_Indicador, fill = SigIndicador)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Comparação dos Indicadores DEC e FEC entre Distribuidoras (2020)", x = "Distribuidora", y = "Média do Indicador") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))
```

Este exemplo demonstra como carregar os dados, calcular médias por ano e distribuidora, e gerar gráficos para a análise. Esses passos podem ser expandidos para uma análise mais detalhada.

## Conclusão

O projeto de análise dos indicadores de continuidade de energia (DEC e FEC) permite entender a qualidade do fornecimento de energia no Brasil e propor melhorias baseadas em dados. Através dessa análise, é possível identificar as regiões e distribuidoras que mais necessitam de intervenções para garantir um fornecimento de energia mais confiável e eficiente, promovendo maior satisfação do consumidor e eficiência energética.

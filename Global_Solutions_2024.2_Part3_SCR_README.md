
# Global Solutions 2024.2 - Parte 3: Statistical Computing with R (SCR)

Este documento detalha a análise exploratória de dados tarifários fornecidos pela ANEEL, utilizando técnicas estatísticas e visualizações para identificar padrões e oportunidades de eficiência energética.

---

## Conjunto de Dados
**Fonte:** ANEEL - Tarifas Homologadas das Distribuidoras de Energia Elétrica.  
**Descrição:**
- Valores de Tarifa de Uso do Sistema de Distribuição (TUSD) e Tarifa de Energia (TE).
- Dados categorizados por distribuidoras, modalidades tarifárias, e classes de consumo.

---

## Análise Estatística

### **1. Tarifas por Distribuidora**
- Identificou-se uma variação significativa nas tarifas médias entre distribuidoras.
- Distribuidoras com tarifas mais altas podem ter custos operacionais maiores, justificando a necessidade de eficiência energética nessas regiões.

### **2. Tarifas por Modalidade Tarifária**
- Modalidades tarifárias como **Azul** e **Verde** apresentam custos diferentes.
- Modalidades horossazonais são ideais para consumidores que podem ajustar o consumo fora de horários de pico.

### **3. Tarifas por Classe de Consumo**
- **Residencial:** Apresenta tarifas médias mais altas, mostrando maior potencial de impacto financeiro com otimização.
- **Rural:** Tarifas mais baixas incentivam o uso em regiões economicamente vulneráveis.
- **Iluminação Pública:** Menores custos médios, refletindo o caráter essencial deste serviço.

---

## Visualizações
### **1. Tarifas Médias por Distribuidora**
Gráfico de barras que ilustra as tarifas médias de TUSD e TE entre as distribuidoras, destacando as variações regionais.

### **2. Tarifas Médias por Modalidade Tarifária**
Gráfico comparativo que explora as diferenças de tarifas entre modalidades, como Azul, Verde, etc.

### **3. Tarifas Médias por Classe de Consumo**
Gráfico destacando os custos médios de diferentes classes de consumidores, como Residencial, Rural, e Iluminação Pública.

---

## Conclusões

### **1. Tarifas e Eficiência Energética**
- **Distribuidoras:** Regiões com tarifas elevadas devem priorizar tecnologias de eficiência energética.
- **Modalidades:** Tarifas horossazonais (ex.: Azul) podem ser combinadas com sistemas de automação para otimizar custos.
- **Classes:** Consumidores residenciais são os mais beneficiados por sistemas de otimização devido às tarifas elevadas.

### **2. Relevância para o Projeto GS**
- Esses insights podem ser integrados aos modelos de IA (Parte 1) para sugerir fontes de energia mais econômicas.
- Sistemas automatizados (Parte 5) podem programar o uso fora dos horários de pico com base nas tarifas.

---

## Próximos Passos
- Incorporar os resultados aos modelos de IA e sistemas Python.
- Explorar oportunidades para incentivar a transição para fontes renováveis em regiões com altas tarifas.


# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="../../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Computational Thinking with Python (CTWP)

## Integrantes: 
- <a href="https://www.linkedin.com/in/joseandrefilho">Jose Andre Filho</a>

## Professores:
### Tutor 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>
### Coordenador
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi Chiovato</a>

# Sistema de Gerenciamento Energético Residencial

## Descrição

Sistema automatizado em Python para gerenciamento e otimização do consumo energético residencial, com interface gráfica interativa e monitoramento em tempo real. O sistema permite a seleção automática de fontes de energia baseada em critérios de economia e sustentabilidade, com foco na redução de custos e aumento da eficiência energética.

## Funcionalidades Principais

### 1. Monitoramento em Tempo Real

- Visualização do consumo energético atual
- Acompanhamento de tarifas das diferentes fontes
- Gráficos dinâmicos de consumo
- Indicadores de performance energética

### 2. Gestão de Fontes de Energia

- Seleção automática entre energia solar e rede elétrica
- Monitoramento da capacidade solar disponível
- Cálculo de custos por fonte
- Análise de intensidade de carbono

### 3. Interface Gráfica

- Dashboard interativo com Tkinter
- Gráficos atualizados em tempo real
- Indicadores visuais da fonte atual de energia
- Seleção de recursos solares disponíveis

### 4. Relatórios e Análises

- Geração de relatórios de consumo em formato CSV
- Cálculo de custos acumulados
- Histórico de uso por fonte de energia
- Métricas de eficiência para avaliação do consumo

## Arquitetura do Sistema

```
4_CTWP/
│
├── requirements.txt               # Lista de dependências do Python
└── src/
    ├── EnergyManager.py             # Classe que gerencia fontes de energia, tarifas e consumo
    ├── MQTTClient.py                # Classe que gerencia a comunicação com o broker MQTT
    ├── GUI.py                       # Classe que gerencia a interface gráfica com Tkinter
    └── main.py                      # Arquivo principal para execução do sistema
```

## Uso do Sistema
### 1. Configuração do Ambiente

1. Crie um arquivo `.env` na raiz do projeto para configurar as variáveis de ambiente necessárias.
2. Adicione as seguintes variáveis ao arquivo `.env`:
   ```
   ELECTRICITYMAP_API_KEY=sua_chave_api
   ```
3. Substitua `sua_chave_api` pela chave de API da plataforma ElectricityMap.
4. Salve o arquivo `.env`.

### 2. Inicialização

1. Instale as dependências com `pip install -r requirements.txt`
2. Execute o arquivo `main.py`
2. Aguarde a conexão com o broker MQTT
3. Selecione o recurso solar disponível na interface gráfica

### 3. Monitoramento

- Observe o gráfico de consumo em tempo real na interface
- Verifique a fonte atual de energia utilizada
- Monitore as tarifas vigentes para cada fonte de energia

### 4. Relatórios

1. Clique em "Salvar Relatório" na interface gráfica
2. O arquivo será salvo em formato CSV
3. Analise os dados históricos para avaliação da eficiência energética

## Integrações

### 1. MQTT

- Broker: mqtt.eclipseprojects.io
- Tópico: rm87775/home/energy/consumption
- Formato: Valores de consumo em kWh

### 2. APIs Externas

- ElectricityMap: Intensidade de carbono para cada fonte de energia
- MockAPI: Dados dos recursos solares disponíveis

## Tomada de Decisão Automática

O sistema seleciona a fonte de energia com base em:

1. Disponibilidade de energia solar
2. Comparação de tarifas entre energia solar e rede elétrica
3. Intensidade de carbono de cada fonte
4. Capacidade atual do sistema solar

## Monitoramento e Alertas

O sistema monitora continuamente:

- Níveis de consumo energético
- Alterações nas tarifas de energia
- Capacidade solar disponível
- Eficiência do sistema em tempo real

## Sustentabilidade

Foco em energia limpa através de:

- Priorização de energia solar sempre que disponível
- Análise da intensidade de carbono de cada fonte
- Otimização do consumo para reduzir o impacto ambiental
- Métricas de eficiência para promover o uso sustentável

## Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


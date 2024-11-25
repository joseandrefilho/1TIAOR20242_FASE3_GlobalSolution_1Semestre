# Sistema de Gerenciamento Energético Residencial

## Descrição
Sistema automatizado em Python para gerenciamento e otimização do consumo energético residencial, com interface gráfica interativa e monitoramento em tempo real. O sistema permite a seleção automática de fontes de energia baseada em critérios de economia e sustentabilidade.

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
- Indicadores visuais de fonte atual
- Seleção de recursos solares

### 4. Relatórios e Análises
- Geração de relatórios de consumo
- Cálculo de custos acumulados
- Histórico de uso por fonte
- Métricas de eficiência

## Arquitetura do Sistema

```
energy_system/
│
├── energy_management_system.py   # Arquivo principal
├── requirements.txt             # Dependências
├── .env                        # Configurações e chaves de API
└── relatorios/                 # Relatórios gerados
```

### Classes Principais

#### 1. EnergyManager
```python
class EnergyManager:
    """Gerencia fontes de energia, tarifas e consumo."""
    def __init__(self):
        self.data = pd.DataFrame()
        self.current_tariff = {}
        self.solar_capacity = None
```

#### 2. MQTTClient
```python
class MQTTClient:
    """Gerencia comunicação MQTT para dados em tempo real."""
    def __init__(self, energy_manager):
        self.client = mqtt.Client()
```

#### 3. GUI
```python
class GUI:
    """Interface gráfica do sistema."""
    def __init__(self, energy_manager):
        self.root = tk.Tk()
        self.energy_manager = energy_manager
```

## Instalação e Execução

1. **Requisitos do Sistema**
```bash
# Dependências principais
python >= 3.8
tkinter
pandas
matplotlib
paho-mqtt
python-dotenv
requests
```

2. **Instalação**
```bash
# Clone o repositório
git clone [url-do-repositorio]

# Instale as dependências
pip install -r requirements.txt

# Configure o arquivo .env
ELECTRICITYMAP_API_KEY=sua_chave_aqui
```

3. **Execução**
```bash
python energy_management_system.py
```

## Uso do Sistema

### 1. Inicialização
1. Execute o programa
2. Aguarde a conexão com o broker MQTT
3. Selecione o recurso solar disponível

### 2. Monitoramento
- Observe o gráfico de consumo em tempo real
- Verifique a fonte atual de energia
- Monitore as tarifas vigentes

### 3. Relatórios
1. Clique em "Salvar Relatório"
2. O arquivo será salvo em formato CSV
3. Analise os dados históricos

## Integrações

### 1. MQTT
- Broker: mqtt.eclipseprojects.io
- Tópico: rm87775/home/energy/consumption
- Formato: Valores de consumo em kWh

### 2. APIs Externas
- ElectricityMap: Intensidade de carbono
- MockAPI: Dados de recursos solares

## Tomada de Decisão Automática

O sistema seleciona a fonte de energia baseado em:
1. Disponibilidade de energia solar
2. Comparação de tarifas
3. Intensidade de carbono
4. Capacidade atual do sistema

## Monitoramento e Alertas

O sistema monitora continuamente:
- Níveis de consumo
- Alterações nas tarifas
- Capacidade solar disponível
- Eficiência do sistema

## Sustentabilidade

Foco em energia limpa através de:
- Priorização de energia solar
- Análise de intensidade de carbono
- Otimização de consumo
- Métricas de eficiência

## Desenvolvimento Futuro

### Melhorias Planejadas
1. Integração com mais fontes de energia
2. Machine Learning para previsão de consumo
3. App mobile para monitoramento
4. Alertas personalizados
5. Backup de dados em nuvem

## Suporte

Em caso de problemas:
1. Verifique as conexões MQTT
2. Confirme as chaves de API
3. Consulte os logs do sistema
4. Entre em contato com suporte

## Licença
MIT License

## Autor
[Seu Nome]

## Agradecimentos
- FIAP
- Comunidade Python
- Contribuidores

# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="../../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Artificial Intelligence with Computer Systems and Sensors (AICSS)

## Integrantes: 
- <a href="https://www.linkedin.com/in/joseandrefilho">Jose Andre Filho</a>

## Professores:
### Tutor 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>
### Coordenador
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi Chiovato</a>

# Sistema de Automação de Iluminação Residencial

## Descrição
Sistema de automação residencial desenvolvido com ESP32 para otimização da iluminação interna e externa, utilizando sensores LDR e Ultrassônico para controle inteligente baseado em luminosidade e presença.

## Funcionalidades
- Controle automático de iluminação externa com dois níveis de intensidade
- Ativação inteligente de iluminação interna baseada em presença
- Monitoramento de consumo energético via MQTT
- Sistema de debug para acompanhamento em tempo real

## Componentes Utilizados
1. **Hardware**:
   - ESP32 DevKit C V4
   - Sensor LDR (Fotoresistor)
   - Sensor Ultrassônico HC-SR04
   - 1 LED Azul (iluminação externa baixa)
   - 2 LEDs Amarelos (iluminação externa alta e interna)
   - 3 Resistores 220Ω

2. **Software**:
   - Arduino IDE
   - Bibliotecas:
     - WiFi.h
     - PubSubClient.h
     - Arduino.h

## Configuração dos Pinos
```cpp
LDR_PIN = 33        // Sensor de luz
TRIG_PIN = 13       // Trigger do ultrassônico
ECHO_PIN = 12       // Echo do ultrassônico
LED_EXTERNO_1 = 15  // LED azul (baixa intensidade)
LED_EXTERNO_2 = 17  // LED amarelo 1 (alta intensidade)
LED_INTERNO = 18    // LED amarelo 2 (interno)
```

## Parâmetros de Configuração
```cpp
LDR_NOITE = 500     // Limiar para ativação noturna
LDR_INTERNO = 300   // Limiar para iluminação interna
DIST_PRESENCA = 200 // Distância para detectar presença (cm)
DIST_PROXIMA = 100  // Distância para presença próxima (cm)
```

## Lógica de Funcionamento

### Iluminação Externa
1. **Período Noturno** (LDR < 500):
   - Sem presença: LED azul ativo (baixa intensidade)
   - Com presença: LED azul + amarelo ativos (alta intensidade)
2. **Período Diurno**: LEDs externos desligados

### Iluminação Interna
- Ativa quando:
  - Ambiente escuro (LDR < 300)
  - Presença próxima detectada (distância < 100cm)

### Consumo Energético
- LED Externo 1: 0.05 kWh
- LED Externo 2: 0.10 kWh
- LED Interno: 0.07 kWh

## Comunicação
- **WiFi**: Conexão à rede local
- **MQTT**: Publicação de dados de consumo
  - Tópico: "rm87775/home/energy/consumption"
  - Formato: kWh com 2 casas decimais

## Instalação e Execução

1. **Configuração do Hardware**:
   ```
   ESP32 -> LDR:
   - 3V3 -> VCC
   - GND -> GND
   - GPIO33 -> AO

   ESP32 -> HC-SR04:
   - 5V -> VCC
   - GND -> GND
   - GPIO13 -> TRIG
   - GPIO12 -> ECHO

   ESP32 -> LEDs:
   - GPIO15 -> LED1 (via resistor 220Ω)
   - GPIO17 -> LED2 (via resistor 220Ω)
   - GPIO18 -> LED3 (via resistor 220Ω)
   ```

2. **Configuração do Software**:
   - Instale as bibliotecas necessárias
   - Configure as credenciais WiFi
   - Ajuste os limiares conforme necessário

## Simulação
O projeto pode ser simulado no Wokwi:
1. Importe o código-fonte
2. Carregue o diagram.json fornecido
3. Execute a simulação

## Debug e Monitoramento
- Serial Monitor (115200 baud)
- Cliente MQTT para acompanhamento do consumo

## Impactos

### Positivos
1. **Eficiência Energética**:
   - Iluminação adaptativa
   - Controle automatizado
   - Monitoramento de consumo

2. **Segurança**:
   - Iluminação mínima constante
   - Intensificação na detecção de presença

3. **Conforto**:
   - Automação inteligente
   - Adaptação às condições ambientais

### Negativos
1. **Dependência Tecnológica**:
   - Necessidade de conexão WiFi
   - Manutenção de sensores

2. **Custos**:
   - Implementação inicial
   - Manutenção do sistema

## Melhorias Futuras
1. Interface web para controle
2. Integração com outros sistemas
3. Ajuste dinâmico de parâmetros
4. Histórico de consumo

## Licença
MIT

## Autor
[Seu Nome]

## Link do Vídeo
[Link para o vídeo no YouTube]


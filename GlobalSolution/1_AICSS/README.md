# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="../../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Artificial Intelligence with Computer Systems and Sensors (AICSS)

## Integrantes:
- [Jose Andre Filho](https://www.linkedin.com/in/joseandrefilho)

## Professores:
### Tutor
- [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)
### Coordenador
- [André Godoi Chiovato](https://www.linkedin.com/in/profandregodoi/)

## Descrição
Este projeto consiste em um sistema de automação residencial desenvolvido com ESP32 para otimizar a iluminação interna e externa de uma residência. O sistema utiliza sensores LDR e Ultrassônico para controle inteligente da iluminação com base na luminosidade do ambiente e na detecção de presença. A solução visa aumentar a eficiência energética e a segurança da residência.

## Funcionalidades
- **Controle automático de iluminação externa** com dois níveis de intensidade.
- **Ativação inteligente da iluminação interna** baseada na presença.
- **Monitoramento de consumo energético** via MQTT.
- **Sistema de debug** para acompanhamento em tempo real.

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
   - Com presença: LED azul + LED amarelo ativos (alta intensidade)
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
1. Acesse o projeto em [https://wokwi.com/projects/414582888017664001](https://wokwi.com/projects/414582888017664001).
2. Execute a simulação.

## Debug e Monitoramento
- Serial Monitor (115200 baud)
- Cliente MQTT para acompanhamento do consumo

## Impactos da Solução

### Impactos Positivos
1. **Eficiência Energética**:
   - Iluminação adaptativa conforme a luminosidade do ambiente e a presença de pessoas.
   - Controle automatizado, reduzindo o consumo desnecessário de energia.
   - Monitoramento de consumo em tempo real via MQTT.

2. **Segurança**:
   - Iluminação mínima constante nas áreas externas, garantindo visibilidade para câmeras sem infravermelho.
   - Aumento da iluminação em caso de detecção de presença, contribuindo para a segurança do ambiente.

3. **Conforto**:
   - Automção inteligente, reduzindo a necessidade de intervenção manual.
   - Adaptação da iluminação às condições ambientais, garantindo conforto visual.

### Impactos Negativos
1. **Dependência Tecnológica**:
   - Necessidade de conexão WiFi para o funcionamento adequado do sistema.
   - Manutenção periódica dos sensores e do hardware envolvido.

2. **Custos**:
   - Investimento inicial para aquisição dos componentes e montagem do sistema.
   - Custos de manutenção e substituição dos sensores e dispositivos.

## Melhorias Futuras
1. Integração com uma interface web para controle remoto da iluminação.
2. Integração com outros sistemas residenciais, como HVAC e segurança.
3. Ajuste dinâmico dos parâmetros de detecção com base em dados de uso.
4. Registro e armazenamento histórico do consumo energético.

## Link do Vídeo
[Link para o vídeo no YouTube]

## Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


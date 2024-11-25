// Inclusão das bibliotecas necessárias
#include <WiFi.h>          // Biblioteca para conexão WiFi do ESP32
#include <PubSubClient.h>  // Biblioteca para comunicação MQTT
#include <Arduino.h>       // Biblioteca base do Arduino

// Definições do sistema para controle de comportamento
#define DEBUG true              // Ativa mensagens de debug no Serial Monitor
#define UPDATE_INTERVAL 2000    // Intervalo de atualização em milissegundos (2 segundos)

// Definição dos pinos utilizados no ESP32
const int LDR_PIN = 33;        // Pino analógico para o sensor de luz (LDR)
const int TRIG_PIN = 13;       // Pino digital para trigger do sensor ultrassônico
const int ECHO_PIN = 12;       // Pino digital para echo do sensor ultrassônico
const int LED_EXTERNO_1 = 15;  // Pino digital para LED azul (iluminação externa baixa)
const int LED_EXTERNO_2 = 17;  // Pino digital para LED amarelo 1 (iluminação externa alta)
const int LED_INTERNO = 18;    // Pino digital para LED amarelo 2 (iluminação interna)

// Limiares para tomada de decisão
const int LDR_NOITE = 500;     // Valor do LDR abaixo do qual considera-se noite
const int LDR_INTERNO = 300;   // Valor do LDR para ativar iluminação interna
const int DIST_PRESENCA = 200; // Distância em cm para detectar presença
const int DIST_PROXIMA = 100;  // Distância em cm para considerar presença próxima

// Valores de consumo de energia em kWh para cada LED
const float CONSUMO_LED_EXT1 = 0.05;  // Consumo do LED externo de baixa intensidade
const float CONSUMO_LED_EXT2 = 0.10;  // Consumo do LED externo de alta intensidade
const float CONSUMO_LED_INT = 0.07;   // Consumo do LED interno

// Configurações de rede
const char* WIFI_SSID = "Wokwi-GUEST";  // Nome da rede WiFi
const char* WIFI_PASS = "";             // Senha do WiFi (vazia para o Wokwi)
const char* MQTT_SERVER = "mqtt.eclipseprojects.io";  // Endereço do servidor MQTT

// Tópico MQTT para publicação do consumo de energia
const char* TOPIC_ENERGY_CONSUMPTION = "rm87775/home/energy/consumption";

// Objetos para comunicação
WiFiClient espClient;           // Cliente WiFi
PubSubClient client(espClient); // Cliente MQTT
unsigned long lastUpdate = 0;   // Variável para controle do tempo da última atualização

// Função para imprimir mensagens de debug
void debugPrint(String message) {
  #if DEBUG                     // Se DEBUG estiver ativado
    Serial.println(message);    // Imprime a mensagem no Serial Monitor
  #endif
}

// Configuração inicial dos pinos
void setupPins() {
  // Define o modo de operação de cada pino
  pinMode(LDR_PIN, INPUT);       // LDR como entrada analógica
  pinMode(TRIG_PIN, OUTPUT);     // TRIG como saída
  pinMode(ECHO_PIN, INPUT);      // ECHO como entrada
  pinMode(LED_EXTERNO_1, OUTPUT);// LED1 como saída
  pinMode(LED_EXTERNO_2, OUTPUT);// LED2 como saída
  pinMode(LED_INTERNO, OUTPUT);  // LED3 como saída
  
  // Inicializa todos os LEDs desligados
  digitalWrite(LED_EXTERNO_1, LOW);
  digitalWrite(LED_EXTERNO_2, LOW);
  digitalWrite(LED_INTERNO, LOW);
}

// Configuração da conexão WiFi
void setupWiFi() {
  debugPrint("\nConectando ao WiFi: " + String(WIFI_SSID));
  WiFi.begin(WIFI_SSID, WIFI_PASS);  // Inicia conexão WiFi

  // Aguarda conexão com timeout
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  // Verifica resultado da conexão
  if (WiFi.status() == WL_CONNECTED) {
    debugPrint("\nWiFi conectado - IP: " + WiFi.localIP().toString());
  } else {
    debugPrint("\nFalha na conexão WiFi - Operando offline");
  }
}

// Configuração do cliente MQTT
void setupMQTT() {
  client.setServer(MQTT_SERVER, 1883);  // Define servidor e porta MQTT
  debugPrint("MQTT configurado - Servidor: " + String(MQTT_SERVER));
}

// Função para medir distância com sensor ultrassônico
int medirDistancia() {
  // Gera pulso de trigger
  digitalWrite(TRIG_PIN, LOW);   // Garante nível baixo
  delayMicroseconds(2);         // Aguarda 2 microssegundos
  digitalWrite(TRIG_PIN, HIGH);  // Pulso alto
  delayMicroseconds(10);        // Mantém por 10 microssegundos
  digitalWrite(TRIG_PIN, LOW);   // Volta para nível baixo

  // Mede o tempo de retorno do eco
  long duration = pulseIn(ECHO_PIN, HIGH);
  // Calcula distância em centímetros
  int distance = duration * 0.034 / 2;
  
  return distance;
}

// Calcula e publica o consumo de energia via MQTT
void publicarConsumo() {
  float consumo = 0.0;
  
  // Soma o consumo de cada LED ativo
  if (digitalRead(LED_EXTERNO_1) == HIGH) consumo += CONSUMO_LED_EXT1;
  if (digitalRead(LED_EXTERNO_2) == HIGH) consumo += CONSUMO_LED_EXT2;
  if (digitalRead(LED_INTERNO) == HIGH) consumo += CONSUMO_LED_INT;

  // Formata consumo com 2 casas decimais
  String mensagemConsumo = String(consumo, 2);
  
  // Publica no MQTT se conectado
  if (client.connected()) {
    client.publish(TOPIC_ENERGY_CONSUMPTION, mensagemConsumo.c_str());
    debugPrint("Consumo publicado: " + mensagemConsumo + " kWh");
  }
}

// Controla o sistema de iluminação baseado nos sensores
void controlarIluminacao(int ldrValue, int distance) {
  // Controle da iluminação externa
  if (ldrValue < LDR_NOITE) {  // Se está escuro
    if (distance <= DIST_PRESENCA) {  // Se detectou presença
      // Ativa alta intensidade
      digitalWrite(LED_EXTERNO_1, HIGH);
      digitalWrite(LED_EXTERNO_2, HIGH);
      debugPrint("Iluminação Externa: Alta intensidade");
    } else {
      // Ativa baixa intensidade
      digitalWrite(LED_EXTERNO_1, HIGH);
      digitalWrite(LED_EXTERNO_2, LOW);
      debugPrint("Iluminação Externa: Baixa intensidade");
    }
  } else {  // Se está claro
    // Desliga iluminação externa
    digitalWrite(LED_EXTERNO_1, LOW);
    digitalWrite(LED_EXTERNO_2, LOW);
    debugPrint("Iluminação Externa: Desligada");
  }

  // Controle da iluminação interna
  if (ldrValue < LDR_INTERNO && distance < DIST_PROXIMA) {
    digitalWrite(LED_INTERNO, HIGH);  // Liga LED interno
    debugPrint("Iluminação Interna: Ligada");
  } else {
    digitalWrite(LED_INTERNO, LOW);   // Desliga LED interno
    debugPrint("Iluminação Interna: Desligada");
  }
  
  // Atualiza consumo após mudanças
  publicarConsumo();
}

// Reconecta ao servidor MQTT se necessário
void reconnectMQTT() {
  // Verifica se está desconectado e tem WiFi
  if (!client.connected() && WiFi.status() == WL_CONNECTED) {
    debugPrint("Tentando conexão MQTT...");
    // Tenta conectar
    if (client.connect("ESP32_Wokwi_Client")) {
      debugPrint("Conectado ao broker MQTT");
    } else {
      debugPrint("Falha na conexão MQTT - Tentando novamente em 5s");
    }
  }
}

// Função de configuração inicial
void setup() {
  Serial.begin(115200);  // Inicia comunicação serial
  debugPrint("\nIniciando sistema de automação...");
  
  setupPins();   // Configura pinos
  setupWiFi();   // Inicia WiFi
  setupMQTT();   // Configura MQTT
  
  debugPrint("Sistema pronto!");
}

// Loop principal
void loop() {
  unsigned long currentMillis = millis();  // Obtém tempo atual
  
  // Verifica se é hora de atualizar
  if (currentMillis - lastUpdate >= UPDATE_INTERVAL) {
    reconnectMQTT();  // Tenta reconexão MQTT se necessário
    
    // Lê sensores
    int ldrValue = analogRead(LDR_PIN);
    int distance = medirDistancia();
    
    // Imprime leituras para debug
    debugPrint("\n--- Leituras ---");
    debugPrint("LDR: " + String(ldrValue));
    debugPrint("Distância: " + String(distance) + " cm");
    
    // Atualiza iluminação e consumo
    controlarIluminacao(ldrValue, distance);
    
    lastUpdate = currentMillis;  // Atualiza tempo da última execução
  }
  
  client.loop();  // Mantém cliente MQTT ativo
}
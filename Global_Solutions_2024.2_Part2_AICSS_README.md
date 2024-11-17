
# Global Solutions 2024.2 - Parte 2: Artificial Intelligence with Computer Systems and Sensors (AICSS)

Este documento detalha a implementação da **Parte 2** do projeto GS 2024.2, que consiste no desenvolvimento de um circuito para controle inteligente de iluminação interna e externa utilizando ESP32 e sensores.

---

## Resumo do Projeto
O sistema utiliza:
- **Sensores LDR e Ultrassônico** para detectar condições de luz e presença.
- **LEDs Internos e Externos** representando a iluminação de uma residência.
- **ESP32** como microcontrolador principal para gerenciar as leituras dos sensores e controlar os LEDs.

---

## Componentes Utilizados
1. **ESP32:** Microcontrolador.
2. **Sensor LDR:** Detecta luminosidade.
3. **Sensor Ultrassônico:** Mede distância/presença.
4. **LEDs:**
   - Externo 1 (intensidade baixa).
   - Externo 2 (intensidade alta).
   - Interno.
5. **Resistores e Fios de Conexão.**
6. **Simulador Wokwi.**

---

## Lógica de Operação
1. **Iluminação Externa:**
   - Durante a noite (baixa luminosidade), o LED Externo 1 é ativado.
   - Presença detectada aumenta a intensidade com o LED Externo 2.
   - Durante o dia (alta luminosidade), os LEDs externos são desligados.

2. **Iluminação Interna:**
   - Ativada somente com baixa luz natural e presença detectada.
   - Desligada quando há luz suficiente ou ausência de presença.

---

## Código-Fonte
```cpp
#include <Arduino.h>

const int ldrPin = 34;        // Pino analógico para leitura do módulo LDR
const int trigPin = 13;       // Pino TRIG do sensor Ultrassom, usado para iniciar a medição de distância
const int echoPin = 12;       // Pino ECHO do sensor Ultrassom, para ler o tempo de resposta do pulso
const int ledExterno_1 = 15;  // LED Externo para iluminação de segurança, intensidade baixa
const int ledExterno_2 = 17;  // LED Externo para iluminação de segurança, intensidade alta
const int ledInterno = 18;    // LED Interno para iluminação de ambiente interno

void setup() {
  Serial.begin(9600);         // Inicializa a comunicação serial a 9600 bps
  pinMode(ldrPin, INPUT);     // Configura o pino do LDR como entrada
  pinMode(trigPin, OUTPUT);   // Configura o pino TRIG do Ultrassom como saída
  pinMode(echoPin, INPUT);    // Configura o pino ECHO do Ultrassom como entrada
  pinMode(ledExterno_1, OUTPUT); // Configura o pino do LED Externo 1 como saída
  pinMode(ledExterno_2, OUTPUT); // Configura o pino do LED Externo 2 como saída
  pinMode(ledInterno, OUTPUT);   // Configura o pino do LED Interno como saída
  Serial.println("Sistema iniciado");  // Mensagem inicial de confirmação
}

void loop() {
  int ldrValue = analogRead(ldrPin);  // Lê o valor do LDR, indicando intensidade de luz ambiente
  int distancia = medirDistancia();   // Chama função para medir a distância detectada pelo Ultrassom

  // Exibe no monitor serial os valores lidos dos sensores
  Serial.print("Intensidade de Luz (LDR): ");
  Serial.println(ldrValue);
  Serial.print("Distância detectada (cm): ");
  Serial.println(distancia);

  // Controle da Luz Externa: mantida acesa em baixa intensidade à noite e intensificada com presença
  if (ldrValue < 500) {                // Condição para baixa luminosidade externa (noite)
    if (distancia > 200) {             // Se não há presença próxima (distância > 200 cm)
      digitalWrite(ledExterno_1, HIGH); // Liga apenas o LED Externo 1 para baixa intensidade
      digitalWrite(ledExterno_2, LOW);  // Mantém o LED Externo 2 desligado
      Serial.println("Luz Externa: baixa intensidade ativada");
    }
    else if (distancia <= 200) {       // Se há presença próxima (distância <= 200 cm)
      digitalWrite(ledExterno_1, HIGH); // Liga o LED Externo 1 para baixa intensidade
      digitalWrite(ledExterno_2, HIGH); // Liga também o LED Externo 2 para aumentar intensidade
      Serial.println("Luz Externa: intensidade aumentada devido à presença");
    }
  } else {
    // Condição para alta luminosidade externa (dia)
    // Ambos os LEDs externos são desligados para economizar energia
    digitalWrite(ledExterno_1, LOW);
    digitalWrite(ledExterno_2, LOW);
    Serial.println("Luz Externa: desligada");
  }

  // Controle da Luz Interna: ligada com pouca luz natural e presença detectada
  if (ldrValue < 300 && distancia < 100) { // Se pouca luz natural e presença próxima (distância < 100 cm)
    digitalWrite(ledInterno, HIGH);        // Liga o LED Interno para melhorar a iluminação interna
    Serial.println("Luz Interna: ligada devido à presença e pouca luz natural");
  } else {
    // Condição para luz natural suficiente ou sem presença
    // O LED Interno é desligado para economizar energia
    digitalWrite(ledInterno, LOW);
    Serial.println("Luz Interna: desligada");
  }

  delay(2000); // Intervalo para estabilidade do sistema, evita leituras excessivas
}

// Função para medir a distância com o sensor Ultrassom
int medirDistancia() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  int duracao = pulseIn(echoPin, HIGH);
  int distancia = duracao * 0.034 / 2;
  return distancia;
}
```

---

## Resultados Esperados
- **Economia de Energia:** Redução no consumo ajustando a iluminação conforme necessidade.
- **Conforto e Segurança:** Ambiente ajustado automaticamente com base na luminosidade e presença.

---

## Próximos Passos
- Testar a simulação no Wokwi.
- Gravar um vídeo demonstrativo do funcionamento.

---


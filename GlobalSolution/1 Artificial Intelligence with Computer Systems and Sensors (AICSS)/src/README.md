
# Projeto de Otimização de Iluminação Residencial com ESP32 e Sensores

Este projeto utiliza o microcontrolador ESP32 com sensores de luminosidade (LDR) e proximidade (Ultrassom) para otimizar a iluminação de um ambiente residencial, promovendo economia de energia e melhorando a segurança. A iluminação externa é ajustada automaticamente conforme a luz ambiente e a presença de pessoas, enquanto a iluminação interna é acionada em função da ocupação e da luminosidade natural.

## Componentes Utilizados
- **ESP32**: Controlador do sistema.
- **Sensor de Luminosidade (LDR)**: Detecta a intensidade de luz natural.
- **Sensor Ultrassom**: Detecta presença para ajustar a iluminação.
- **LEDs**: Simulam as luzes interna e externa. Dois LEDs externos para intensidades de segurança baixa e alta e um LED interno para iluminação ambiente.

## Código e Funcionamento
O código (`codigo_esp32.ino`) controla a iluminação interna e externa com base nos dados dos sensores. Abaixo estão as principais condições do sistema:

- **Iluminação Externa**:
  - Em baixa luminosidade externa (à noite), o LED Externo 1 é ativado em baixa intensidade.
  - Se uma presença for detectada (distância ≤ 200 cm), o LED Externo 2 também é ativado, aumentando a intensidade de luz externa para segurança.
  - Durante o dia (alta luminosidade), ambos os LEDs externos são desligados.

- **Iluminação Interna**:
  - A luz interna é acionada em condições de pouca luz natural e presença próxima (distância < 100 cm).

## Testes no Wokwi
Para simular e testar este projeto no Wokwi:

1. **Acesse o Wokwi**: Entre no site [Wokwi](https://wokwi.com/) e carregue o circuito com ESP32, LDR, Ultrassom e LEDs.
2. **Configure os Pinos**:
   - LED Externo 1 (baixa intensidade): Conectado ao pino `15`.
   - LED Externo 2 (alta intensidade): Conectado ao pino `17`.
   - LED Interno: Conectado ao pino `18`.
   - LDR: Conectado ao pino `34`.
   - Sensor Ultrassom: Pinos `TRIG` e `ECHO` conectados aos pinos `13` e `12`.
3. **Execute o Código**:
   - Carregue o código `codigo_esp32.ino` no simulador e execute.
   - Use os controles do Wokwi para ajustar a luminosidade no LDR e simular presença no sensor Ultrassom.

### Testes Específicos
- **Teste de Iluminação Externa**:
  - Simule baixa luminosidade ambiente para verificar se o LED Externo 1 acende em baixa intensidade.
  - Em seguida, simule presença no Ultrassom (distância ≤ 200 cm) para verificar se o LED Externo 2 acende, aumentando a iluminação.
  - Ajuste a luminosidade para alta e verifique se ambos os LEDs externos desligam.

- **Teste de Iluminação Interna**:
  - Simule baixa luminosidade e presença próxima no Ultrassom (distância < 100 cm) para verificar se o LED Interno acende.
  - Aumente a luminosidade ou simule ausência para verificar se o LED Interno desliga.

### Observação dos Resultados
Monitore os logs no Serial Monitor para verificar mensagens de depuração, incluindo leituras de luminosidade e distância, além dos estados das luzes internas e externas.

## Considerações Finais
Este sistema visa a automação eficiente da iluminação, promovendo economia de energia e segurança. Em caso de falha no sensor ou ESP32, o sistema pode exigir manutenção. Sensores com maior alcance podem ser considerados para ambientes maiores.

**Vídeo de Demonstração**: [Insira o link do vídeo do YouTube aqui]

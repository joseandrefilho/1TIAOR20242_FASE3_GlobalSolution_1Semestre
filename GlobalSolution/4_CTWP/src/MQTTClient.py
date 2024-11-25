# MQTTClient.py
import paho.mqtt.client as mqtt
import pandas as pd
import time

class MQTTClient:
    """Classe que gerencia a comunicação com o broker MQTT."""

    def __init__(self, energy_manager):
        self.energy_manager = energy_manager
        self.client = mqtt.Client()
        self.client.on_message = self.on_message

    def connect(self, broker="mqtt.eclipseprojects.io", port=1883, topic="rm87775/home/energy/consumption"):
        """Conecta ao broker MQTT e inscreve no tópico."""
        self.client.connect(broker, port, 60)
        self.client.subscribe(topic)
        print(f"Conectado ao broker MQTT {broker} e inscrito no tópico {topic}.")

    def start(self):
        """Inicia a escuta do cliente MQTT."""
        self.connect()
        self.client.loop_forever()

    def on_message(self, client, userdata, msg):
        """Processa as mensagens recebidas do MQTT."""
        try:
            payload = msg.payload.decode()
            timestamp = pd.to_datetime(time.strftime("%Y-%m-%d %H:%M:%S"))

            if msg.topic == "rm87775/home/energy/consumption":
                consumption = float(payload)
                if self.energy_manager.current_source == "Energia Solar" and self.energy_manager.current_capacity is not None:
                    self.energy_manager.current_capacity -= consumption
                    self.energy_manager.current_capacity = max(self.energy_manager.current_capacity, 0)

                    # Atualizar a capacidade no dicionário
                    resource_name = self.energy_manager.selected_resource_name
                    self.energy_manager.resource_capacities[resource_name] = self.energy_manager.current_capacity

                new_row = {
                    "Timestamp": timestamp,
                    "Consumption": consumption,
                    "Tariff": self.energy_manager.current_tariff.get(self.energy_manager.current_source, 0.0),
                    "Energy_Source": self.energy_manager.current_source or "Desconhecido"
                }

                # Verifica se o DataFrame está vazio
                if self.energy_manager.data.empty:
                    self.energy_manager.data = pd.DataFrame([new_row])
                else:
                    self.energy_manager.data = pd.concat(
                        [self.energy_manager.data, pd.DataFrame([new_row])],
                        ignore_index=True
                    )
        except Exception as e:
            print(f"Erro ao processar mensagem MQTT: {type(e).__name__} - {e}")
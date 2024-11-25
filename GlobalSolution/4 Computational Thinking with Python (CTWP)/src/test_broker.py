import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT!")
        client.subscribe("rm87775/home/energy/consumption")
    else:
        print(f"Falha na conexão MQTT. Código de retorno: {rc}")

def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Substitua pelo broker que está funcionando
client.connect("mqtt.eclipseprojects.io", 1883)
client.loop_forever()

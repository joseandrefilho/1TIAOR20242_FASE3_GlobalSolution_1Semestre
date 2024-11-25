# main.py
from EnergyManager import EnergyManager
from GUI import GUI

if __name__ == "__main__":
    energy_manager = EnergyManager()
    energy_manager.start_mqtt_client()  # Iniciar o cliente MQTT antes da GUI

    gui = GUI(energy_manager)
    gui.start()
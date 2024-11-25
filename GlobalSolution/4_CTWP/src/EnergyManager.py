# EnergyManager.py
import pandas as pd
import requests
import warnings
import urllib3
from threading import Thread
from dotenv import load_dotenv
import os
from MQTTClient import MQTTClient

# Suprimir avisos de depreciação (opcional)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Suprimir avisos de SSL inseguros (se você optar por desativar a verificação SSL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Carregar variáveis de ambiente
load_dotenv()
api_key = os.getenv("ELECTRICITYMAP_API_KEY")

class EnergyManager:
    """Classe que gerencia as fontes de energia, tarifas, consumo e capacidade solar."""
    
    def __init__(self):
        # Inicializando o DataFrame com tipos de dados explícitos
        self.data = pd.DataFrame({
            "Timestamp": pd.Series(dtype='datetime64[ns]'),
            "Consumption": pd.Series(dtype='float'),
            "Tariff": pd.Series(dtype='float'),
            "Energy_Source": pd.Series(dtype='str')
        })
        # Variáveis que serão preenchidas com dados das APIs
        self.current_tariff = {}
        self.current_source = None
        self.solar_capacity = None
        self.current_capacity = None
        self.solar_carbon_intensity = None
        self.grid_carbon_intensity = None
        self.mqtt_client = MQTTClient(self)
        self.solar_resources = []
        self.selected_resource_name = None

        # Dicionário para armazenar a capacidade atual de cada recurso
        self.resource_capacities = {}

        # Buscar dados das APIs
        self.fetch_data_from_mockapi()
        self.fetch_carbon_intensity()

    def start_mqtt_client(self):
        """Inicia o cliente MQTT em uma thread separada."""
        mqtt_thread = Thread(target=self.mqtt_client.start, daemon=True)
        mqtt_thread.start()

    def fetch_data_from_mockapi(self):
        """Busca dados do MockAPI e atualiza os recursos solares disponíveis."""
        try:
            url = "https://joseandrefilho.mockable.io/rm87775/api/energy"
            response = requests.get(url, verify=False)  # Desativa a verificação SSL

            if response.status_code == 200:
                data = response.json()
                print("Dados recebidos da MockAPI:", data)
                self.solar_resources = data  # Armazena todos os recursos

                # Inicializar o dicionário de capacidades com os valores iniciais
                for resource in self.solar_resources:
                    resource_name = resource["resource_name"]
                    self.resource_capacities[resource_name] = float(resource["current_capacity"])
            else:
                print(f"Erro ao buscar dados do MockAPI: {response.status_code}")
                self.solar_resources = []
        except Exception as e:
            print(f"Erro na conexão com a API MockAPI: {type(e).__name__} - {e}")
            self.solar_resources = []

    def select_solar_resource(self, resource_name):
        """Atualiza o recurso solar selecionado e ajusta as tarifas com base na intensidade de carbono."""
        try:
            resource = next(item for item in self.solar_resources if item["resource_name"] == resource_name)
            self.selected_resource_name = resource_name
            self.solar_capacity = float(resource["solar_capacity"])  # Converte para float
            
            # Recuperar a capacidade atual armazenada para o recurso
            self.current_capacity = float(self.resource_capacities.get(resource_name, self.solar_capacity))

            # Tarifas base do MockAPI
            base_solar_tariff = float(resource["current_tariff"]["solar"])
            base_grid_tariff = float(resource["current_tariff"]["grid"])

            # Ajustar as tarifas com base na intensidade de carbono
            if self.grid_carbon_intensity and self.solar_carbon_intensity:
                carbon_factor = self.grid_carbon_intensity / (self.grid_carbon_intensity + self.solar_carbon_intensity)
                adjusted_solar_tariff = base_solar_tariff * (1 - carbon_factor)
                adjusted_grid_tariff = base_grid_tariff * (1 + carbon_factor)
            else:
                # Caso não tenha intensidade de carbono, usar tarifas base
                adjusted_solar_tariff = base_solar_tariff
                adjusted_grid_tariff = base_grid_tariff

            self.current_tariff["Energia Solar"] = round(adjusted_solar_tariff, 2)
            self.current_tariff["Rede Elétrica"] = round(adjusted_grid_tariff, 2)

            print(f"Recurso solar selecionado: {resource_name}")
            print(f"Tarifas ajustadas: Energia Solar = {self.current_tariff['Energia Solar']}, Rede Elétrica = {self.current_tariff['Rede Elétrica']}")
        except StopIteration:
            print(f"Recurso solar com nome '{resource_name}' não encontrado.")

    def fetch_carbon_intensity(self):
        """Busca a intensidade de carbono para energia solar e rede elétrica."""
        try:
            url = "https://api.electricitymap.org/v3/carbon-intensity/latest?zone=BR-NE"
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                self.grid_carbon_intensity = data.get("carbonIntensity", 200)
                self.solar_carbon_intensity = 50  # Valor fixo para energia solar
                print(f"Intensidade de carbono obtida: Rede Elétrica = {self.grid_carbon_intensity}, Energia Solar = {self.solar_carbon_intensity}")
            else:
                print(f"Erro ao buscar intensidade de carbono: {response.status_code}")
        except Exception as e:
            print(f"Erro na conexão com a API: {type(e).__name__} - {e}")

    def select_energy_source(self):
        """Seleciona automaticamente a fonte de energia com base na capacidade solar e tarifas."""
        if self.current_capacity is not None and self.current_capacity > 0:
            if self.solar_carbon_intensity is not None and self.grid_carbon_intensity is not None:
                if self.solar_carbon_intensity < self.grid_carbon_intensity:
                    self.current_source = "Energia Solar"
                elif self.current_tariff.get("Energia Solar", float('inf')) <= self.current_tariff.get("Rede Elétrica", float('inf')):
                    self.current_source = "Energia Solar"
                else:
                    self.current_source = "Rede Elétrica"
            else:
                self.current_source = "Energia Solar"
        else:
            self.current_source = "Rede Elétrica"

    def save_report(self):
        """Salva o relatório de consumo de energia em formato CSV."""
        file_name = "relatorio_consumo_energia.csv"
        self.data.to_csv(file_name, index=False)
        print(f"Relatório salvo como {file_name}")

    def calculate_costs(self):
        """Calcula o custo total com base nas tarifas e consumos registrados."""
        if not self.data.empty:
            total_cost = (self.data["Consumption"] * self.data["Tariff"]).sum()
            return total_cost
        return 0.0
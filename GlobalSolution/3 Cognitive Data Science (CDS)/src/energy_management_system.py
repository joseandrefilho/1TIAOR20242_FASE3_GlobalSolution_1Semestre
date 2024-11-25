import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import time
from threading import Thread
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
import requests
import warnings
import itertools
import urllib3

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
        messagebox.showinfo("Relatório Salvo", f"Relatório salvo como {file_name}")

    def calculate_costs(self):
        """Calcula o custo total com base nas tarifas e consumos registrados."""
        if not self.data.empty:
            total_cost = (self.data["Consumption"] * self.data["Tariff"]).sum()
            return total_cost
        return 0.0

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

class GUI:
    """Classe para gerenciar a interface gráfica com Tkinter."""
    
    def __init__(self, energy_manager):
        self.energy_manager = energy_manager
        self.root = tk.Tk()
        self.root.title("Sistema de Gerenciamento Energético")
        self.root.geometry("900x700")  # Definir tamanho da janela
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')  # Usar um tema moderno

        # Definir estilo personalizado
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('TButton', font=('Helvetica', 12))
        self.style.configure('TCombobox', font=('Helvetica', 12))

        # Definir estilos para as fontes de energia
        self.style.configure('Green.TLabel', background='green', foreground='white')
        self.style.configure('Red.TLabel', background='red', foreground='white')

        self.create_widgets()
        self.start_update_status()  # Inicia a atualização da GUI

    def create_widgets(self):
        """Cria os elementos da interface gráfica."""
        # Criar frames para organizar a interface
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        self.middle_frame = ttk.Frame(self.root)
        self.middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

        # Adicionar um título
        self.title_label = ttk.Label(self.top_frame, text="Sistema de Gerenciamento Energético", style='Title.TLabel')
        self.title_label.pack(pady=5)

        # Adicionar um separador
        self.separator = ttk.Separator(self.top_frame, orient='horizontal')
        self.separator.pack(fill=tk.X, pady=5)

        # Seção para seleção de recurso solar
        self.resource_label = ttk.Label(self.top_frame, text="Selecione o Recurso Solar:")
        self.resource_label.pack(pady=5)

        # Obter a lista de nomes de recursos solares disponíveis
        resource_names = [resource["resource_name"] for resource in self.energy_manager.solar_resources]
        self.selected_resource = tk.StringVar(self.root)

        if resource_names:
            self.selected_resource.set(resource_names[0])  # Seleciona o primeiro por padrão
            self.energy_manager.select_solar_resource(resource_names[0])  # Atualiza o recurso selecionado
        else:
            self.selected_resource.set('Nenhum recurso disponível')

        self.resource_menu = ttk.Combobox(
            self.top_frame, textvariable=self.selected_resource, values=resource_names, state="readonly", width=30
        )
        self.resource_menu.pack(pady=5)

        # Vincular a mudança de seleção ao método que atualiza o recurso
        if resource_names:
            self.resource_menu.bind("<<ComboboxSelected>>", self.on_resource_selected)
        else:
            messagebox.showwarning("Aviso", "Nenhum recurso solar disponível no momento.")

        # Seção para exibir informações
        info_frame = ttk.Frame(self.middle_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Labels de informação
        self.tariff_label = ttk.Label(info_frame, text="Tarifa Atual (R$/kWh):")
        self.tariff_label.pack(pady=5)

        # Label da fonte atual, que terá a cor alterada
        self.source_label = ttk.Label(info_frame, text="Fonte Atual:", style='TLabel')
        self.source_label.pack(pady=5, fill=tk.X)

        self.cost_label = ttk.Label(info_frame, text="Custo Total (R$):")
        self.cost_label.pack(pady=5)

        self.capacity_label = ttk.Label(info_frame, text="Capacidade Total:")
        self.capacity_label.pack(pady=5)

        self.current_capacity_label = ttk.Label(info_frame, text="Capacidade Atual:")
        self.current_capacity_label.pack(pady=5)

        # Botão para salvar relatório
        self.save_button = ttk.Button(info_frame, text="Salvar Relatório", command=self.energy_manager.save_report)
        self.save_button.pack(pady=20)

        # Seção para o gráfico
        graph_frame = ttk.Frame(self.middle_frame)
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_graph(graph_frame)

    def on_resource_selected(self, event):
        """Atualiza o recurso solar selecionado quando o usuário muda a seleção."""
        selected_name = self.selected_resource.get()
        self.energy_manager.select_solar_resource(selected_name)

    def create_graph(self, parent_frame):
        """Cria e configura o gráfico na interface."""
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Inicia a animação para atualizar o gráfico
        self.animation = FuncAnimation(
            self.fig,
            self.update_graph,
            frames=itertools.count(),
            interval=2000,
            cache_frame_data=False
        )

    def update_graph(self, _):
        """Atualiza o gráfico de consumo em tempo real."""
        if not self.energy_manager.data.empty:
            self.ax.clear()
            # Ordenar os dados por Timestamp
            data_sorted = self.energy_manager.data.sort_values(by="Timestamp")
            self.ax.plot(
                data_sorted["Timestamp"],
                data_sorted["Consumption"],
                label="Consumo (kWh)",
                color="#1f77b4",
                marker='o',
                linestyle='-'
            )
            self.ax.set_title("Consumo Energético em Tempo Real")
            self.ax.set_xlabel("Tempo")
            self.ax.set_ylabel("Consumo (kWh)")
            self.ax.legend(loc="upper left")
            self.ax.tick_params(axis="x", rotation=45)
            self.fig.tight_layout()

        # Atualiza o canvas do gráfico
        self.canvas.draw()

    def start_update_status(self):
        """Inicia a atualização periódica do status."""
        self.update_status()

    def update_status(self):
        """Atualiza o status da interface gráfica com os dados em tempo real."""
        self.energy_manager.select_energy_source()
        total_cost = self.energy_manager.calculate_costs()
        self.update_labels(total_cost)
        # Agendar a próxima atualização em 1 segundo
        self.root.after(1000, self.update_status)

    def update_labels(self, total_cost):
        """Atualiza os labels da interface gráfica."""
        try:
            solar_tariff = self.energy_manager.current_tariff.get('Energia Solar', 'N/A')
            grid_tariff = self.energy_manager.current_tariff.get('Rede Elétrica', 'N/A')
            current_source = self.energy_manager.current_source or 'Desconhecido'
            solar_capacity = float(self.energy_manager.solar_capacity) if self.energy_manager.solar_capacity is not None else 'N/A'
            current_capacity = float(self.energy_manager.current_capacity) if self.energy_manager.current_capacity is not None else 'N/A'

            self.tariff_label["text"] = f"Tarifa Atual (R$/kWh):\nEnergia Solar: {solar_tariff} | Rede Elétrica: {grid_tariff}"
            self.cost_label["text"] = f"Custo Total (R$): {total_cost:.2f}"
            self.capacity_label["text"] = f"Capacidade Total: {solar_capacity:.2f} kWh" if isinstance(solar_capacity, float) else f"Capacidade Total: {solar_capacity}"
            self.current_capacity_label["text"] = f"Capacidade Atual: {current_capacity:.2f} kWh" if isinstance(current_capacity, float) else f"Capacidade Atual: {current_capacity}"

            # Atualizar o label da fonte atual com cor
            self.source_label["text"] = f"Fonte Atual: {current_source}"

            if current_source == "Energia Solar":
                self.source_label.configure(style='Green.TLabel')
            elif current_source == "Rede Elétrica":
                self.source_label.configure(style='Red.TLabel')
            else:
                self.source_label.configure(style='TLabel')  # Estilo padrão
        except Exception as e:
            print(f"Erro ao atualizar labels: {type(e).__name__} - {e}")

    def start(self):
        """Inicia a interface gráfica."""
        self.root.mainloop()

if __name__ == "__main__":
    energy_manager = EnergyManager()
    energy_manager.start_mqtt_client()  # Iniciar o cliente MQTT antes da GUI

    gui = GUI(energy_manager)
    gui.start()
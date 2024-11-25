# GUI.py
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import itertools

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
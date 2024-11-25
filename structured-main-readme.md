# Sistema Integrado de Gestão Energética - FIAP Global Solution 2024/1

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP" border="0" width=40% height=40%></a>
</p>

## Índice
1. [Informações do Projeto](#informações-do-projeto)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Subprojetos](#subprojetos)
4. [Tecnologias Utilizadas](#tecnologias-utilizadas)
5. [Instalação e Configuração](#instalação-e-configuração)
6. [Documentação](#documentação)

## Informações do Projeto

**Turma:** 1TIAOR - 2024/1
**Disciplina:** Global Solution - Fase 3
**Tema:** Gestão e Otimização Energética Residencial

### Equipe
- **Aluno:** José Andre Filho - RM87775
  - [LinkedIn](https://www.linkedin.com/in/joseandrefilho)
  - [GitHub](https://github.com/joseandrefilho)

### Professores
- **Tutor:** Lucas Gomes Moreira
- **Coordenador:** André Godoi Chiovato

## Estrutura do Projeto

```plaintext
1TIAOR20242_FASE3_GlobalSolution_1Semestre/
├── GlobalSolution/
│   ├── 1_AICSS/               # Automação ESP32
│   │   └── src/
│   │       ├── diagram.json   # Circuito Wokwi
│   │       └── sketch.ino     # Código ESP32
│   │
│   ├── 2_SCR/                 # Análise R
│   │   ├── src/
│   │   │   ├── main.R        # Script principal
│   │   │   ├── part1.R       # Configurações
│   │   │   ├── part2.R       # Análises
│   │   │   └── part3.R       # Visualizações
│   │   └── data/
│   │
│   ├── 3_CDS/                 # Banco de Dados
│   │   ├── mer/
│   │   │   └── script.ddl
│   │   └── src/
│   │       └── notebooks/
│   │
│   └── 4_CTWP/               # Sistema Python
│       └── src/
│           └── energy_management_system.py
│
├── assets/
│   └── logo-fiap.png
├── requirements.txt
└── README.md
```

## Subprojetos

### 1. AICSS - Automação de Iluminação
Sistema de automação residencial com ESP32 para controle inteligente de iluminação.
- [Documentação AICSS](GlobalSolution/1_AICSS/README.md)
- [Demonstração no Wokwi](link-do-wokwi)
- [Vídeo de Funcionamento](link-do-youtube)

### 2. SCR - Análise Estatística
Análise exploratória de dados energéticos da ANEEL usando R.
- [Documentação SCR](GlobalSolution/2_SCR/README.md)
- **Scripts:**
  - `main.R`: Orquestração da análise
  - `part1.R`: Preparação de dados
  - `part2.R`: Análises estatísticas
  - `part3.R`: Visualizações

### 3. CDS - Pipeline de Dados
Sistema de armazenamento e análise em Oracle Database.
- [Documentação CDS](GlobalSolution/3_CDS/README.md)
- **Componentes:**
  - Modelo relacional
  - Scripts DDL
  - Notebooks de análise
  - Pipeline ETL

### 4. CTWP - Sistema de Gerenciamento
Interface gráfica em Python para monitoramento energético.
- [Documentação CTWP](GlobalSolution/4_CTWP/README.md)
- **Funcionalidades:**
  - Dashboard em tempo real
  - Integração MQTT
  - Relatórios automatizados

## Tecnologias Utilizadas

### Hardware
- ESP32
- Sensor LDR
- Sensor Ultrassônico HC-SR04
- LEDs

### Software
- **Linguagens:**
  - C++ (Arduino)
  - R
  - Python
  - SQL (Oracle)
- **Frameworks/Bibliotecas:**
  - Tkinter
  - ggplot2
  - pandas
  - matplotlib
- **Ferramentas:**
  - Wokwi
  - RStudio
  - Oracle SQL Developer
  - Jupyter Notebooks

## Instalação e Configuração

### Pré-requisitos
```bash
# Python 3.8+
python --version

# R 4.0+
R --version

# Oracle Database 19c+
sqlplus -v
```

### Configuração do Ambiente
```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/1TIAOR20242_FASE3_GlobalSolution_1Semestre.git
cd 1TIAOR20242_FASE3_GlobalSolution_1Semestre

# 2. Ambiente Python
python -m venv env
source env/bin/activate  # Linux/Mac
.\env\Scripts\activate   # Windows
pip install -r requirements.txt

# 3. Pacotes R
Rscript -e "install.packages(c('tidyverse', 'ggplot2', 'dplyr'))"

# 4. Banco de Dados
sqlplus / as sysdba @3_CDS/mer/script.ddl
```

## Documentação

### Links Importantes
- [Documentação Técnica Completa](link-do-pdf)
- [Apresentação do Projeto](link-da-apresentacao)
- [Vídeo Demonstrativo](link-do-video)

### Manuais por Módulo
- [Manual do Sistema de Automação](GlobalSolution/1_AICSS/README.md)
- [Guia de Análise Estatística](GlobalSolution/2_SCR/README.md)
- [Documentação do Banco de Dados](GlobalSolution/3_CDS/README.md)
- [Manual do Usuário do Sistema](GlobalSolution/4_CTWP/README.md)

## Licença

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">
<a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sob <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY 4.0</a>
</p>

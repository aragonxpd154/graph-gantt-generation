import csv
import sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QMessageBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# Variável para armazenar as atividades
atividades = []

# Função para converter uma string em um objeto de data
def parse_data(data_str):
    if isinstance(data_str, str):
        try:
            return datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            return datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
    return data_str

# Função para adicionar uma nova atividade
def adicionar_atividade():
    atividade = entry_atividade.text()
    inicio = parse_data(entry_inicio.text())
    fim = parse_data(entry_fim.text())

    if atividade and inicio and fim:
        atividades.append((atividade, inicio, fim))
        update_grafico()
        update_listbox()
        clear_fields()
        save_activities()
    else:
        QMessageBox.warning(window, "Aviso", "Preencha todos os campos!")

# Função para editar uma atividade existente
def editar_atividade():
    atividade_selecionada = listbox_atividades.currentRow()
    if atividade_selecionada >= 0:
        atividade_index = atividade_selecionada
        atividade_atual = atividades[atividade_index]
        atividade = entry_atividade.text()
        inicio = entry_inicio.text()
        fim = entry_fim.text()
        
        if atividade and inicio and fim:
            atividades[atividade_index] = (atividade, inicio, fim)
            update_grafico()
            update_listbox()
            clear_fields()
            save_activities()
        else:
            QMessageBox.warning(window, "Aviso", "Preencha todos os campos!")
    else:
        QMessageBox.warning(window, "Aviso", "Selecione uma atividade para editar!")

# Função para excluir uma atividade existente
def excluir_atividade():
    atividade_selecionada = listbox_atividades.currentRow()
    if atividade_selecionada >= 0:
        atividade_index = atividade_selecionada
        atividades.pop(atividade_index)
        update_grafico()
        update_listbox()
        clear_fields()
        save_activities()
    else:
        QMessageBox.warning(window, "Aviso", "Selecione uma atividade para excluir!")

# Função para limpar os campos de entrada
def clear_fields():
    entry_atividade.clear()
    entry_inicio.clear()
    entry_fim.clear()



# Função para atualizar a lista de atividades
def update_listbox():
    listbox_atividades.clear()
    for atividade in atividades:
        listbox_atividades.addItem(atividade[0])

# Função para preencher os campos de entrada com os dados da atividade selecionada
def preencher_campos():
    atividade_selecionada = listbox_atividades.currentRow()
    if atividade_selecionada >= 0:
        atividade_index = atividade_selecionada
        atividade_atual = atividades[atividade_index]
        clear_fields()
        entry_atividade.setText(atividade_atual[0])
        entry_inicio.setText(atividade_atual[1])
        entry_fim.setText(atividade_atual[2])

# Função para salvar as atividades em um arquivo .dat
def save_activities():
    with open("atividades.dat", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(atividades)

# Função para carregar as atividades de um arquivo .dat
def load_activities():
    try:
        with open("atividades.dat", "r") as file:
            reader = csv.reader(file)
            atividades.clear()
            for row in reader:
                atividades.append(row)
    except FileNotFoundError:
        pass

# Classe principal da aplicação
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuração da janela
        self.setWindowTitle("Configuração do Gráfico de Gantt")
        self.setGeometry(100, 100, 800, 600)

        # Variável para armazenar as atividades
        self.atividades = []
        
        # Rótulos e campos de entrada
        label_atividade = QLabel("Atividade:", self)
        label_atividade.move(10, 10)
        self.entry_atividade = QLineEdit(self)
        self.entry_atividade.move(10, 30)

        label_inicio = QLabel("Data de Início (dd/mm/aaaa):", self)
        label_inicio.move(10, 60)
        self.entry_inicio = QLineEdit(self)
        self.entry_inicio.move(10, 80)

        label_fim = QLabel("Data de Fim (dd/mm/aaaa):", self)
        label_fim.move(10, 110)
        self.entry_fim = QLineEdit(self)
        self.entry_fim.move(10, 130)

        # Botões
        button_adicionar = QPushButton("Adicionar", self)
        button_adicionar.move(10, 160)
        button_adicionar.clicked.connect(adicionar_atividade)

        button_editar = QPushButton("Editar", self)
        button_editar.move(10, 190)
        button_editar.clicked.connect(editar_atividade)

        button_excluir = QPushButton("Excluir", self)
        button_excluir.move(10, 220)
        button_excluir.clicked.connect(excluir_atividade)

        # Lista de atividades
        self.listbox_atividades = QListWidget(self)
        self.listbox_atividades.setGeometry(150, 10, 240, 200)
        self.listbox_atividades.itemClicked.connect(preencher_campos)

        # Configuração do gráfico
        self.fig = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
        self.ax.xaxis.set_major_locator(mdates.YearLocator())

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Carrega as atividades do arquivo .dat
        load_activities()

        # Exibe o gráfico e a lista de atividades inicialmente
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.update_grafico()
        self.update_listbox()

    def update_grafico(self):
        self.ax.clear()
        for i, atividade in enumerate(self.atividades):
            atividade, inicio, fim = atividade
            inicio = parse_data(inicio)
            fim = parse_data(fim)
            self.ax.barh(i, width=(fim - inicio).days, left=inicio, height=0.6, align='center', color='blue')

        self.ax.set_yticks(range(len(self.atividades)))
        self.ax.set_yticklabels([atividade[0] for atividade in self.atividades])
        self.ax.set_xlabel("Data")
        self.ax.set_ylabel("Atividade")
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
        self.ax.xaxis.set_major_locator(mdates.YearLocator())

        self.canvas.draw()

    def update_listbox(self):
        self.listbox_atividades.clear()
        for atividade in self.atividades:
            self.listbox_atividades.addItem(atividade[0])

# Configuração da aplicação
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())

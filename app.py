import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.font_manager as fm
from tkinter import *
from tkinter import messagebox

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
    atividade = entry_atividade.get()
    inicio = parse_data(entry_inicio.get())
    fim = parse_data(entry_fim.get())

    if atividade and inicio and fim:
        atividades.append((atividade, inicio, fim))
        update_grafico()
        update_listbox()
        clear_fields()
        save_activities()
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")

# Função para editar uma atividade existente
def editar_atividade():
    atividade_selecionada = listbox_atividades.curselection()
    if atividade_selecionada:
        atividade_index = atividade_selecionada[0]
        atividade_atual = atividades[atividade_index]
        atividade = entry_atividade.get()
        inicio = entry_inicio.get()
        fim = entry_fim.get()
        
        if atividade and inicio and fim:
            atividades[atividade_index] = (atividade, inicio, fim)
            update_grafico()
            update_listbox()
            clear_fields()
            save_activities()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
    else:
        messagebox.showwarning("Aviso", "Selecione uma atividade para editar!")

# Função para excluir uma atividade existente
def excluir_atividade():
    atividade_selecionada = listbox_atividades.curselection()
    if atividade_selecionada:
        atividade_index = atividade_selecionada[0]
        atividades.pop(atividade_index)
        update_grafico()
        update_listbox()
        clear_fields()
        save_activities()
    else:
        messagebox.showwarning("Aviso", "Selecione uma atividade para excluir!")

# Função para limpar os campos de entrada
def clear_fields():
    entry_atividade.delete(0, END)
    entry_inicio.delete(0, END)
    entry_fim.delete(0, END)

# Função para atualizar o gráfico
def update_grafico():
    ax.clear()
    for i, atividade in enumerate(atividades):
        atividade, inicio, fim = atividade
        inicio = parse_data(inicio)
        fim = parse_data(fim)
        ax.barh(i, width=(fim - inicio).days, left=inicio, height=0.6, align='center', color='blue')

    ax.set_yticks(range(len(atividades)))
    ax.set_yticklabels([atividade[0] for atividade in atividades])
    ax.set_xlabel("Data")
    ax.set_ylabel("Atividade")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
    ax.xaxis.set_major_locator(mdates.YearLocator())

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Função para atualizar a lista de atividades
def update_listbox():
    listbox_atividades.delete(0, END)
    for atividade in atividades:
        listbox_atividades.insert(END, atividade[0])

# Função para preencher os campos de entrada com os dados da atividade selecionada
def preencher_campos(event):
    atividade_selecionada = listbox_atividades.curselection()
    if atividade_selecionada:
        atividade_index = atividade_selecionada[0]
        atividade_atual = atividades[atividade_index]
        clear_fields()
        entry_atividade.insert(END, atividade_atual[0])
        entry_inicio.insert(END, atividade_atual[1])
        entry_fim.insert(END, atividade_atual[2])

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

# Configuração da janela
window = Tk()
window.title("Configuração do Gráfico de Gantt")
window.geometry("400x400")

# Rótulos e campos de entrada
label_atividade = Label(window, text="Atividade:")
label_atividade.pack()
entry_atividade = Entry(window)
entry_atividade.pack()

label_inicio = Label(window, text="Data de Início (dd/mm/aaaa):")
label_inicio.pack()
entry_inicio = Entry(window)
entry_inicio.pack()

label_fim = Label(window, text="Data de Fim (dd/mm/aaaa):")
label_fim.pack()
entry_fim = Entry(window)
entry_fim.pack()

# Botões
button_adicionar = Button(window, text="Adicionar", command=adicionar_atividade)
button_adicionar.pack()

button_editar = Button(window, text="Editar", command=editar_atividade)
button_editar.pack()

button_excluir = Button(window, text="Excluir", command=excluir_atividade)
button_excluir.pack()

# Lista de atividades
listbox_atividades = Listbox(window)
listbox_atividades.pack()

# Configuração do gráfico
fig, ax = plt.subplots(figsize=(10, 6))

# Formatação das datas
date_fmt = mdates.DateFormatter('%d/%m/%Y')
ax.xaxis.set_major_formatter(date_fmt)
ax.xaxis.set_major_locator(mdates.YearLocator())

# Carrega as atividades do arquivo .dat
load_activities()

# Exibe o gráfico e a lista de atividades inicialmente
update_grafico()
update_listbox()

# Vincula a função de preencher campos ao evento de seleção na lista de atividades
listbox_atividades.bind('<<ListboxSelect>>', preencher_campos)

# Configuração da fonte
font_name = "Arial"
plt.rcParams["font.family"] = font_name

# Exibe a janela
window.mainloop()

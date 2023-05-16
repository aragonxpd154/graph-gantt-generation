#!/bin/bash

# Atualiza os repositórios
sudo apt update

# Instala os pacotes necessários
sudo apt install python3 python3-pip python3-tk -y
pip3 install matplotlib

# Executa o script Python
python3 app.py

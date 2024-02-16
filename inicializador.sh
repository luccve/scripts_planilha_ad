#!/bin/bash

# Criação do ambiente virtual
python3 -m venv venv

# Ativação do ambiente virtual
source ./venv/bin/activate

# Atualização do pip
python3 -m pip install --upgrade pip

# Instalação dos requisitos
python3 -m pip install -r requirements.txt


echo "Ambiente configurado e requisitos instalados com sucesso!"

echo "Inicializando programa!"

python3 interface.py

deactivate
@echo off

:: Criação do ambiente virtual
python -m venv venv

:: Ativação do ambiente virtual
call venv\Scripts\activate

:: Atualização do pip
python -m pip install --upgrade pip

:: Instalação dos requisitos
python -m pip install -r requirements.txt

echo Ambiente configurado e requisitos instalados com sucesso!

echo Inicializando programa!

:: Executa o script Python
python interface.py

:: Desativação do ambiente virtual
deactivate

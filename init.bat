@echo off
cd /d %~dp0

if exist SDAlthE\venv\Scripts\python310.exe (
    echo Iniciando com ambiente virtual...
    SDAlthE\venv\Scripts\python310.exe SDAlthE\main.py
) else (
    echo Ambiente virtual nao encontrado, usando Python do sistema...
    python main.py
)

pause
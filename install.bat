@echo off
python -m venv venv
call venv\Scripts\activate
call python -m pip install --upgrade pip
call python -m pip install -r requirements-windows.txt

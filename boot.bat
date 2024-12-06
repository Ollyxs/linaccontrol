@echo off
call venv\Scripts\activate
call uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload


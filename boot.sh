#!/bin/bash

source venv/bin/activate
uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload

#!/bin/bash
# Simple script to run the FastAPI development server

# Use the virtual environment's Python
.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000


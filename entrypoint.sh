#!/bin/sh

# Executa as migrações 
poetry run alembic upgrade head

# Inicia a aplicação 
poetry run fastapi run fast_zero/app.py
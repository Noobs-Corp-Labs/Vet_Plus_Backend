"""
Service de exemplo para execução de tarefas em background.

Uso:
- Criar funções que serão rodadas de forma assíncrona (ex: enviar email).
- Usar `process_background_task` para adicionar a função à fila do FastAPI.

Esse arquivo serve como TEMPLATE para criação de novos services de background.
"""

from fastapi import BackgroundTasks, Depends
import uuid
from app.logger import logger

def send_email(email: str):
    """Exemplo de função simples que roda em background."""
    logger.info(f"Sending email to {email}")
    return True

def process_background_task(bg_tasks: BackgroundTasks, task_function, *args, **kwargs):
    """Wrapper para registrar uma função no BackgroundTasks."""
    task_id = str(uuid.uuid4())
    bg_tasks.add_task(lambda: task_function(*args, **kwargs))
    return task_id
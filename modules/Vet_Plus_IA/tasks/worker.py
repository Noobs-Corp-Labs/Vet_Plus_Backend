import threading
import queue
import time

from tasks.questions_generator import generate_question
from utils import save_list_to_txt

# fila de tarefas e variáveis de controle
task_queue = queue.Queue()
processed_count = 0
total_tasks = 0
status = "No task"
task_name = ""
lock = threading.Lock()


# inicia ou adiciona tarefas à fila
def enqueue_tasks(ask, so, subj):
    global total_tasks, lock, status, task_name

    list_of_tasks = []

    list_of_tasks.append(ask)

    save_list_to_txt(list_of_tasks, "list_of_tasks.txt")

    with lock:
        total_tasks += len(list_of_tasks)

    for task in list_of_tasks:
        task_queue.put((task, so, subj))

    # Iniciar a thread de worker apenas uma vez, se ainda não estiver rodando
    if not hasattr(enqueue_tasks, 'worker_started'):
        status = "Working"
        task_name = ""
        worker_thread = threading.Thread(target=dequeue_tasks, daemon=True)
        worker_thread.start()
        enqueue_tasks.worker_started = True

    return len(list_of_tasks) # Ok

# processa os itens da fila
def dequeue_tasks():
    global processed_count, task_name

    while True:
        try:
            task = task_queue.get(timeout=3)
        except queue.Empty:
            reset_progress()
            break

        generate_question(task[0])
        task_name = task[1] + " - " + task[2]

        with lock:
            processed_count += 1
        task_queue.task_done()

# retorna o progresso
def get_progress():
    global processed_count, total_tasks, status, task_name

    with lock:
        percent = (processed_count / total_tasks) * 100 if total_tasks > 0 else 0
    return {'processed': processed_count, 'total': total_tasks, 'progress': round(percent, 2), 'status' : status, 'task_name': task_name}


# reseta o progresso
def reset_progress():
    global processed_count, total_tasks, task_name, status
    with lock:
        processed_count = 0
        total_tasks = 0
        task_name = ""
        status = "Done"
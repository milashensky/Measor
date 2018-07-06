import os

BASE_DIR = os.path.join(os.path.dirname(__file__))
TASKS_DIR = os.path.join(BASE_DIR, 'tasks')
DEBUG = True


if not os.path.exists(TASKS_DIR):
    os.makedirs(TASKS_DIR)

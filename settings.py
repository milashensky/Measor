import os

BASE_DIR = os.path.join(os.path.dirname(__file__))
TASKS_DIR = os.path.join(BASE_DIR, 'tasks')
AUTH_FILE_PATH = os.path.join(BASE_DIR, 'auth.txt')
AUTH_SALT = b'0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5'

DEBUG = False

MAX_LOGS_COUNT = 100
MAX_LOG_LIFE_DAYS = 7

if not os.path.exists(TASKS_DIR):
    os.makedirs(TASKS_DIR)

###########################
# Load LOCAL_SETTINGS
###########################
try:
    from types import ModuleType
    import local_settings
    for key in dir(local_settings):
        value = getattr(local_settings, key)
        if not key.startswith('__') and not isinstance(value, ModuleType):
            globals()[key] = value
except ImportError:
    pass

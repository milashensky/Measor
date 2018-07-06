import json
import os

from datetime import datetime
from flask import current_app as app


def build_conf(data):
    out = {
        "name": data.get('name'),
        "interval": data.get('interval'),
        "interval_units": data.get("interval_units"),
        "created": datetime.now().timestamp()
    }
    return json.dumps(out)


def get_tasks():
    tasks = []
    names = list(os.walk(app.config['TASKS_DIR']))[0][1]
    for name in names:
        f = open(os.path.join(app.config['TASKS_DIR'], name, 'conf.json'), 'r')
        tasks.append(json.loads(f.read()))
    return tasks

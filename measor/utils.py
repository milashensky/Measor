import json
import os
import hashlib
import binascii

from slugify import slugify
from datetime import datetime
from flask import current_app as app


def build_conf(data):
    out = {
        "name": data.get('name'),
        "interval": data.get('interval'),
        "interval_units": data.get("interval_units"),
        "created": datetime.now().timestamp(),
        "slug": slugify(data.get('name')),
    }
    return json.dumps(out)


def get_tasks():
    tasks = []
    names = list(os.walk(app.config['TASKS_DIR']))[0][1]
    for name in names:
        try:
            f = open(os.path.join(app.config['TASKS_DIR'], name, 'conf.json'), 'r')
            tasks.append(json.loads(f.read()))
        except FileNotFoundError:
            pass
    return tasks


def check_auth(username, password):
    path = app.config.get('AUTH_FILE_PATH')
    pass_str = 'username=%s; password=%s' % (username, password)
    dk = hashlib.pbkdf2_hmac('sha256', pass_str.encode(), app.config.get('AUTH_SALT'), 100000)
    token = binascii.hexlify(dk).decode()
    try:
        f = open(path, 'r')
        content = f.readlines()
        for line in content:
            if line.strip() == token:
                return True
    except FileNotFoundError:
        pass
    return False

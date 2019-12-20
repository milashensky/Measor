import os
import json
import datetime
import base64

from flask import request, abort, current_app as app

from measor.mixins import AuthRequered, TaskRequeredMixin, ApiMixin, SaveTaskMixin
from measor.utils import get_tasks, get_log_status, check_auth
from measor.filters import decodeUnicode


class ApiTaskLogs(AuthRequered, TaskRequeredMixin, ApiMixin):
    methods = ['GET']

    def get_item(self, name):
        context = {}
        context['status'] = False
        try:
            with open(os.path.join(self.logs_path, name + '.txt'), 'r', encoding='utf-8') as f:
                data = f.readlines()
                context['status'] = get_log_status(self.task.get('slug', ''), name + '.txt')
                context['data'] = [decodeUnicode(i) for i in data]
                context['name'] = name
        except Exception:
            abort(404)
        return context

    def get(self, *args, **kwargs):
        dirpath = os.path.join(app.config['TASKS_DIR'], kwargs.get('slug', ''))
        self.logs_path = os.path.join(dirpath, 'logs')
        log_name = kwargs.get('log_name')
        if log_name:
            return self.get_item(log_name)
        try:
            logs_names = list(os.walk(self.logs_path))[0][2]
        except IndexError:
            logs_names = []
        if self.task.get('max_logs_count'):
            logs_names = logs_names[:int(self.task.get('max_logs_count'))]
        logs_names.sort(reverse=True)
        logs = []
        if logs_names:
            for name in logs_names:
                date = int(name.split('log')[1].split('.')[0])
                if int(self.task.get('last_run', 0)) - date > 0:
                    name = name.split('.')[0]
                    logs.append({"date": date, "name": name, 'status': get_log_status(self.task.get('slug', ''), name + '.txt')})
        return logs


class ApiTask(AuthRequered, TaskRequeredMixin, ApiMixin, SaveTaskMixin):
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    fields = ('interval_units', 'interval', 'name', 'code')

    def get(self, *args, **kwargs):
        return self.task

    def build_task(self):
        self.task['build_now'] = True
        f = open(os.path.join(app.config['TASKS_DIR'], self.task.get('slug', ''), 'conf.json'), 'w')
        f.write(json.dumps(self.task))
        f.close()
        return {'success': True}

    def toggle_pause(self):
        if self.task.get('pause', False):
            self.task['pause'] = False
        else:
            self.task['pause'] = True
        f = open(os.path.join(app.config['TASKS_DIR'], self.task.get('slug', ''), 'conf.json'), 'w')
        f.write(json.dumps(self.task))
        f.close()
        return {'success': True, "paused": self.task['pause']}

    def post(self, *args, **kwargs):
        data = json.loads(request.data.decode())
        if data.get('action') == 'build_now':
            return self.build_task()
        if data.get('action') == 'pause':
            return self.toggle_pause()
        return {'success': False}

    def put(self, *args, **kwargs):
        return self.save_task(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.task['wait_for_delete'] = True
        f = open(os.path.join(app.config['TASKS_DIR'], self.task.get('slug', ''), 'conf.json'), 'w')
        f.write(json.dumps(self.task))
        f.close()
        return {'success': True}


class ApiTasks(AuthRequered, ApiMixin, SaveTaskMixin):
    methods = ['GET', 'POST']
    fields = ('interval_units', 'interval', 'name', 'code')

    def get(self, *args, **kwargs):
        return get_tasks(with_run_status=True, last_logs=request.args.get('last_statuses'))

    def post(self, *args, **kwargs):
        return self.save_task(*args, **kwargs)


class ApiStats(AuthRequered, ApiMixin):
    methods = ['GET']

    def get(self, *args, **kwargs):
        tasks = get_tasks(with_run_status=True)
        running = 0
        paused = 0
        success = 0
        fail = 0
        for task in tasks:
            if task.get('last_status'):
                success += 1
            else:
                fail += 1
            if task.get('pause'):
                paused += 1
            if task['running']:
                running += 1
        data = {
            'now': datetime.datetime.now().timestamp(),
            'tasks_total': len(tasks),
            'failed': fail,
            'succeeded': success,
            'running': running,
            'paused': paused
        }
        return data


class ApiContext(ApiMixin):
    methods = ['GET']

    def get(self, *args, **kwargs):
        auth = request.authorization
        if auth and check_auth(auth.username, auth.password):
            return {
                'id': 1,
                "defaults": {
                    'code': "from splinter import Browser\n\nwith Browser('chrome') as browser:"
                    '\n    browser.visit("http://www.google.com")',
                    'max_logs_count': app.config['MAX_LOGS_COUNT'],
                    'max_log_life': app.config['MAX_LOG_LIFE_DAYS']
                }
            }
        return {'id': None}


class LoginApi(ApiMixin):
    methods = ['POST']

    def post(self, *args, **kwargs):
        if check_auth(self.data.get('username'), self.data.get('password')):
            auth = self.data.get('username') + ':' + self.data.get('password')
            return {"state": True, 'token': base64.encodebytes(auth.encode()).decode().strip()}
        return {"state": False, "errors": ['Incorrect user or password']}


class LogoutApi(ApiMixin):
    methods = ['POST']

    def post(self, *args, **kwargs):
        request.authorization = None
        return {"state": True}

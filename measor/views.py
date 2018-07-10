import os
import json

from flask import request, Response, abort, redirect, url_for, current_app as app
from flask.views import View
from slugify import slugify

from measor.mixins import AuthRequered, TemplateView, TaskRequeredMixin, ApiMixin
from measor.utils import build_conf, get_tasks


class IndexView(AuthRequered, TemplateView):
    template_name = 'index.html'
    methods = ['GET']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class CreateTaskView(AuthRequered, TemplateView):
    template_name = 'create.html'
    fields = ('interval_units', 'interval', 'name', 'code')
    task = {}

    def get_context_data(self, *args, **kwargs):
        context = kwargs or {"data": {
            'max_logs_count': app.config['MAX_LOGS_COUNT'],
            'max_log_life': app.config['MAX_LOG_LIFE_DAYS']}
        }

        context['title'] = 'Create new task'
        return context

    def post(self, *args, **kwargs):
        data = {}
        for i in request.form:
            data[i] = request.form.get(i)
        errors = {}
        have_errors = False
        for field in self.fields:
            if data.get(field, '') == '' or data.get(field, None) is None:
                errors[field] = 'This field is required'
                have_errors = True
        task = build_conf(data)
        if self.task.get('slug'):
            task.pop('pause', None)
            task.pop('slug', None)
            tmp_task = self.task.copy()
            tmp_task['edited'] = task.pop('created', None)
            tmp_task.update(task)
            task = tmp_task
        if task.get('slug') and not have_errors:
            path = os.path.join(app.config['TASKS_DIR'], task.get('slug'))
            tmp = os.path.join(app.config['TASKS_DIR'], slugify(task.get('name')))
            if (self.task.get('slug') or not os.path.exists(path)) and (self.task.get('slug') == slugify(task.get('name')) or not os.path.exists(tmp)):
                if not self.task.get('slug'):
                    os.makedirs(path)
                f = open(os.path.join(path, 'conf.json'), 'w')
                f.write(json.dumps(task))
                f.close()
                f = open(os.path.join(path, 'task.py'), 'w')
                f.write(data.get('code'))
                f.close()
            else:
                errors['name'] = 'Task with this name is already exists'
        if len(errors.keys()) > 0:
            return super().get(**{'errors': errors, 'data': data})
        return redirect(url_for('index'))


class TaskDetailView(AuthRequered, TaskRequeredMixin, TemplateView):
    template_name = 'task_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        dirpath = os.path.join(app.config['TASKS_DIR'], kwargs.get('slug', ''))
        logs_path = os.path.join(dirpath, 'logs')
        try:
            logs_names = list(os.walk(logs_path))[0][2]
        except IndexError:
            logs_names = []
        log_name = kwargs.get('log_name')
        logs_names.sort(reverse=True)
        logs = []
        curr_name = ''
        if logs_names:
            for name in logs_names:
                date = int(name.split('log')[1].split('.')[0])
                if int(self.task.get('last_run', 0)) - date > 0:
                    name = name.split('.')[0]
                    logs.append({"date": date, "name": name})
                    if name == log_name:
                        curr_name = name
            if not log_name:
                curr_name = logs[0].get('name')
            elif not curr_name:
                abort(404)
            f = open(os.path.join(logs_path, curr_name + '.txt'), 'r', encoding='utf-8')
            context['curr_log'] = f.readlines()
            context['curr_name'] = curr_name
            context['logs_count'] = len(logs_names)
            f.close()
        context['logs'] = logs
        return context


class LogoutView(View):

    def dispatch_request(self, *args, **kwargs):
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})


class TaskEditView(TaskRequeredMixin, CreateTaskView):

    def get_context_data(self, *args, **kwargs):
        context = {"data": self.task}
        f = open(os.path.join(app.config['TASKS_DIR'], self.task.get('slug', ''), 'task.py'), 'r')
        context["data"]["code"] = f.read()
        context.update(super().get_context_data(*args, **kwargs))
        f.close()
        context['title'] = 'Edit %s task' % self.task.get('name', '')
        return context


class TaskDeleteView(AuthRequered, TaskRequeredMixin, TemplateView):
    template_name = "delete.html"

    def post(self, *args, **kwargs):
        self.task['wait_for_delete'] = True
        f = open(os.path.join(app.config['TASKS_DIR'], self.task.get('slug', ''), 'conf.json'), 'w')
        f.write(json.dumps(self.task))
        f.close()
        return redirect(url_for('index'))


class ApiTask(AuthRequered, TaskRequeredMixin, ApiMixin):
    methods = ['GET', 'POST']

    def get(self, *args, **kwargs):
        return json.dumps(self.task), 200, {'ContentType': 'application/json'}

    def post(self, *args, **kwargs):
        data = json.loads(request.data.decode())
        if data.get('action') == 'build_now':
            self.task['build_now'] = True
            f = open(os.path.join(app.config['TASKS_DIR'], self.task.get('slug', ''), 'conf.json'), 'w')
            f.write(json.dumps(self.task))
            f.close()
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}


class ApiTasks(AuthRequered, ApiMixin):
    methods = ['GET']

    def get(self, *args, **kwargs):
        return json.dumps(get_tasks(with_run_status=True)), 200, {'ContentType': 'application/json'}

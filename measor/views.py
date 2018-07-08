import os
import json

from flask import request, Response, abort, redirect, url_for, current_app as app
from flask.views import View
from slugify import slugify

from measor.mixins import AuthRequered, TemplateView
from measor.utils import build_conf, get_tasks


class IndexView(AuthRequered, TemplateView):
    template_name = 'index.html'
    methods = ['GET']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tasks'] = get_tasks()
        return context


class CreateTaskView(AuthRequered, TemplateView):
    template_name = 'create.html'
    methods = ['GET', 'POST']
    fields = ('interval_units', 'interval', 'name', 'code')

    def get_context_data(*args, **kwargs):
        context = kwargs or {}
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
        name = data.get('name')
        if name and not have_errors:
            path = os.path.join(app.config['TASKS_DIR'], slugify(name))
            if not os.path.exists(path):
                os.makedirs(path)
                f = open(os.path.join(path, 'conf.json'), 'w')
                f.write(build_conf(data))
                f.close()
                f = open(os.path.join(path, 'task.py'), 'w')
                f.write(data.get('code'))
                f.close()
            else:
                errors['name'] = 'Task with this name is already exists'
        if len(errors.keys()) > 0:
            return super().get(**{'errors': errors, 'data': data})
        return redirect(url_for('index'))


class TaskDetailView(AuthRequered, TemplateView):
    template_name = 'task_detail.html'
    task = None

    def get_context_data(self, *args, **kwargs):
        context = {'task': self.task}
        dirpath = os.path.join(app.config['TASKS_DIR'], kwargs.get('slug', ''))
        logs_path = os.path.join(dirpath, 'logs')
        logs_names = list(os.walk(logs_path))[0][2]
        logs_names.sort(reverse=True)
        logs = []
        if logs_names:
            for name in logs_names:
                date = int(name.split('log')[1].split('.')[0])
                logs.append({"date": date, "name": name.split('.')[0]})
            f = open(os.path.join(logs_path, logs_names[0]), 'r')
            context['last_log'] = f.readlines()
            context['last_name'] = logs_names[0].split('.')[0]
            f.close()
        context['logs'] = logs
        return context

    def dispatch_request(self, *args, **kwargs):
        try:
            f = open(os.path.join(app.config['TASKS_DIR'], kwargs.get('slug', ''), 'conf.json'), 'r')
            self.task = json.loads(f.read())
        except FileNotFoundError:
            abort(404)
        return super().dispatch_request(*args, **kwargs)


class LogDetailView(AuthRequered, TemplateView):
    template_name = 'task_detail.html'


class LogoutView(View):

    def dispatch_request(self, *args, **kwargs):
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

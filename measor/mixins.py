import os
import json

from slugify import slugify
from flask import request, Response, render_template, abort, current_app as app
from flask.views import View

from measor.utils import check_auth, build_conf


class AuthRequered:

    def dispatch_request(self, *args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response(
                'Could not verify your access level for that URL.\n'
                'You have to login with proper credentials', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return super().dispatch_request(*args, **kwargs)


class TemplateView(View):
    methods = ['GET', 'POST']

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def get_template_name(self):
        return self.template_name

    def dispatch_request(self, *args, **kwargs):
        if request.method == 'POST':
            return self.post(*args, **kwargs)
        elif request.method == 'GET':
            return self.get(*args, **kwargs)
        return Response('Method is not allowed', 405, {})

    def get_context_data(self, *args, **kwargs):
        return {}

    def get(self, *args, **kwargs):
        return self.render_template(self.get_context_data(*args, **kwargs))

    def post(self, *args, **kwargs):
        return Response('Method is not allowed', 405, {})


class TaskRequeredMixin:
    task = {}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['task'] = self.task
        return context

    def dispatch_request(self, *args, **kwargs):
        try:
            f = open(os.path.join(app.config['TASKS_DIR'], kwargs.get('slug', ''), 'conf.json'), 'r')
            self.task = json.loads(f.read())
        except OSError:
            abort(404)
        return super().dispatch_request(*args, **kwargs)


class ApiMixin(View):
    methods = ['GET', 'POST']
    data = {}

    def dispatch_request(self, *args, **kwargs):
        try:
            if request.data:
                self.data = json.loads(request.data.decode())
        except Exception:
            pass
        if hasattr(self, request.method.lower()):
            handler = getattr(self, request.method.lower())
            resp = handler(*args, **kwargs)
            if not isinstance(resp, Response):
                return json.dumps(resp), 200, {'ContentType': 'application/json'}
            return resp
        return Response('Method is not allowed', 405, {})


class SaveTaskMixin:
    task = {}

    def save_task(self, *args, **kwargs):
        data = self.data
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
            return {'errors': errors, "status": False}
        return {'status': True}

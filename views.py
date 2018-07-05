import json

from flask import Flask, request, Response
from flask.views import View
from mixins import AuthRequered, TemplateView


class IndexView(AuthRequered, TemplateView):
    template_name = 'index.html'
    methods = ['GET']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class CreateTaskView(AuthRequered, TemplateView):
    template_name = 'create.html'
    methods = ['GET', 'POST']

    def post(self):
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


class LogoutView(View):

    def dispatch_request(self, *args, **kwargs):
        return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

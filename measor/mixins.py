from flask import request, Response, render_template
from flask.views import View


class AuthRequered:

    def check_auth(self, username, password):
        return username == 'admin' and password == 'secret'

    def dispatch_request(self, *args, **kwargs):
        auth = request.authorization
        if not auth or not self.check_auth(auth.username, auth.password):
            return Response(
                'Could not verify your access level for that URL.\n'
                'You have to login with proper credentials', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return super().dispatch_request(*args, **kwargs)


class TemplateView(View):

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

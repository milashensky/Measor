import sys
import os

from flask import Flask, send_from_directory

from views import IndexView, LogoutView, CreateTaskView

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
app = Flask(__name__)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/task', view_func=CreateTaskView.as_view('create_task'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))

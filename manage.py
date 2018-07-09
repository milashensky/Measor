#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from flask import Flask, send_from_directory

from measor.views import IndexView, LogoutView, CreateTaskView, TaskDetailView, TaskEditView, TaskDeleteView
from measor.filters import format_datetime, timestamp2date, decodeUnicode
from measor.docker import init_docker


def create_app():
    app = Flask(__name__)

    app.config.from_object('settings')
    sys.path.insert(0, os.path.join(app.config['BASE_DIR']))

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    # container = init_docker(app.config)
    # app.config['CONTAINER_ID'] = container.id

    app.add_url_rule('/', view_func=IndexView.as_view('index'))
    app.add_url_rule('/new_task', view_func=CreateTaskView.as_view('create_task'))
    app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
    app.add_url_rule('/task/<slug>', view_func=TaskDetailView.as_view('task_detail'))
    app.add_url_rule('/task/<slug>/edit', view_func=TaskEditView.as_view('edit_task'))
    app.add_url_rule('/task/<slug>/delete', view_func=TaskDeleteView.as_view('delete_task'))
    app.add_url_rule('/task/<slug>/<log_name>', view_func=TaskDetailView.as_view('log_detail'))

    app.jinja_env.filters['decodeUnicode'] = decodeUnicode
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['timestamp2date'] = timestamp2date
    return app


port = int(os.environ.get('PORT', 8000))
app = create_app()
app.run(port=port)

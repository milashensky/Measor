#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from flask import Flask, send_from_directory

from measor.views import IndexView, LogoutView, CreateTaskView
from measor.filters import format_datetime, timestamp2date


def create_app():
    app = Flask(__name__)

    app.config.from_object('settings')
    sys.path.insert(0, os.path.join(app.config['BASE_DIR']))

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    app.add_url_rule('/', view_func=IndexView.as_view('index'))
    app.add_url_rule('/new_task', view_func=CreateTaskView.as_view('create_task'))
    app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['timestamp2date'] = timestamp2date
    return app


port = int(os.environ.get('PORT', 8000))
app = create_app()
app.run(port=port)

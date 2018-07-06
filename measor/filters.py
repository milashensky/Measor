from flask import current_app as app
from datetime import datetime


def format_datetime(value, format='medium'):
    if format == 'full':
        format = "EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format = "EE dd.MM.y HH:mm"
    return value.strftime(format)


def timestamp2date(value, format=""):
    if not format:
        format = app.config.get('DATETIME_FORMAT') or '%Y-%m-%d %H:%M:%S'
    return datetime.fromtimestamp(int(value)).strftime(format)

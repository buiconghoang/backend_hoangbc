from filemonitor import app
from flask import render_template, jsonify, request
from filemonitor.database import session
from filemonitor.models import FilePathModel, WebhookUrl
import json
from datetime import datetime

@app.route('/register_web_hook')
def register_web_hook():
    try:
        args = request.args
        p = args['path']
        web_hook_url = args['web_hook_url']
        whu = WebhookUrl(web_hook_url)
        fp = FilePathModel(p)
        fp.add_webhook_url(whu)
        session.add_all([whu, fp])
        return {'status': 'success'}
    except Exception as err:
        print(err)
        return {'status': 'failed'}
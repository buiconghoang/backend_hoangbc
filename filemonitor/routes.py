from filemonitor import app, myobserver
from flask import render_template, jsonify, request
from filemonitor.database import session
from filemonitor.models import FilePathModel, WebhookUrl
import json
from datetime import datetime
import logging
import os

@app.route('/register_web_hook')
def register_web_hook():
    try:
        args = request.args
        p = args['path']
        if not os.path.exists(p):
            logging.error(f"register_web_hook path {p} not exists")
            return {'status': 'failed'}

        web_hook_url = args['web_hook_url']
        whu = get_webhook(web_hook_url)
        fp = get_filepath(p)
        fp.add_webhook(whu)
        session.add_all([fp])
        session.commit()
        myobserver.add_watched_file(fp.serialize())

        return {'status': 'success'}
    except Exception as err:
        logging.error("register_web_hook err:" + str(err))
        return {'status': 'failed'}
    finally:
        session.close()

@app.route('/get_file_paths')
def get_file_paths():
    try:
        file_paths = session.query(FilePathModel).all()
        rv = []
        for f in file_paths:
            rv.append(f.serialize())
        return jsonify(rv)
    except Exception as err:
        logging.error("get_file_paths err:" + str(err))
        return {'status': 'failed'}
    finally:
        session.close()
    
def get_filepath(p):
    fp = session.query(FilePathModel).filter(FilePathModel.path == p).first()
    if fp:
        return fp
    return FilePathModel(p)

def get_webhook(url):
    webhook = session.query(WebhookUrl).filter(WebhookUrl.url == url).first()
    if webhook:
        return webhook
    return WebhookUrl(url)

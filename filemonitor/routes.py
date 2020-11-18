from filemonitor import app, myobserver
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
        fp.add_webhook(whu)
        myobserver.add_watched_file(fp)
        session.add_all([fp])
        session.commit()
        return {'status': 'success'}
    except Exception as err:
        print(err)
        return {'status': 'failed'}
    finally:
        print('zz')
        session.close()

@app.route('/get_file_paths')
def get_file_paths():
    try:
        file_paths = session.query(FilePathModel).all()
        rv = []
        for f in file_paths:
            print(f)
            rv.append(f.serialize())
        return jsonify(rv)
    except Exception as err:
        print(err)
        return {'status': 'failed'}
    finally:
        print('1')
        session.close()
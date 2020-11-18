from filemanagement import app
from flask import jsonify, request
from filemanagement.database import session
from filemanagement.models import FileInfoModel
import json
from datetime import datetime


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get_file_info')
def get_file_info():
    try:
        p = request.args['path']
        file_info = session.query(FileInfoModel).filter_by(id=p).all()
        if len(file_info) == 0:
            return {}
        return jsonify(file_info[0].serialize())
    except Exception as e:
        print(e)
        return {'status': 'failed'}
    finally:
        session.close()

@app.route('/update_file_info', methods=['POST'])
def update_file_info():
    try:
        data = json.loads(request.data)
        data['date_created'] = datetime.fromtimestamp(float(data['date_created']))
        data['date_updated'] = datetime.fromtimestamp(float(data['date_updated']))

        fileinfo_model = FileInfoModel(
            data['path'], data['size'], data['hash'],
            data['date_created'], data['date_updated'])
        
        session.add(fileinfo_model)
        session.commit()
        return f'id: {fileinfo_model.id}'
    except Exception as err:
        print(err)
        return {'status': 'failed'}
    finally:
        session.close()
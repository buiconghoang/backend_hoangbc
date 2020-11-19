from filemanagement import app
from flask import jsonify, request
from filemanagement.database import session
from filemanagement.models import FileInfoModel
import json
from datetime import datetime
from filemanagement.constant import EventType
import logging


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/get_file_info')
def get_file_info():
    try:
        p = request.args['path']
        file_info = session.query(FileInfoModel).filter_by(path=p).all()
        if len(file_info) == 0:
            return {}
        return jsonify(file_info[0].serialize())
    except Exception as e:
        logging.error(f'get_file_info err: {str(e)}')
        return {'status': 'failed'}
    finally:
        session.close()


@app.route('/get_file_infos')
def get_file_infos():
    try:
        file_infos = session.query(FileInfoModel).all()
        if len(file_infos) == 0:
            return {}
        rv = []
        for file_info in file_infos:
            rv.append(file_info.serialize())

        return jsonify(rv)
    except Exception as e:
        logging.error(f'get_file_info err: {str(e)}')
        return {'status': 'failed'}
    finally:
        session.close()


@app.route('/update_file_info', methods=['POST'])
def update_file_info():
    try:
        logging.info("update_file_info")
        data = json.loads(request.data)
        event_type = data.get('eventtype', 'created')
        dest_path = data.get('dest_path', '')
        src_path = data.get('path', '')
        size = data.get('size', 0)
        date_created = datetime.fromtimestamp(float(data.get('date_updated', 0)))
        date_updated = datetime.fromtimestamp(float(data.get('date_updated', 0)))


        logging.info(f'--->update_file_info event type : {event_type}')
        fileinfo_model = FileInfoModel(src_path, data['size'], data['hash'], date_created, date_updated)

        if event_type == EventType.CREATED:
            logging.info(f'--->update_file_info: id: {fileinfo_model.id}')
            session.add(fileinfo_model)
        elif event_type == EventType.MODIFIED or event_type == EventType.MOVED:
            if dest_path:
                fileinfo_model.path = dest_path

            session.query(FileInfoModel).filter(FileInfoModel.path == src_path).\
                update(fileinfo_model.make_update_obj(), synchronize_session=False)
        elif event_type == EventType.DELETED:
            session.query(FileInfoModel).filter(FileInfoModel.path == src_path).\
                delete(synchronize_session=False)
        session.commit()
        return f'id: {fileinfo_model.id}'
    except Exception as err:
        print(str(err))
        logging.error('update_file_info err: ' + str(err))
        return {'status': 'failed'}
    finally:
        session.close()

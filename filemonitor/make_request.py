import os
from filemonitor.utils import make_hash
import request
import json

def create_body(src_path, dest_path, event_name):
    stat = os.stat(src_path)

    body = {}
    body['path'] = src_path
    body['date_modified'] = stat.st_mtime
    body['date_created'] = stat.st_ctime
    body['size'] = stat.st_size
    body['hash'] = make_hash(file_path, stat.st_size, stat.st_mtime)
    body['event'] = event_name
    return body

def send_request(url, src_path, ):
    data = 
    request.post("http://127.0.0.1:8080/update_file_info", json.du)

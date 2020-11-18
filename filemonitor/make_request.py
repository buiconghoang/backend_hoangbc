import os
from filemonitor.utils import make_hash
import requests
import json

def create_body(src_path, event_type, dest_path=''):
    body = {}
    if dest_path:
        stat = os.stat(dest_path)
        body['hash'] = make_hash(dest_path, stat.st_size, stat.st_mtime)
    else:
        stat = os.stat(src_path)
        body['hash'] = make_hash(src_path, stat.st_size, stat.st_mtime)

    body['path'] = src_path
    body['date_updated'] = stat.st_mtime
    body['date_created'] = stat.st_ctime
    body['size'] = stat.st_size
    body['eventtype'] = event_type
    body['dest_path'] = dest_path
    return body

def send_request(url, src_path, event_name, dest_path=''):
    data = create_body(src_path, event_name, dest_path)
    print("data: ",data)
    requests.post(url, json.dumps(data))

    

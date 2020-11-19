import sys
import time
import os
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, RegexMatchingEventHandler
from filemonitor.models import FilePathModel, WebhookUrl
from filemonitor.make_request import send_request
from filemonitor.database import session
from filemonitor.constant import EventType

class EventHandler(FileSystemEventHandler):

    def __init__(self, observer):
        super().__init__()
        self.my_observer = observer

    def on_any_event(self, event):
        self.my_observer.notify(event)

class MyObserver():

    __instance = None
   
    @staticmethod
    def getInstance():
        if MyObserver.__instance == None:
            MyObserver()
        return MyObserver.__instance

    def __init__(self):
        if MyObserver.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MyObserver.__instance = self
            self.observer = Observer()
            self.event_handler = EventHandler(self)
            self.filepath_objs = {}
    
    def init_watched_file(self):
        results = session.query(FilePathModel).all()
        for filepath_model in results:
            self.add_watched_file(filepath_model.serialize())

    def add_watched_file(self, filepath_model):
        p = os.path.abspath(filepath_model['path'])
        self.filepath_objs[p] = filepath_model

        if os.path.isdir(p):
            self.observer.schedule(self.event_handler, p, recursive=True)

        if os.path.isfile(filepath_model['path']):
            p = os.path.dirname(p)
            self.observer.schedule(self.event_handler, p, recursive=True)


    def notify(self, filesystem_event):
        src_path = os.path.abspath(filesystem_event.src_path)
        event_type = filesystem_event.event_type
        dest_path = ''

        if os.path.isdir(src_path):
            return

        logging.info(f"notify filesystem event: {filesystem_event}")

        is_send_request = False
        webhook_urls = []
        if event_type == EventType.moved:
            dest_path = os.path.abspath(filesystem_event.dest_path)
        
        for filepath, filepath_obj in self.filepath_objs.items():
            if src_path.startswith(filepath):
                is_send_request = True
                webhook_urls = [webhook['url'] for webhook in filepath_obj['webhook']]
                break

        if not is_send_request and src_path in self.filepath_objs:
            is_send_request = True
            webhook_urls = [webhook['url'] for webhook in self.filepath_objs[src_path]['webhook']]
        
        if is_send_request:
            for webhook_url in webhook_urls:
                send_request(webhook_url, src_path, event_type, dest_path)

    def start(self):
        self.observer.start()
    
    def stop(self):
        self.observer.stop()


# if __name__ == '__main__':

#     class CustomFilePathModel(object):
#         def __init__(self, path):
#             self.path = path
#         def get_wehook_urls(self):
#             return ['http://127.0.0.1:8080/update_file_info']
    

#     cfpm = CustomFilePathModel(r'D:\\zttt\\i.txt')
#     myobserver = MyObserver.getInstance()
#     myobserver.add_watched_file(cfpm)

#     myobserver.start()
#     i= 0
#     try:
#         while True:
#             if i%10 == 0:
#                 print(i)
#             i += 1
#             if i == 20:
#                 print('start watch "D:\\z2"')
#                 cfpm = CustomFilePathModel(r'D:\\z2')
#                 myobserver.add_watched_file(cfpm)
#             time.sleep(1)
#     except Exception as e:
#         print(e)
#         myobserver.stop()
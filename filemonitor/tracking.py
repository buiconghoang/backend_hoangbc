import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, RegexMatchingEventHandler
# from filemonitor.models import FilePathModel, WebhookUrl
import time
import os

class EventHandler(FileSystemEventHandler):

    def __init__(self, observer):
        super().__init__()
        self.my_observer = observer

    def on_any_event(self, event):
        self.my_observer.notify(event)
        # print("EVENT")
        # print(event)
        # print(event.event_type)
        # print(event.src_path)
        # print()

class EventType:
    x = 100

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
            self.filepath_model = {}
    
    def add_watched_file(self, filepath_model):
        self.filepath_model[filepath_model['path']] = filepath_model
        if os.path.isdir(filepath_model['path']):
            self.observer.schedule(self.event_handler, filepath_model['path'], recursive=True)
        if os.path.isfile(filepath_model['path']):
            p = os.path.dirname(filepath_model['path'])
            self.observer.schedule(self.event_handler, p, recursive=True)


    def notify(self, filesystem_event):
        print('notify')
        
        print(filesystem_event)

    def start(self):
        self.observer.start()
    
    def stop(self):
        self.observer.stop()



if __name__ == '__main__':
    path = {'path': r'D:\\zttt\\i.txt'}
    # paths = [r'D:\\zttt\\i.txt']
    myobserver = MyObserver.getInstance()
    myobserver.add_watched_file(path)

    myobserver.start()
    i= 0
    try:
        while True:

            if i%10 == 0:
                print(i)
            i += 1
            if i == 20:
                print('start watch "D:\\z2"')
                myobserver.add_watched_file({'path': r"D:\\z2"})
            if i == 40:
                myobserver.stop()
                break
            time.sleep(1)
    except Exception as e:
        print(e)
        myobserver.stop()


# if __name__ == "__main__":
#     # path = sys.argv[1] if len(sys.argv) > 1 else '.'
#     # paths = [r"D:\zttt\abc\123.txt", r"D:\zttt\X.txt", r"D:\zttt\i.txt"]
#     paths = [r'D:\zttt']
#     # paths = [r'D:\\zttt\\i.txt']
#     event_handler = EventHandler()
#     observer = Observer()
#     observers = []
#     for path in paths:
#         observer.schedule(event_handler, path, recursive=False)
#         observers.append(observer)
#     observer.start()
#     i= 0
#     try:
#         while True:
#             if i%10 == 0:
#                 print(i)
#             i += 1
#             if i == 20:
#                 print('start watch "D:\\z2"')
#                 observer.schedule(event_handler, "D:\\z2", recursive=True)
#             if i == 30:
#                 observer.stop()
#                 break
#             time.sleep(1)
#     except Exception as e:
#         print(e)
#         observer.stop()
#     # observer.join()
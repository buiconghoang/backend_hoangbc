from flask import Flask
from filemonitor.tracking import MyObserver
from filemonitor.database import init_db, session

app = Flask(__name__)
init_db()
myobserver = MyObserver.getInstance()
myobserver.init_watched_file(session)
from filemonitor import routes

myobserver.start()
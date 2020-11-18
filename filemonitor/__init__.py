import logging
from flask import Flask
from filemonitor.tracking import MyObserver
from filemonitor.database import init_db, session
from filemonitor.config import config

logging.basicConfig(format=config.log_format, filename=config.log_path, level=logging.INFO)

app = Flask(__name__)
init_db()
myobserver = MyObserver.getInstance()
myobserver.init_watched_file()
from filemonitor import routes

myobserver.start()
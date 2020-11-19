import logging
from flask import Flask
from filemonitor.database import init_db
from filemonitor.config import config

logging.basicConfig(format=config.log_format, filename=config.log_path, level=logging.INFO)

app = Flask(__name__)
init_db()
from filemonitor.tracking import MyObserver
myobserver = MyObserver.getInstance()
myobserver.init_watched_file()
from filemonitor import routes

myobserver.start()
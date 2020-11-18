import logging
from flask import Flask
from filemanagement.database import init_db
from filemanagement.config import config

logging.basicConfig(format=config.log_format, filename=config.log_path, level=logging.INFO)

app = Flask(__name__)

init_db()

from filemanagement import routes

from flask import Flask
from filemanagement.database import init_db

app = Flask(__name__)

init_db()

from filemanagement import routes

from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from filemanagement.config import configdb
import os

if configdb.db_path:
    db_path = configdb.db_path
else:
    try:
        db_path = os.path.join(os.path.dirname(__file__), configdb.db_name)
    except Exception as e:
        db_path = os.path.join(os.getcwd(), configdb.db_name)

SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.abspath(db_path)
engine = create_engine(SQLALCHEMY_DATABASE_URI,  echo = True)
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()

def init_db():
    import filemanagement.models
    table_names = inspect(engine).get_table_names()
    for table_name in configdb.table_names.values():
        if table_name not in table_names: 
            Base.metadata.create_all(engine)
            break

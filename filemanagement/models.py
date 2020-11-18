from sqlalchemy import Column, Integer, String, Float, DateTime, inspect
from filemanagement.database import Base
from filemanagement.config  import configdb
from datetime import datetime

class FileInfoModel(Base):
    __tablename__ = configdb.table_names['fileinfo']
    id = Column(Integer, primary_key=True)
    path = Column(String, index=True)
    size = Column(Float)
    hash_file = Column(String)
    date_created = Column(DateTime)
    date_updated = Column(DateTime)

    def __init__(self, path, size, hash_file, date_created, date_updated):
        self.path = path
        self.hash_file = hash_file
        self.size = size
        self.date_created = date_created
        self.date_updated = date_updated

    def __repr__(self):
        return f"<FileInfor(id={self.id},path={self.path}, size={self.size},\
             date_created={self.date_created}, date_updated={self.date_updated})>"

    def serialize(self):
        obj = {}
        for c in inspect(self).attrs.keys():
            if c == 'id':
                continue
            val = getattr(self, c)
            if isinstance(val, datetime):
                val = str(val)
            obj[c] = val
        return obj

    def make_update_obj(self):
        obj = {}
        obj['path'] = self.path
        obj['size'] = self.size
        obj['date_created'] = self.date_created
        obj['date_updated'] = self.date_updated
        return obj

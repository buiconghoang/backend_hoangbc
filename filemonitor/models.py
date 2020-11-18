from sqlalchemy import Column, Integer, String, Float, DateTime, inspect, Table, ForeignKey
from sqlalchemy.orm import relationship
from filemonitor.database import Base
from filemonitor.config  import configdb

filepath_webhookurl = Table(configdb.table_names['filepath_webhook'], Base.metadata,
    Column('filepath_id', ForeignKey(f'{configdb.table_names["filepath"]}.id'), primary_key=True),
    Column('webhook_id', ForeignKey(f'{configdb.table_names["webhook"]}.id'), primary_key=True)
)

class FilePathModel(Base):
    __tablename__ = configdb.table_names['filepath']
    id = Column(Integer, primary_key=True)
    path = Column(String, index=True)
    webhook = relationship('WebhookUrl', secondary=filepath_webhook,
                            back_populates='filepaths')

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f"<FilePathModel(id={self.id},path={self.path})>"
    
    def add_webhook(self, wh_obj):
        self.webhook.append(wh_obj)

    def get_wehook_urls(self):
        urls = []
        for wh in self.webhook:
            urls.append(wh.url)
        return urls


    def serialize(self):
        obj = {}
        for c in inspect(self).attrs.keys():
            if c == 'id':
                continue
            val = getattr(self, c)
            if c == 'webhook':
                webhook = []
                for webhook in val:
                    webhook.append(webhook.serialize())
                val = webhook
            obj[c] = val
        return obj

class WebhookUrl(Base):
    __tablename__ = configdb.table_names['webhook']
    id = Column(Integer, primary_key=True)
    url = Column(String, index=True)

    filepaths = relationship('FilePathModel', secondary=filepath_webhook,
                            back_populates='webhook')

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return f"<Webhook(id={self.id},url={self.url})>"

    def serialize(self):
        obj = {}
        for c in inspect(self).attrs.keys():
            if c == 'id' or c == 'filepaths':
                continue
            val = getattr(self, c)
            obj[c] = val
        return obj
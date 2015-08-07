from datetime import datetime, date
import time

from sqlalchemy import Sequence, Column, ForeignKey

# column types
from sqlalchemy import Integer, String, Unicode
from sqlalchemy import Boolean, Date, LargeBinary
from sqlalchemy import PickleType
from sqlalchemy import Enum
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SerialBase(object):
    def serialize(self):
        data = dict()
        table = self.__table__
        for column in table.columns:
            name = column.name
            try:
                pytype = column.type.python_type
            except NotImplementedError:
                print "NOTIMPLEMENTEDERROR", column.type
            value = getattr(self, name)
            if pytype is datetime or pytype is date:
                if value is not None:
                    value = value.isoformat()
            data[name] = value
        return data
    

####################################
## Data Types                     ##
####################################

FileType = Enum('agenda', 'minutes', 'attachment',
                name='file_type_enum')

####################################
## Tables                         ##
####################################

class Repository(Base,SerialBase):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True)
    uuid = Column(Unicode(35), unique=True)

class FilePath(Base, SerialBase):
    __tablename__ = 'filepaths'
    id = Column(Unicode, primary_key=True)

class WhereIs(Base, SerialBase):
    __tablename__ = 'whereis'
    path = Column(Unicode, ForeignKey('filepaths.id'),
                  primary_key=True)
    repo = Column(Integer, ForeignKey('repositories.id'),
                  primary_key=True)
    
                      

class MainCache(Base, SerialBase):
    __tablename__ = 'main_cache'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True)
    retrieved = Column(DateTime)
    updated = Column(DateTime)
    content = Column(PickleType)


####################################
## Relationships                  ##
####################################


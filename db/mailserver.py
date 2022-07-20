from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from db import db_connect

Base = declarative_base()



class Mailserver:
  def __init__(self) -> None:
    self.__name__ = "mailserver"
    self.engine = create_engine(db_connect.mailserver)

  def connect(self):
    return self.engine.connect()

  def test_connection(self) -> bool:
    try:
      with self.connect() as c:
        is_connected = True
    except:
      is_connected = False
    return is_connected

  def query(self, sql):
    with self.connect() as c:
      results = c.execute(sql)
    
    return [ str(row) for row in results ]
    


class Virtual_aliases(Base):
  __tablename__ = "virtual_aliases"

  id = Column(Integer, primary_key=True)
  domain_id = Column(Integer, ForeignKey('virtual_domains.id'))
  source = Column(String)
  destination = Column(String)
  
  virtual_domains = relationship(
      "Virtual_domains", back_populates="virtual_aliases", cascade="all, delete-orphan"
  )


class Virtual_domains(Base):
  __tablename__ = "virtual_domains"

  id = Column(Integer, primary_key=True)
  name = Column(String)
  
  virtual_aliases = relationship(
      "Virtual_aliases", back_populates="virtual_domains", cascade="all, delete-orphan"
  )
  
  virtual_users = relationship(
      "Virtual_users", back_populates="virtual_domains", cascade="all, delete-orphan"
  )


class Virtual_users(Base):
  __tablename__ = "virtual_users"

  id = Column(Integer, primary_key=True)
  domain_id = Column(Integer)
  password = Column(String)
  email = Column(String)
  
  virtual_domains = relationship(
      "Virtual_domains", back_populates="virtual_users", cascade="all, delete-orphan"
  )
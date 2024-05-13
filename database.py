from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

# helper methods

Base = declarative_base()
def opendb():
    engine = create_engine('sqlite:///sensors.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def get(table, id):
    session = opendb()
    result = session.query(table).filter_by(id=id).first()
    session.close()
    return result

def get_all(table):
    session = opendb()
    result = session.query(table).all()
    session.close()
    return result

def add(data):
    session = opendb()
    session.add(data)
    session.commit()
    session.close()

# classes
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    def __str__(self):
        return f'{self.name}'
    
class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String, default='')
    tempf = Column(Float)
    temp = Column(Float)
    humidity = Column(Float) 
    created_on = Column(DateTime, default=datetime.now)
    def __str__(self):
        return f'{self.name}'
    

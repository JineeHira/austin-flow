import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Date
from geoalchemy2 import Geometry


class Connection(object):

    def __init__(self, db_connection):
        engine = create_engine(db_connection)
        self.engine = engine

    def get_session(self):
        Session = sessionmaker(bind=self.engine)

        return Session()

    def get_engine(self):
        return self.engine


Base = declarative_base()


def init_db(db_connection):
    engine = create_engine(db_connection)
    Base.metadata.create_all(bind=engine)

class Traffic(Base):
    __tablename__ = 'traffic_report'
    
    timestamp = Column(Integer, primary_key=True)
    traffic_report_id = Column(String)
    date_time = Column(DateTime)
    issue_reported = Column(String)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String)
    weekday = Column(String)
    date = Column(DateTime)
    time = Column(DateTime)

    def __init__(self, timestamp, traffic_report_id, date_time, issue_reported, location, latitude, longitude, address, weekday, date, time):
        self.timestamp = timestamp
        self.traffic_report_id = traffic_report_id
        self.date_time = date_time
        self.issue_reported = issue_reported
        self.location = f'POINT({longitude} {latitude})'
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.weekday = weekday
        self.date = date
        self.time = time
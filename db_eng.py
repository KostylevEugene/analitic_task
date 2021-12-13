from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base     
from sqlalchemy.orm import sessionmaker, scoped_session

''' Данный файл необходим для создания БД, подключения и взаимодействия с ней '''


engine = create_engine('sqlite:///db.db', echo=True)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

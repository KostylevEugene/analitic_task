from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base     # (?) для определения (или помощи создания) таблиц и моделей
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///db.db', echo=True)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
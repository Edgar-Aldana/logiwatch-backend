from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = "{}://{}:{}@{}:{}/{}?client_encoding=utf8".format(
    getenv("DATABASE_DRIVER"),
    getenv("DATABASE_USER"),
    getenv("DATABASE_PASSWORD"),
    getenv("DATABASE_HOST"),
    getenv("DATABASE_PORT"),
    getenv("DATABASE_NAME")
)


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={}, echo=False, client_encoding='utf-8')

Session = sessionmaker(expire_on_commit=False, autocommit=False, autoflush=False)
Session.configure(bind=engine)
session = Session()

Base = declarative_base()

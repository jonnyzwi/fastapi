
import fastapi
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings, uri#, DATABASE_URL


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/database_name>'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi_DB'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

SQLALCHEMY_DATABASE_URL = 'postgres://ammbnnbiydgmxn:865288d3aa6f5daeb0c6defb4d94036f344bd41ce0bf8dee8b035dff79b70281@ec2-54-144-165-97.compute-1.amazonaws.com:5432/d74soohkq8rpbl'
SQLALCHEMY_DATABASE_URL = 'postgres://ammbnnbiydgmxn:865288d3aa6f5daeb0c6defb4d94036f344bd41ce0bf8dee8b035dff79b70281@ec2-54-144-165-97.compute-1.amazonaws.com:5432/d74soohkq8rpbl?sslmode=require'
# SQLALCHEMY_DATABASE_URL='(heroku config:get DATABASE_URL -a fastapi-zwitrader)'
# SQLALCHEMY_DATABASE_URL = 'postgres://ammbnnbiydgmxn:865288d3aa6f5daeb0c6defb4d94036f344bd41ce0bf8dee8b035dff79b70281@ec2-54-144-165-97.compute-1.amazonaws.com:5432/d74soohkq8rpbl?ssl=true&sslfactory=org.postgresql.ssl.NonValidatingFactory'

# SQLALCHEMY_DATABASE_URL = DATABASE_URL


SQLALCHEMY_DATABASE_URL = uri 

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


print('KLASDLKASLKJASJLDS&*&&*#*&&$*JSHAJKHDAJSKHDKJ')


# print(f'''
#     {SQLALCHEMY_DATABASE_URL}
#         database_hostname:           {settings.database_hostname}
#         database_port:               {settings.database_port}
#         database_password:           {settings.database_password}
#         database_name:               {settings.database_name}
#         database_username:           {settings.database_username}
#         secret_key:                  {settings.secret_key}
#         algorithm:                   {settings.algorithm}
#         access_token_expire_minutes: {settings.access_token_expire_minutes}
#     ''')

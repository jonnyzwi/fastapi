
import fastapi
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings #uri#, DATABASE_URL



######################
import os
import re
try:
    uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    # rest of connection code using the connection string `uri`
except:
    pass
######################



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# app.config["SQLALCHEMY_DATABASE_URI"]= f'postgresql://{db_user}:{db_pswd}@{db_host}/{db_name}'
# HEROKU_URL = f'postgresql://{db_user}:{db_pswd}@{db_host}/{db_name}'

HEROKU_URL = 'postgresql://ammbnnbiydgmxn:865288d3aa6f5daeb0c6defb4d94036f344bd41ce0bf8dee8b035dff79b70281@ec2-54-144-165-97.compute-1.amazonaws.com:5432/d74soohkq8rpbl'


# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/database_name>'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi_DB'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'


HEROKU_DATABASE_URL = 'postgres://ammbnnbiydgmxn:865288d3aa6f5daeb0c6defb4d94036f344bd41ce0bf8dee8b035dff79b70281@ec2-54-144-165-97.compute-1.amazonaws.com:5432/d74soohkq8rpbl'
# HEROKU_DATABASE_URL = 'postgresql://ammbnnbiydgmxn:865288d3aa6f5daeb0c6defb4d94036f344bd41ce0bf8dee8b035dff79b70281@ec2-54-144-165-97.compute-1.amazonaws.com:5432/d74soohkq8rpbl?sslmode=require'

# HEROKU_DATABASE_URL='(heroku config:get DATABASE_URL -a fastapi-zwitrader)'
# HEROKU_DATABASE_URL =  'postgres://ammbnnbiydgmxn:865288d3aa6f5daeb0c6defb4d94036f344bd41ce0bf8dee8b035dff79b70281@ec2-54-144-165-97.compute-1.amazonaws.com:5432/d74soohkq8rpbl?ssl=true&sslfactory=org.postgresql.ssl.NonValidatingFactory'
# HEROKU_DATABASE_URL =  'postgresql://ammbnnbiydgmxn:865288d3aa6f5daeb0c6defb4d94036f344bd41ce0bf8dee8b035dff79b70281@ec2-54-144-165-97.compute-1.amazonaws.com:5432/d74soohkq8rpbl?ssl=true&sslfactory=org.postgresql.ssl.NonValidatingFactory'

# HEROKU_DATABASE_URL = DATABASE_URL
# HEROKU_DATABASE_URL = uri 

SQLALCHEMY_DATABASE_URL = HEROKU_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


print('KLASDLKASLKJASJLDS&*&&*#*&&$*JSHAJKHDAJSKHDKJ')


full_credentials = f'''
    SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}

        database_hostname:           {settings.database_hostname}
        database_port:               {settings.database_port}
        database_password:           {settings.database_password}
        database_name:               {settings.database_name}
        database_username:           {settings.database_username}
        secret_key:                  {settings.secret_key}
        algorithm:                   {settings.algorithm}
        access_token_expire_minutes: {settings.access_token_expire_minutes}
    '''

print(full_credentials)
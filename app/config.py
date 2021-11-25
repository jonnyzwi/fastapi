from pydantic import BaseSettings

# validating environment variables (varaible as not case sensitive)
class Settings(BaseSettings):
        # database_password:str = 'localhost'
        # database_username:str = 'postgres'
        # secret_key: str = ''

        database_hostname           :str
        database_port               :str
        database_password           :str
        database_name               :str
        database_username           :str
        secret_key                  :str
        algorithm                   :str
        access_token_expire_minutes :int

        class Config:
            # env_file = "/Users/jzwi/pythonProjects/FreeCodeCamp_API/.env"
            env_file = ".env"

settings = Settings()


HEROKU_DBNAME='d74soohkq8rpbl'
HEROKU_HOST='ec2-54-144-165-97.compute-1.amazonaws.com'
HEROKU_PORT=5432
HEROKU_USER='ammbnnbiydgmxn'
HEROKU_PWD='865288d3aa6f5daeb0c6defb4d94036f344bd41ce0bf8dee8b035dff79b70281'
HEROKU_SSL_MODE='require'

HEROKU_URL = 'postgresql://ammbnnbiydgmxn:865288d3aa6f5daeb0c6defb4d94036f344bd41ce0bf8dee8b035dff79b70281@ec2-54-144-165-97.compute-1.amazonaws.com:5432/d74soohkq8rpbl'


'''
heroku pg:credentials:url -a fastapi-zwitrader

Connection info string:
   "dbname=d74soohkq8rpbl host=ec2-54-144-165-97.compute-1.amazonaws.com port=5432 user=ammbnnbiydgmxn password=865288d3aa6f5daeb0c6defb4d94036f344bd41ce0bf8dee8b035dff79b70281 sslmode=require"

Connection URL:
   postgres://ammbnnbiydgmxn:865288d3aa6f5daeb0c6defb4d94036f344bd41ce0bf8dee8b035dff79b70281@ec2-54-144-165-97.compute-1.amazonaws.com:5432/d74soohkq8rpbl
'''
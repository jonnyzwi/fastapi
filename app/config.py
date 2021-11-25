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



import os
import re

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`
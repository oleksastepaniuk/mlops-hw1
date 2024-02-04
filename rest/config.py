import os

class Config:
    POSTGRES_DB_URL = os.environ.get('POSTGRES_DB_URL')
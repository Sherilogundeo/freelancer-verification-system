import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///db.sqlite3')

class DevelopmentConfig(Config):
    DEBUG = True
    BASE_URL = os.getenv('DEV_BASE_URL')

class ProductionConfig(Config):
    DEBUG = False
    BASE_URL = os.getenv('BASE_URL')

def get_env(var_name):
    try:
        return os.getenv(var_name)
    except KeyError:
        raise KeyError("Set the {} environment variable".format(var_name))
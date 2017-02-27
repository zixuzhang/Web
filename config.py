import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'eL7fnDZRL6kEbeAI'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    MONGODB_DB = 'zxjd'
    DEBUG = True

class TestingConfig(Config):
    TESTING =True

class ProductionConfig(Config):
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    MONGODB_DB = 'zxjd_database'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
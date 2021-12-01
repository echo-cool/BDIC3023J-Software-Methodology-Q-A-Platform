import os

basedir = os.path.abspath(os.path.dirname(__file__))


# basic configuration

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ec94cr32ffs2123ffd3fg3dsa2r39cfc6d796ae3029594d'

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = '609899054@qq.com'
    MAIL_PASSWORD = 'hnktohctbgwhbchh'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Student Exchange Forum of BJUT]'
    FLASKY_MAIL_SENDER = '609899054@qq.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_LIKER_PER_PAGE = 50
    CACHE_TYPE = os.environ.get('CACHE_TYPE') or "simple"
    REDIS_URL = os.environ.get('REDIS_URL') or ""
    REDIS_USERNAME = os.environ.get('REDIS_USERNAME') or ""
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD') or ""

    @staticmethod
    def init_app(app):
        pass


# define some  specific  configuration
# you can choose a suit one

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

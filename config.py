import os

basedir = os.path.abspath(os.path.dirname(__file__))



class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'ou_xiao_ou@163.com'
    MAIL_PASSWORD = 'BJXWOHPBIPNUYHRW'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Student Exchange Forum of BJUT]'
    FLASKY_MAIL_SENDER = 'ou_xiao_ou@163.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_LIKER_PER_PAGE = 50

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

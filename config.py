import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgres:///apartment_ranker"


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "testing secret key"
    SQLALCHEMY_DATABASE_URI = "postgres:///apartment_ranker_test"

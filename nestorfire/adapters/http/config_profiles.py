import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):

    REDIS_URL = "redis://redis:6379/0"
    QUEUES = ["default"]


class DevConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    TESTING = True

class ProductionConfig(BaseConfig):
    pass



class DevConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:Bunuhat1rla@localhost/library_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    DEBUG = True

class ProdConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://user:pass@prod-db/prod"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

config = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": ProdConfig
}

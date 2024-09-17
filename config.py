import os


class Config:
    HOST = os.getenv("DB_HOST")
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASS")
    DATABASE = os.getenv("DB_NAME")
    PI_SERVER = os.getenv("PI_SERVER_ENDPOINT")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

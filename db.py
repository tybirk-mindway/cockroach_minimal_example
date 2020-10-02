from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

USE_SQLITE = True
connect_args = {}

if USE_SQLITE:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./data/test_database.db"
    connect_args["check_same_thread"] = True
else:
    SQLALCHEMY_DATABASE_URL = os.environ["DB_FULL_PATH"]
    # Hack to get certificate file into docker from .env file. Possibly not the ideal approach!
    with open("./db.crt", "w") as f:
        f.write(os.environ["DB_CERTIFICATE"])

    connect_args = {"sslmode": "verify-full", "sslrootcert": "./db.crt"}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args, echo=True)
SessionLocal = sessionmaker(bind=engine)  # autocommit=False, autoflush=False,

Base = declarative_base()

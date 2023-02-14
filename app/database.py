from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings
import cloudinary 


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------- Cloudinery Config --------------------------- #
# Config
cloudinary.config(
  cloud_name = settings.cd_cloud_name,
  api_key = settings.cd_api_key,
  api_secret = settings.cd_api_secret,
#   secure = true
)



# while True:
#     try:
#         connect = psycopg2.connect(
#             host='localhost', database='fastapi', user='postgres', password='admin', cursor_factory=RealDictCursor,)
#         curser = connect.cursor()
#         print("Database Connection successfull !!")
#         break
#     except Exception as error:
#         print("Database Connection Failed")
#         print("Error: ", error)
#         time.sleep(5)
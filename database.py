from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url="postgresql://postgres:Akshit%4022@localhost:5432/akshit"
engine= create_engine(db_url)
session= sessionmaker(autocommit=False, autoflush=False, bind=engine)
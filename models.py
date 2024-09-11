from sqlalchemy import Column, String, Integer,Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "postgresql://postgres:postgres@db:5432/account_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    no_rekening = Column(String, unique=True, index=True)
    nama = Column(String, index=True)
    nik = Column(String, unique=True, index=True)
    no_hp = Column(String, unique=True, index=True)
    saldo = Column(Float, default=0.0)
    
    activities = relationship("Activity", back_populates="customer")
    
class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    no_rekening = Column(String, ForeignKey("customers.no_rekening"), index=True)
    tipe = Column(String, index=True)
    nominal = Column(Float)
    saldo_setelah = Column(Float)

    customer = relationship("Customer", back_populates="activities")
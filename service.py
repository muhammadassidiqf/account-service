from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import Customer, Activity, SessionLocal
import uuid


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def daftar(db: Session, nama: str, nik: str, no_hp: str) -> str:
    if db.query(Customer).filter(Customer.nik == nik).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"remark": "NIK sudah digunakan."}
        )
    if db.query(Customer).filter(Customer.no_hp == no_hp).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"remark": "No HP sudah digunakan."}
        )

    no_rekening = str(uuid.uuid4().int)[:10]
    new_customer = Customer(no_rekening=no_rekening, nama=nama, nik=nik, no_hp=no_hp)

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer.no_rekening


def tabung(db: Session, no_rekening: str, tipe: str, nominal: float) -> float:
    customer = db.query(Customer).filter(Customer.no_rekening == no_rekening).first()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"remark": "No Rekening Tidak ditemukan."}
        )

    customer.saldo += nominal

    activity = Activity(
        no_rekening=no_rekening,
        tipe=tipe,
        nominal=nominal,
        saldo_setelah=customer.saldo
    )

    db.add(activity)
    db.commit()
    db.refresh(customer)

    return customer.saldo


def tarik(db: Session, no_rekening: str, tipe: str, nominal: float) -> float:
    customer = db.query(Customer).filter(Customer.no_rekening == no_rekening).first()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"remark": "No Rekening Tidak ditemukan."}
        )

    customer.saldo -= nominal

    activity = Activity(
        no_rekening=no_rekening,
        tipe=tipe,
        nominal=nominal,
        saldo_setelah=customer.saldo
    )

    db.add(activity)
    db.commit()
    db.refresh(customer)

    return customer.saldo

def saldo(db: Session, no_rekening: str) -> str:
    customer = db.query(Customer).filter(Customer.no_rekening == no_rekening).first()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"remark": "No Rekening Tidak ditemukan."}
        )

    return customer.saldo
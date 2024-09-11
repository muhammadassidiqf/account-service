from fastapi import FastAPI,Depends,HTTPException, status
from models import SessionLocal
from sqlalchemy.orm import Session
from service import daftar as daftar_service,tabung as tabung_service,tarik as tarik_service,saldo as saldo_service, get_db
from requests import dto_daftar,dto_activity
import logging

app = FastAPI()

@app.post("/daftar", status_code=status.HTTP_200_OK)
def daftar(nasabah: dto_daftar, db: Session = Depends(get_db)):
    try:
        no_rekening = daftar_service(db, nasabah.nama, nasabah.nik, nasabah.no_hp)
        return {"message": "Daftar berhasil","no_rekening": no_rekening}
    except Exception as e:
        raise HTTPException(status_code=500, detail=F"Something went wrong {str(e)}")

@app.post("/tabung", status_code=status.HTTP_200_OK)
def tabung_uang(request: dto_activity, db: Session = Depends(get_db)):
    try:
        saldo = tabung_service(db, request.no_rekening,'tabung', request.nominal)
        return {"message": "Menabung berhasil", "no_rekening": request.no_rekening, "saldo": saldo}
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

@app.post("/tarik", status_code=status.HTTP_200_OK)
def tarik_uang(request: dto_activity, db: Session = Depends(get_db)):
    try:
        saldo = tarik_service(db, request.no_rekening,'tarik', request.nominal)
        return {"message": "Tarik uang berhasil", "no_rekening": request.no_rekening, "saldo": saldo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong {str(e)}")

@app.get("/saldo/{no_rekening}", status_code=status.HTTP_200_OK)
def saldo_rek(no_rekening: str, db: Session = Depends(get_db)):
    try:
        saldos = saldo_service(db, no_rekening)
        return {"message": "Saldo saat ini", "no_rekening": no_rekening, "saldo": saldos}
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")
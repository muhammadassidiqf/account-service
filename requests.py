from pydantic import BaseModel

class dto_daftar(BaseModel):
    nama: str
    nik: str
    no_hp: str
    
class dto_activity(BaseModel):
    no_rekening: str
    nominal: float
from sqlalchemy import Integer,String
from sqlalchemy.orm import mapped_column,Mapped
from extension import db

Base = db.Model


class Patient(Base):
    __tablename__="patients"
    
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String,nullable=False)
    age:Mapped[int]=mapped_column(Integer,nullable=False)
    phone:Mapped[int]=mapped_column(String(15),nullable=False,unique=True)
    
    def __repr__(self):
        return f"<Patient {self.name}>" # from this repr class we call directly like patient (patient name)
    
    
from sqlalchemy import Integer,String
from sqlalchemy.orm import mapped_column,Mapped
from extension import db

Base=db.Model 

class Department(Base):
    
    __tablename__="departments"
    
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String,nullable=False,unique=True)
    
    def __repr__(self):
        return f"<Department {self.name}>"
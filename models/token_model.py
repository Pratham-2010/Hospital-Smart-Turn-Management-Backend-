from sqlalchemy import String,Integer,ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from extension import db

Base=db.Model

class Token(Base):
    __tablename__="tokens"
    
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    
    token_number:Mapped[int]=mapped_column(Integer,nullable=False)
    
    status:Mapped[str]=mapped_column(String(20),nullable=False,default="WAITING")
    
    #now lets connect required foreign keys to this table
    patient_id:Mapped[int]=mapped_column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )
    
    department_id:Mapped[int]=mapped_column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )
    
    #token number must be unique per department
    __table_args__=(
        UniqueConstraint(
            "token_number","department_id",
            name="unique_token_per_department"
        ),
    )
    
    def __repr__(self):
        return f"<Token : {self.token_number}>"
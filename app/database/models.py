from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

"""
Razão social
- Telefone
- Endereço
- Data de cadastro
- Faturamento declarado
- Dados bancários (Um cliente pode ter mais de um banco)
    - Ag
    - Conta
    - Banco

"""


class User(Base):
    __tablename__ = "Users"

    company = Column(String, primary_key=True)
    address = Column(String, nullable=True)
    billing = Column(Integer, nullable=False)
    bank_info = relationship("Bank")
    active = Column(Boolean, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), server_onupdate=func.now())


class Bank(Base):

    __tablename__ = "Bancos"

    id = Column(Integer, primary_key=True)
    company = Column(String, ForeignKey(User.company))
    agency = Column(String, nullable=False)
    account = Column(String, nullable=False)
    bank = Column(String, nullable=False)

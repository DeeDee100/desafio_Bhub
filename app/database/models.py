from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Company(Base):
    __tablename__ = "company"

    cnpj = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    email = Column(String, nullable=True)
    income = Column(Integer, nullable=False)  # Faturamento
    active = Column(Boolean, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), server_onupdate=func.now())
    bank_info = relationship("Bank")


class Bank(Base):

    __tablename__ = "bank"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String, ForeignKey("company.cnpj"))
    agency = Column(String, nullable=False)
    account = Column(String, nullable=False)
    bank = Column(String, nullable=False)

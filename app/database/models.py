from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, SmallInteger
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
    bank_info = relationship(
        "Bank",
        cascade="all,delete-orphan",
        back_populates="company_name",
        uselist=True,
    )


class Bank(Base):

    __tablename__ = "bank"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String, ForeignKey("company.cnpj"))
    company_name = relationship("Company", back_populates="bank_info")
    agency = Column(String, nullable=False)
    account = Column(String, nullable=False)
    bank = Column(String, nullable=False)
    bank_code = Column(SmallInteger)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), server_onupdate=func.now())


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    is_staff = Column(Boolean, nullable=False)

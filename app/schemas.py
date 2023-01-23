from pydantic import BaseModel, EmailStr
from typing import Optional


class CompanyEntry(BaseModel):

    cnpj: str
    name: str
    address: str
    income: int
    email: Optional[EmailStr]
    active: Optional[bool] = True


class CompanyUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    income: Optional[int]
    email: Optional[EmailStr]
    active: Optional[bool] = True


class BankEntry(BaseModel):
    cnpj: str
    agency: str
    account: str
    bank: str


class BankDelete(BaseModel):
    agency: str
    account: str

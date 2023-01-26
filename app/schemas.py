from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re
from itertools import cycle


class CompanyEntry(BaseModel):

    cnpj: str
    name: str
    address: str
    income: int
    email: Optional[EmailStr]
    active: Optional[bool] = True

    @validator("cnpj")
    def check_cnpj(cls, value):
        if len(value) != 14:
            raise ValueError("CNPJ inválido!")
        pattern = re.compile(r"[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2}")
        if not re.fullmatch(pattern, value):
            raise ValueError("CNPJ inválido!")
        cnpj_r = value[::-1]
        for i in range(2, 0, -1):
            cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
            dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
            if cnpj_r[i - 1:i] != str(dv % 10):
                raise ValueError("CNPJ Inválido!")
        return value

    class Config:
        schema_extra = {
            "example": {
                "cnpj": "84048818000174",
                "name": "Dee company",
                "address": "Rua dos Bobos, 0",
                "income": 1000,
                "email": "dee@example.com",
                "active": True,
            }
        }


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


class UserEntry(BaseModel):
    name: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

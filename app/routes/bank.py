from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from app.OAuth import OAuth2
from app.database.database import get_db
from app.database import models
from app import schemas

router = APIRouter(tags=["Banco"], dependencies=[Depends(OAuth2.get_token_header)])


@router.get("/{cnpj}")
def home_bank(cnpj: str, db: Session = Depends(get_db)):
    banks = db.query(models.Bank).filter(models.Bank.cnpj == cnpj).all()
    return {"message": banks}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_bank(bank: schemas.BankEntry, db: Session = Depends(get_db)):
    new = models.Bank(**bank.dict())
    db.add(new)
    try:
        db.commit()
        db.refresh(new)
        return {"message": bank.dict()}
    except IntegrityError as err:
        raise HTTPException(status_code=409, detail={"message": err.args})


@router.delete("/delete/{cnpj}")
def delete_bank_account(
    cnpj: str, bank_info: schemas.BankDelete, db: Session = Depends(get_db)
):
    request_bank = (
        db.query(models.Bank)
        .filter(
            models.Bank.cnpj == cnpj,
            models.Bank.account == bank_info.account,
            models.Bank.agency == bank_info.agency,
        )
        .first()
    )

    if not request_bank:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    db.delete(request_bank)
    db.commit()
    return Response(status_code=204)

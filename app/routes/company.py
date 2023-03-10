from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from app.database.database import get_db
from app.database import models
from app import schemas

router = APIRouter(tags=["Clientes"])


@router.get("/")
def home_company(db: Session = Depends(get_db)):
    users = db.query(models.Company).all()
    return {"message": users}


@router.post("/register", status_code=201)
def register_company(user: schemas.CompanyEntry, db: Session = Depends(get_db)):
    new = models.Company(**user.dict())
    db.add(new)
    try:
        db.commit()
        db.refresh(new)
        return {"message": user.dict()}
    except IntegrityError as err:
        raise HTTPException(status_code=409, detail={"message": err.args})


@router.delete("/delete/{cnpj}", status_code=204)
def delete_company(cnpj: str, db: Session = Depends(get_db)):
    requested_company = (
        db.query(models.Company).filter(models.Company.cnpj == cnpj).first()
    )

    if not requested_company:
        raise HTTPException(
            status_code=404, detail=f"Cliente com cnpj {cnpj} não encontrado"
        )

    db.delete(requested_company)
    db.commit()
    return Response(status_code=204)


@router.put("/update/{cnpj}")
def update_company(
    cnpj: str, company: schemas.CompanyUpdate, db: Session = Depends(get_db)
):
    company_query = db.query(models.Company).filter(models.Company.cnpj == cnpj)
    if not company_query.first():
        raise HTTPException(
            status_code=404, detail=f"Cliente com cnpj {cnpj} não encontrado"
        )

    data_dict = company.dict(exclude_unset=True)
    company_query.update(data_dict)

    db.commit()
    return {"message": " updated"}

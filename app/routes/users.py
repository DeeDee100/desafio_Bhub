from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from app.database.database import get_db
from app.database import models
from app import schemas


router = APIRouter(tags=['Users'])


@router.get("/")
def home_users():
    return {'message': 'users root, please login and/read the docs to use the API'}


@router.get("/teste")
def teste(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {'message': users}


@router.post("/register", status_code=201)
def register_user(user: schemas.UserEntry, db: Session = Depends(get_db)):
    is_first_user = db.query(models.User).all()
    if not is_first_user:
        superuser = True
    new_user = models.User(
        **user.dict(),
        is_admin=superuser,
        is_staff=superuser
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return {"message": "Deu bão"}
    except IntegrityError as err:
        raise HTTPException(status_code=409, detail={"message": err})

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from app.database.database import get_db
from app import utilis
from app.database import models
from app import schemas


router = APIRouter(tags=['Users'])


@router.get("/")
def home_users():
    return {'message': 'users root, please login and/read the docs to use the API'}



@router.post("/register", status_code=201)
def register_user(user: schemas.UserEntry, db: Session = Depends(get_db)):
    superuser = False
    usres_query = db.query(models.User).all()
    if not usres_query:
        superuser = True
    pwd_hashed = utilis.hash(user.password)
    user.password = pwd_hashed
    new_user = models.User(
        **user.dict(),
        is_admin=superuser,
        is_staff=superuser
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return_user = user.dict()
        return_user.pop('password')
        return {"data": return_user}
    except IntegrityError as err:
        raise HTTPException(status_code=409, detail={"message": err})

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from app.database.database import get_db
from app.database.models import User
from app.OAuth import OAuth2
from app import utilis
from app import schemas


router = APIRouter(tags=['Users'], dependencies=[Depends(OAuth2.get_token_header)])


@router.get("/")
def home_users():
    return {'message': 'users root, please login'}



@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserEntry, db: Session = Depends(get_db)):
    superuser = False
    usres_query = db.query(User).all()
    if not usres_query:
        superuser = True
    pwd_hashed = utilis.hash(user.password)
    user.password = pwd_hashed
    new_user = User(
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


@router.patch("/update/{email}")
def update_users(
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: int= Depends(OAuth2.current_user)
):
    logged_user = db.query(User).filter_by(email=current_user.email).first()

    if not logged_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail={'message': 'Operação não autorizada, contate um supervisor'}
        )

    user_query = db.query(User).filter_by(email=user.email).first()
    data_dict = user.dict(exclude_unset=True)
    user_query.update(data_dict)
    db.commit()
    return {'message': 'Updated'}

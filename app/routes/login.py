from fastapi import APIRouter, Depends, status, HTTPException
from app.database.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# from app import schemas
from app.schemas import Token
from app.OAuth import OAuth2
from app.database import models
from sqlalchemy.orm.session import Session

router = APIRouter(
    tags=['Login']
)


@router.post("/login")
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()

    print(user.email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Credenciais invalidas")
    acess_token = OAuth2.create_token(data={"user_email": user.email})
    return {"access_token": acess_token, "token_type": "bearer"}

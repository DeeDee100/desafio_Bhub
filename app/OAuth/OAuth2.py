from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm.session import Session
from app.database.database import get_db
from fastapi.security import OAuth2PasswordBearer
from app.database.config import settings
import datetime as dt


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRE_TIME = settings.access_token_expire_minutes
CREDENTIAL_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credencial invalida",
        headers={"WWW-Authenticate": "Bearer"},
)


class TokenData(BaseModel):
    email: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_token(data: dict):
    to_encode = data.copy()

    expire = dt.datetime.utcnow() + dt.timedelta(minutes=EXPIRE_TIME)
    to_encode.update({"exp": expire})

    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("user_email")
        if email is None:
            raise CREDENTIAL_EXCEPTION
        token_data = TokenData(email=email)
    except JWTError:
        raise CREDENTIAL_EXCEPTION
    return token_data


def current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)


def get_token_header(x_token: str = Header()):
    verify_token(x_token)

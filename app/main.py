from fastapi import FastAPI, Depends
from pydantic import BaseModel
from .database.database import get_db, engine
from sqlalchemy.orm.session import Session
from .database import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class User(BaseModel):
    name: str
    email: str




@app.get("/")
def home(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {"message": users}


@app.post("/register")
def register_user(user: User):
    return {"message": "Cadastrado"}
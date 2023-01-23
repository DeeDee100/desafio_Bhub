from fastapi import FastAPI
from .database.database import engine
from .database import models
from .routes import company, bank

app = FastAPI(
    title="Bhub Bank",
    description="API para cadastro de clientes e bancos do desafio Bhub",
    version=0.1,
)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "This is the root path from the bhub bank api, please refeer to the docs on how to use on /docs"
    }


app.include_router(company.router, prefix="/company")
app.include_router(bank.router, prefix="/bank")

from fastapi import FastAPI
from router import accounting_router, business_router, loan_application_router
from fastapi.middleware.cors import CORSMiddleware

from model import db_model
from db_config.database import engine, Base

db_model.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(accounting_router.router)
app.include_router(business_router.router)
app.include_router(loan_application_router.router)



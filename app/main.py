from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Anonymizer Microservice",
    description="Secure NLP microservice for dataset anonymization",
    version="1.0.0"
)

app.include_router(router)

from fastapi import FastAPI

from app.routes.fraud import router as fraud_router
from app.routes.assistant import router as assistant_router

app = FastAPI(
    title="AI Banking Operations Agent"
)

app.include_router(fraud_router)
app.include_router(assistant_router)


@app.get("/")
def home():
    return {
        "message": "AI Banking Operations Agent Running"
    }
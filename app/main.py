from fastapi import FastAPI

from app.routes.fraud import router as fraud_router
from app.routes.assistant import router as assistant_router

app = FastAPI(
    title="AI Banking Operations Agent"
)

# Security Headers
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)

    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data: https:; "
        "frame-ancestors 'none';"
    )

    return response

app.include_router(fraud_router)
app.include_router(assistant_router)

@app.get("/")
def home():
    return {
        "message": "AI Banking Operations Agent Running"
    }
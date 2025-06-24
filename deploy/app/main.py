from fastapi import FastAPI
from app.auth import router as auth_router
from app.cert import router as cert_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(cert_router, prefix="/ssl")

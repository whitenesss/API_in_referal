from fastapi import FastAPI
from routers import auth, referral


app = FastAPI()

app.include_router(auth.router)
app.include_router(referral.router)

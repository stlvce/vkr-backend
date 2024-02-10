from fastapi import FastAPI
from app.user.router import userRouter

app = FastAPI()

app.include_router(userRouter)

from fastapi import FastAPI 
from app.routers import auth, user,trainer

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(trainer.router)

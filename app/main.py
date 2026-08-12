from fastapi import FastAPI 
from app.routers import auth,trainer,schedule,member

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth.router)
app.include_router(trainer.router)
app.include_router(schedule.router)
app.include_router(member.router)
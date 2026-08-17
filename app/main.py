from fastapi import FastAPI 
from app.routers import trainer,schedule,member,attendance , membership,auth

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth.router)
app.include_router(trainer.router)
app.include_router(schedule.router)
app.include_router(member.router)
app.include_router(attendance.router)
app.include_router(membership.router)
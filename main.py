from database.session import engine, Base
from fastapi import FastAPI, Depends
from auth.register import router as register_router

app = FastAPI()

app.include_router(register_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Roblox Admin Panel API is running."}

if __name__ == "__main__":
    from uvicorn import run
    run("main:app", reload=True)

from database.session import engine, Base
from fastapi import FastAPI, Depends
from auth.register import router as register_router
from auth.login import router as login_router
from debug.users import router as debug_users_router
from debug.setters import router as debug_setters_router
from user.users import router as users_router

# Import all models to register them with Base
from models.user import User
from models.todo import ToDoTask
from models.blacklist import Blacklist
from models.watchlist import Watchlist
from models.kickban import KickBanLog
from models.player_notes import PlayerNote
from models.team_notes import TeamNote

app = FastAPI()

app.include_router(register_router)
app.include_router(login_router)
app.include_router(debug_users_router)
app.include_router(users_router)
app.include_router(debug_users_router)
app.include_router(debug_setters_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"status": 200}

if __name__ == "__main__":
    from uvicorn import run
    run("main:app", reload=True)

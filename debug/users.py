from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from database.session import get_session

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/users")
async def list_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "roblox_name": user.roblox_name,
            "role": user.role,
            "is_active": user.is_active,
            "approved": user.approved,
            "last_login": user.last_login
        }
        for user in users
    ]

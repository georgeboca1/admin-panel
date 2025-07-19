from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from database.session import get_session

router = APIRouter(prefix="/debug", tags=["debug"])

@router.post("/approve")
async def set_approved(id: int,session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == id))
    user = result.scalars().first()
    if user:
        user.approved = True
        await session.commit()
        return {
            "id": user.id,
            "username": user.username,
            "roblox_name": user.roblox_name,
            "role": user.role,
            "is_active": user.is_active,
            "approved": user.approved,
            "last_login": user.last_login
        }
    return {"error": "User not found"}

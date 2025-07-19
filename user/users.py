from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from database.session import get_session
from models.user import User
from auth.dependencies import get_owner_user, VALID_ROLES
from user.users_schema import *

router = APIRouter(prefix="/users", tags=["users"])

#TODO: Do not allow anyone but logged in people to get user data.

@router.get("", response_model=list[UserResponse])
async def get_users(
    session: AsyncSession = Depends(get_session),
):
    """List all users in the system"""
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a specific user by ID"""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_owner_user)
):
    """Update a user's information"""
    # Check if user exists
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate role if being updated
    if user_update.role is not None and user_update.role not in VALID_ROLES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid role. Must be one of: {', '.join(VALID_ROLES)}"
        )

    # Create update dict excluding None values
    update_data = user_update.dict(exclude_unset=True)
    
    if update_data:
        await session.execute(
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
        )
        await session.commit()

    # Fetch and return updated user
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one()

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_owner_user)
):
    """Delete a user"""
    # Prevent self-deletion
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account"
        )

    # Check if user exists
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user
    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()

@router.patch("/{user_id}/approve", response_model=UserResponse)
async def approve_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_owner_user)
):
    """Approve a user's account"""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.execute(
        update(User)
        .where(User.id == user_id)
        .values(approved=True)
    )
    await session.commit()

    # Fetch and return updated user
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one()

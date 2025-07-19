from fastapi import APIRouter, HTTPException, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from models.user import User
from database.session import get_session, Base
from auth.register_schema import RegisterRequest
import re

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,32}$")
ROBLOX_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,32}$")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(request: RegisterRequest, session: AsyncSession = Depends(get_session)):
    # Validate username and roblox_name
    if not USERNAME_REGEX.match(request.username):
        raise HTTPException(status_code=400, detail="Invalid username format.")
    if not ROBLOX_REGEX.match(request.roblox_name):
        raise HTTPException(status_code=400, detail="Invalid Roblox username format.")

    try:
        # Using a transaction to ensure atomicity
        async with session.begin():
            # Check for existing user using SELECT FOR UPDATE to prevent race conditions
            result = await session.execute(
                select(User)
                .where(User.username == request.username)
                .with_for_update()
            )
            if result.scalar():
                raise HTTPException(status_code=409, detail="Username already exists.")

            # Hash password
            password_hash = pwd_context.hash(request.password)

            # Create new user - let SQLAlchemy handle the ID
            new_user = User(
                username=request.username,
                password_hash=password_hash,
                roblox_name=request.roblox_name,
                role="user",
                is_active=True,
                approved=False,
                last_login=None
            )
            session.add(new_user)

        return {"message": "Registration successful. Awaiting approval."}
    except SQLAlchemyError as e:
        # Log the error here if you have logging set up
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration. Please try again."
        )

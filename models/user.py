from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database.session import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    roblox_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    approved = Column(Boolean, default=False)
    last_login = Column(DateTime, default=None)

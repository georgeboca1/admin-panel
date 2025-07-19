from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
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

    # Relationships
    assigned_tasks = relationship("ToDoTask", foreign_keys="ToDoTask.assigned_to", back_populates="assignee")
    created_tasks = relationship("ToDoTask", foreign_keys="ToDoTask.created_by", back_populates="creator")
    blacklist_entries = relationship("Blacklist", back_populates="admin")
    watchlist_entries = relationship("Watchlist", back_populates="admin")
    kickban_logs = relationship("KickBanLog", back_populates="admin")
    player_notes = relationship("PlayerNote", back_populates="admin")
    team_notes = relationship("TeamNote", back_populates="creator")

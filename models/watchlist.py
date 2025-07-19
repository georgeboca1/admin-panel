from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database.session import Base
import datetime

class Watchlist(Base):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    roblox_id = Column(Integer, nullable=False)
    tags = Column(JSON, default=list)  # Store tags as JSON array
    notes = Column(String)
    added_by = Column(Integer, ForeignKey("users.id"))
    date_added = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship
    admin = relationship("User", back_populates="watchlist_entries")
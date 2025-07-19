from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base
import datetime

class PlayerNote(Base):
    __tablename__ = "player_notes"

    id = Column(Integer, primary_key=True, index=True)
    roblox_id = Column(Integer, nullable=False)
    note = Column(String, nullable=False)
    added_by = Column(Integer, ForeignKey("users.id"))
    date_added = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship
    admin = relationship("User", back_populates="player_notes")
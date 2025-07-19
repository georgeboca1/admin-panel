from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database.session import Base
import datetime

class TeamNote(Base):
    __tablename__ = "team_notes"

    id = Column(Integer, primary_key=True, index=True)
    note = Column(String, nullable=False)
    role_tag = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    replies = Column(JSON, default=list)  # Store replies as JSON array
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship
    creator = relationship("User", back_populates="team_notes")
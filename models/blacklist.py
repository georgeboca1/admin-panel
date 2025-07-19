from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base
import datetime

class Blacklist(Base):
    __tablename__ = "blacklist"

    id = Column(Integer, primary_key=True, index=True)
    roblox_id = Column(Integer, nullable=False)
    roblox_name = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    added_by = Column(Integer, ForeignKey("users.id"))
    evidence_url = Column(String)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship
    admin = relationship("User", back_populates="blacklist_entries")
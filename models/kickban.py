from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base
import datetime

class KickBanLog(Base):
    __tablename__ = "kickban_logs"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # kick or ban
    roblox_id = Column(Integer, nullable=False)
    roblox_name = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    evidence = Column(String)
    duration = Column(String)
    added_by = Column(Integer, ForeignKey("users.id"))
    date_added = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship
    admin = relationship("User", back_populates="kickban_logs")
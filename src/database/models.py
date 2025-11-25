import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Scan(Base):
    """Database model for a single scan record."""
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String, unique=True, index=True, nullable=False)
    filename = Column(String, nullable=False)
    identified_type = Column(String, nullable=False)
    status = Column(String, default="queued", nullable=False)
    
    # Storing complex objects as JSON
    tool_findings = Column(JSON, nullable=True)
    ai_analysis = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def to_dict(self):
        """Converts the object to a dictionary."""
        return {
            "id": self.id,
            "scan_id": self.scan_id,
            "filename": self.filename,
            "identified_type": self.identified_type,
            "status": self.status,
            "tool_findings": self.tool_findings,
            "ai_analysis": self.ai_analysis,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

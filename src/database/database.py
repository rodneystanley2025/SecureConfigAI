from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Database Configuration ---
DATABASE_URL = "sqlite:///./a-i-scanner.db"

# Create the database engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} # Needed for SQLite with FastAPI
)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency to get a database session.
    Ensures the session is always closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings
from app.db.models import Item  # Import models to register them

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production to disable SQL logging
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,  # Recycle connections after 1 hour
)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session


def init_db():
    """Initialize database - create all tables"""
    SQLModel.metadata.create_all(engine)


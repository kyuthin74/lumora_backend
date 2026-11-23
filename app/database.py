from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import Settings

settings = Settings()
DATABASE_URL = settings.DATABASE_URL

# pool_pre_ping avoids "connection closed" errors when a hosted DB
# (e.g. Supabase pooler) drops idle connections.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    with SessionLocal() as session:
        yield session

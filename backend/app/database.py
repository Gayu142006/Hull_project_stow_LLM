import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./stow.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from .models.location import StowLocation
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    if db.query(StowLocation).count() == 0:
        sample_locations = [
            StowLocation(location_id="A-01", available_length_cm=22.0, available_width_cm=17.0, available_height_cm=12.0, weight_capacity_kg=10.0, occupied_volume_cm3=500.0, status="AVAILABLE"),
            StowLocation(location_id="A-02", available_length_cm=40.0, available_width_cm=30.0, available_height_cm=30.0, weight_capacity_kg=15.0, occupied_volume_cm3=1000.0, status="AVAILABLE"),
            StowLocation(location_id="A-03", available_length_cm=15.0, available_width_cm=15.0, available_height_cm=10.0, weight_capacity_kg=10.0, occupied_volume_cm3=200.0, status="AVAILABLE"),
            StowLocation(location_id="A-04", available_length_cm=25.0, available_width_cm=20.0, available_height_cm=15.0, weight_capacity_kg=10.0, occupied_volume_cm3=600.0, status="AVAILABLE")
        ]
        db.add_all(sample_locations)
        db.commit()
    db.close()

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./device_ids.db"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Define DeviceID model
class DeviceID(Base):
    __tablename__ = "device_ids"

    id = Column(Integer, primary_key=True, index=True)
    android_id = Column(String, unique=True, index=True)
    advertising_id = Column(String, index=True)
    limit_ad_tracking = Column(Boolean, default=False)
    device_info = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Initialize database
def init_db():
    Base.metadata.create_all(bind=engine)

# Database CRUD operations
def get_device_ids(db, skip=0, limit=100):
    devices = db.query(DeviceID).offset(skip).limit(limit).all()
    
    # Konversi semua objek SQLAlchemy ke dict
    return [
        {
            "id": device.id,
            "android_id": device.android_id,
            "advertising_id": device.advertising_id,
            "limit_ad_tracking": device.limit_ad_tracking,
            "device_info": device.device_info,
            "created_at": device.created_at,
            "updated_at": device.updated_at
        }
        for device in devices
    ]

def get_device_id_by_android_id(db, android_id: str):
    device = db.query(DeviceID).filter(DeviceID.android_id == android_id).first()
    if not device:
        return None
    
    # Konversi objek SQLAlchemy ke dict
    return {
        "id": device.id,
        "android_id": device.android_id,
        "advertising_id": device.advertising_id,
        "limit_ad_tracking": device.limit_ad_tracking,
        "device_info": device.device_info,
        "created_at": device.created_at,
        "updated_at": device.updated_at
    }

def add_device_id(db, device_data):
    # Langsung cek di database
    db_device_obj = db.query(DeviceID).filter(DeviceID.android_id == device_data.android_id).first()
    
    # Convert device_info to dict using model_dump() for Pydantic v2
    device_info_dict = device_data.device_info.model_dump()
    
    if db_device_obj:
        # Update existing device
        db_device_obj.advertising_id = device_data.advertising_id
        db_device_obj.limit_ad_tracking = device_data.limit_ad_tracking
        db_device_obj.device_info = device_info_dict
        db_device_obj.updated_at = datetime.utcnow()
        db_device = db_device_obj
    else:
        # Create new device
        db_device = DeviceID(
            android_id=device_data.android_id,
            advertising_id=device_data.advertising_id,
            limit_ad_tracking=device_data.limit_ad_tracking,
            device_info=device_info_dict,
        )
        db.add(db_device)
    
    db.commit()
    db.refresh(db_device)
    
    # Konversi objek SQLAlchemy ke dict untuk serialisasi
    return {
        "id": db_device.id,
        "android_id": db_device.android_id,
        "advertising_id": db_device.advertising_id,
        "limit_ad_tracking": db_device.limit_ad_tracking,
        "device_info": db_device.device_info,
        "created_at": db_device.created_at,
        "updated_at": db_device.updated_at
    }

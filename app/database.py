from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

SQLALCHEMY_DATABASE_URL = "sqlite:///./device_ids.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DeviceID(Base):
    __tablename__ = "device_ids"

    id = Column(Integer, primary_key=True, index=True)
    android_id = Column(String, unique=True, index=True)
    advertising_id = Column(String, index=True)
    limit_ad_tracking = Column(Boolean, default=False)
    device_info = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_device_ids(db, skip=0, limit=100):
    devices = db.query(DeviceID).offset(skip).limit(limit).all()
    
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
    db_device_obj = db.query(DeviceID).filter(DeviceID.android_id == device_data.android_id).first()
    
    device_info_dict = device_data.device_info.model_dump()
    
    if db_device_obj:
        db_device_obj.advertising_id = device_data.advertising_id
        db_device_obj.limit_ad_tracking = device_data.limit_ad_tracking
        db_device_obj.device_info = device_info_dict
        db_device_obj.updated_at = datetime.utcnow()
        db_device = db_device_obj
    else:
        db_device = DeviceID(
            android_id=device_data.android_id,
            advertising_id=device_data.advertising_id,
            limit_ad_tracking=device_data.limit_ad_tracking,
            device_info=device_info_dict,
        )
        db.add(db_device)
    
    db.commit()
    db.refresh(db_device)
    
    return {
        "id": db_device.id,
        "android_id": db_device.android_id,
        "advertising_id": db_device.advertising_id,
        "limit_ad_tracking": db_device.limit_ad_tracking,
        "device_info": db_device.device_info,
        "created_at": db_device.created_at,
        "updated_at": db_device.updated_at
    }
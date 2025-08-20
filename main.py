from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Optional
import logging
from datetime import datetime

from app.models import DeviceIdData, DeviceIdResponse, DeviceIdCreate
from app.database import get_device_ids, get_device_id_by_android_id, add_device_id, SessionLocal, init_db
from app.utils import get_db, setup_logger

# Setup application logger
logger = setup_logger()

# Initialize FastAPI app
app = FastAPI(
    title="ID Collector API",
    description="API for collecting and retrieving Android device IDs",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_db_client():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")

# API endpoints
@app.post("/api/store-ids", response_model=DeviceIdResponse)
async def store_ids(device_data: DeviceIdCreate, db=Depends(get_db)):
    try:
        logger.info(f"Received request to store IDs for device: {device_data.android_id}")
        
        # Add device ID to database
        result = add_device_id(db, device_data)
        
        return {
            "success": True,
            "message": "Device IDs stored successfully",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error storing device IDs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/all-ids", response_model=DeviceIdResponse)
async def get_all_ids(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    try:
        logger.info(f"Fetching all device IDs with skip={skip}, limit={limit}")
        devices = get_device_ids(db, skip=skip, limit=limit)
        
        return {
            "success": True,
            "message": f"Retrieved {len(devices)} device IDs",
            "data": devices
        }
    except Exception as e:
        logger.error(f"Error retrieving all device IDs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/get-ids/{device_id}", response_model=DeviceIdResponse)
async def get_device_by_id(device_id: str, db=Depends(get_db)):
    try:
        logger.info(f"Fetching device with ID: {device_id}")
        device = get_device_id_by_android_id(db, device_id)
        
        if not device:
            logger.warning(f"Device with ID {device_id} not found")
            raise HTTPException(status_code=404, detail="Device not found")
        
        return {
            "success": True,
            "message": "Device found",
            "data": device
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving device ID {device_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

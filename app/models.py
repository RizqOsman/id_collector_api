from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class DeviceInfo(BaseModel):
    manufacturer: str
    model: str
    os_version: str
    screen_size: str = None
    screen_density: int = None
    device_language: str = None
    network_type: str = None
    ram_total: int = None
    storage_total: int = None
    storage_free: int = None
    battery_level: int = None
    is_rooted: bool = None
    installed_apps_count: int = None

class DeviceIdCreate(BaseModel):
    android_id: str
    advertising_id: str
    limit_ad_tracking: bool
    device_info: DeviceInfo

class DeviceIdData(DeviceIdCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DeviceIdResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

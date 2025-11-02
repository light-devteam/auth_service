from typing import Optional

from pydantic import BaseModel


class FingerprintSchema(BaseModel):
    visitor_id: str
    user_agent: str
    platform: Optional[str] = None
    screen_resolution: Optional[str] = None
    timezone: Optional[str] = None
    vendor: Optional[str] = None
    webgl_vendor: Optional[str] = None
    webgl_renderer: Optional[str] = None
    hardware_concurrency: Optional[int] = None
    device_memory: Optional[int] = None
    languages: Optional[str] = None

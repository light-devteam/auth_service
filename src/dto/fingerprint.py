from msgspec import Struct


class FingerprintDTO(Struct):
    visitor_id: str
    user_agent: str
    platform: str = None
    screen_resolution: str = None
    timezone: str = None
    vendor: str = None
    webgl_vendor: str = None
    webgl_renderer: str = None
    hardware_concurrency: int = None
    device_memory: int = None
    languages: str = None

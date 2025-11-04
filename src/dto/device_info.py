from msgspec import Struct


class DeviceInfoDTO(Struct):
    ip: str

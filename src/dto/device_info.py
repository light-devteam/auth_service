from msgspec import Struct

from src.dto.fingerprint import FingerprintDTO


class DeviceInfoDTO(Struct):
    ip: str
    fingerprint: FingerprintDTO

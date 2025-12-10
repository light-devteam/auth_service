from enum import StrEnum


class ProbeType(StrEnum):
    LIVENESS = 'Liveness'
    READINESS = 'Readiness'

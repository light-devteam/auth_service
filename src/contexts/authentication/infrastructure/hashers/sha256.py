import hashlib

from src.contexts.authentication.domain.hashers import IHasher


class SHA256Hasher(IHasher):
    def hash(self, data: bytes) -> bytes:
        return hashlib.sha256(data).digest()

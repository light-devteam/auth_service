from msgspec import Struct


class JWKPairDTO(Struct):
    public: dict
    private: dict

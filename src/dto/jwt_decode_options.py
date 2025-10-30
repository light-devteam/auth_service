from msgspec import Struct


class JwtDecodeOptionsDTO(Struct):
    verify_signature: bool = True
    verify_exp: bool = True
    verify_nbf: bool = True
    verify_iat: bool = True
    verify_aud: bool = True
    verify_iss: bool = True
    verify_sub: bool = True
    verify_jti: bool = True

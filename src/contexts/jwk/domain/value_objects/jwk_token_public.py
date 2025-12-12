import json


class JWKTokenPublic(dict):
    def __init__(self, value: str | bytes | bytearray | dict) -> None:
        if isinstance(value, (str, bytes, bytearray)):
            value = json.loads(value)
        if not isinstance(value, dict):
            raise TypeError(f'{self.__class__.__name__} must be initialized with a JSON object')
        super().__init__(value)

    def __str__(self) -> str:
        return json.dumps(self)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({json.dumps(self)})'

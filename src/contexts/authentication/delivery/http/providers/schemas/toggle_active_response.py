from pydantic import BaseModel


class ToggleActiveResponse(BaseModel):
    is_active: bool

from datetime import datetime
from pydantic import BaseModel


class CardBase(BaseModel):
    store_id: int
    code: str
    code_type: int


class CardOut(CardBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CardIn(CardBase):
    pass

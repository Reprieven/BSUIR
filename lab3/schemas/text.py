from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class STextBase(BaseModel):
    name: str
    text: str

    @field_validator("name")
    @classmethod
    def validate_filename(cls, v: str) -> str:
        if not v.lower().endswith(".rtf"):
            raise ValueError("Файл должен иметь расширение .rtf")
        return v


class STextAdd(STextBase):
    pass


class STextUpdate(BaseModel):
    text: Optional[str] = None

class STextResponse(STextBase):
    id: int
    date: datetime

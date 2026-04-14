from pydantic import BaseModel, Field, ConfigDict


class SLemmaBase(BaseModel):
    lemma: str
    morph: str
    role: str


class SLemmaAdd(SLemmaBase):
    word: str


class SLemmaAddDb(SLemmaAdd):
    text_id: int = Field(..., ge=1)


class SLemmaUpdate(SLemmaBase):
    pass


class SLemmaResponse(SLemmaBase):
    id: int
    word: str

class SLemmaCount(SLemmaBase):
    count: int
    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel

class SStat(BaseModel):
    texts: int
    words: int
    unique_words: int
    lemmas: int
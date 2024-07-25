from pydantic import BaseModel


class MemesOut(BaseModel):
    title: str
    category: str
    image: str


class MemesIn(BaseModel):
    title: str
    category: str
    image: bytes


class MemesPut(BaseModel):
    title: str | None = None
    category: str | None = None
    image: bytes | None = None



from pydantic import BaseModel
from typing import List, Optional


class SSentenceResponse(BaseModel):
    id: int
    text_id: int
    index: int
    content: str


class DepNode(BaseModel):
    id: int
    word: str
    lemma: str
    pos: str
    dep: str
    head_id: int


class DepEdge(BaseModel):
    source: int
    target: int
    label: str


class DepTree(BaseModel):
    nodes: List[DepNode]
    edges: List[DepEdge]


class ConstituentNode(BaseModel):
    label: str
    word: Optional[str] = None
    children: Optional[List["ConstituentNode"]] = None


class ConstituencyTree(BaseModel):
    root: ConstituentNode
    bracket_notation: str


class SSentenceAnalysis(BaseModel):
    sentence: str
    dependency_tree: DepTree
    constituency_tree: ConstituencyTree


class SSentenceAnalyzeInput(BaseModel):
    text: str

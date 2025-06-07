from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GraphPointDTO:
    timestamp: datetime
    price: float
    text: Optional[str] = None

@dataclass
class MetaDTO:
    total_points: int
    normalized_points: int
    year: Optional[int] = None
    version: Optional[str] = None

@dataclass
class LinksDTO:
    self: str
    next: Optional[str] = None
    prev: Optional[str] = None

@dataclass
class GraphDataDTO:
    meta: MetaDTO
    data: List[GraphPointDTO]
    links: LinksDTO
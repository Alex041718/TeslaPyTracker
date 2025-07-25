from typing import List
from datetime import datetime
from dataclasses import dataclass

@dataclass
class SalePointDTO:
    date: datetime
    sales_count: int
    sold_vins: List[str]
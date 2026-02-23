from dataclasses import dataclass, field
from typing import Optional
from datetime import date


@dataclass
class LineItem:
    name: str
    quantity: int
    unit_price: float


@dataclass
class Invoice:
    invoice_id: str
    vendor: str
    amount: float
    items: list[LineItem] = field(default_factory=list)
    due_date: Optional[date] = None
    raw_text: str = ""
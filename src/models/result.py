from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    is_valid: bool
    issues: list[str]


@dataclass
class ApprovalResult:
    approved: bool
    reasoning: str
    requires_review: bool = False


@dataclass
class PaymentResult:
    success: bool
    message: str
    transaction_id: Optional[str] = None
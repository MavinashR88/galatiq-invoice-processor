from src.tools.db_client import get_item, has_sufficient_stock
from src.models.invoice import Invoice
from src.models.result import ValidationResult
from src.utils.logger import get_logger

log = get_logger(__name__)


def validate(invoice: Invoice) -> ValidationResult:
    log.info(f"Validating invoice: {invoice.invoice_id}")

    issues = []

    if invoice.amount <= 0:
        issues.append(f"Invalid amount: {invoice.amount}")

    for item in invoice.items:
        if item.quantity <= 0:
            issues.append(f"Invalid quantity for {item.name}: {item.quantity}")
            continue

        db_item = get_item(item.name)

        if db_item is None:
            issues.append(f"Unknown item not in inventory: {item.name}")
            continue

        if not has_sufficient_stock(item.name, item.quantity):
            issues.append(
                f"Insufficient stock for {item.name}: "
                f"requested {item.quantity}, available {db_item['stock']}"
            )

    is_valid = len(issues) == 0

    if is_valid:
        log.info(f"Invoice {invoice.invoice_id} passed validation")
    else:
        log.warning(f"Invoice {invoice.invoice_id} failed validation: {issues}")

    return ValidationResult(is_valid=is_valid, issues=issues)
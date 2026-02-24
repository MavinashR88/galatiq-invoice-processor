from src.tools.db_client import get_item, has_sufficient_stock
from src.models.invoice import Invoice
from src.models.result import ValidationResult
from src.utils.logger import get_logger
from datetime import date

log = get_logger(__name__)


def validate(invoice: Invoice) -> ValidationResult:
    log.info(f"Validating invoice: {invoice.invoice_id}")

    issues = []

    if invoice.amount <= 0:
        issues.append(f"Invalid amount: {invoice.amount}")

    calculated_total = sum(i.quantity * i.unit_price for i in invoice.items)
    if invoice.items and abs(calculated_total - invoice.amount) > 0.01:
        issues.append(
            f"Amount mismatch: invoice total is ${invoice.amount} "
            f"but line items sum to ${round(calculated_total, 2)}"
        )

    if invoice.due_date:
        try:
            due = date.fromisoformat(str(invoice.due_date))
            if due < date.today():
                log.warning(f"Invoice {invoice.invoice_id} is overdue: due date was {invoice.due_date}")
        except ValueError:
            issues.append(f"Invalid due date format: {invoice.due_date}")

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
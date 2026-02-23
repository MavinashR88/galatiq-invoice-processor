from src.agents.extractor import extract
from src.agents.validator import validate
from src.agents.approver import approve
from src.agents.payment import process_payment
from src.utils.logger import get_logger

log = get_logger(__name__)


def run(file_path: str) -> dict:
    log.info("=" * 50)
    log.info(f"Starting invoice pipeline for: {file_path}")
    log.info("=" * 50)

    invoice = extract(file_path)
    log.info(f"Extracted: {invoice.invoice_id} | {invoice.vendor} | ${invoice.amount}")

    validation = validate(invoice)
    log.info(f"Validation: {'PASSED' if validation.is_valid else 'FAILED'}")

    approval = approve(invoice, validation)
    log.info(f"Approval: {'APPROVED' if approval.approved else 'REJECTED'}")

    payment = process_payment(invoice, approval)
    log.info(f"Payment: {'SUCCESS' if payment.success else 'SKIPPED'}")

    log.info("=" * 50)

    return {
        "invoice_id": invoice.invoice_id,
        "vendor": invoice.vendor,
        "amount": invoice.amount,
        "validation": {
            "passed": validation.is_valid,
            "issues": validation.issues,
        },
        "approval": {
            "approved": approval.approved,
            "reasoning": approval.reasoning,
        },
        "payment": {
            "success": payment.success,
            "message": payment.message,
            "transaction_id": payment.transaction_id,
        },
    }
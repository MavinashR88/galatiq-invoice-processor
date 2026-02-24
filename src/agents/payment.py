import uuid
import json
from src.models.invoice import Invoice
from src.models.result import ApprovalResult, PaymentResult
from src.utils.logger import get_logger

log = get_logger(__name__)


def process_payment(invoice: Invoice, approval: ApprovalResult) -> PaymentResult:
    log.info(f"Processing payment for invoice: {invoice.invoice_id}")

    if not approval.approved:
        log.warning(f"Invoice {invoice.invoice_id} rejected — {approval.reasoning}")

        with open("logs/rejections.log", "a") as f:
            f.write(json.dumps({
                "invoice_id": invoice.invoice_id,
                "vendor": invoice.vendor,
                "amount": invoice.amount,
                "reason": approval.reasoning
            }) + "\n")

        return PaymentResult(
            success=False,
            message=f"Rejected: {approval.reasoning}",
        )

    transaction_id = str(uuid.uuid4())

    _mock_payment(vendor=invoice.vendor, amount=invoice.amount)

    log.info(f"Payment successful — transaction: {transaction_id}")

    return PaymentResult(
        success=True,
        message=f"Paid ${invoice.amount} to {invoice.vendor}",
        transaction_id=transaction_id,
    )


def _mock_payment(vendor: str, amount: float) -> dict:
    print(f"Paid {amount} to {vendor}")
    return {"status": "success"}
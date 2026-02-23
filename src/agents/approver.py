from src.tools.llm_client import chat
from src.models.invoice import Invoice
from src.models.result import ValidationResult, ApprovalResult
from src.config.settings import settings
from src.utils.logger import get_logger

log = get_logger(__name__)

SYSTEM_PROMPT = """
You are a VP reviewing invoices for approval.
You will be given invoice details and validation results.
Reason carefully and respond with valid JSON only. No extra text.
Use this exact structure:
{
    "approved": true or false,
    "reasoning": "your reasoning here",
    "requires_review": true or false
}
"""


def approve(invoice: Invoice, validation: ValidationResult) -> ApprovalResult:
    log.info(f"Running approval for invoice: {invoice.invoice_id}")

    requires_review = invoice.amount > settings.approval_threshold

    prompt = f"""
Invoice ID: {invoice.invoice_id}
Vendor: {invoice.vendor}
Amount: ${invoice.amount}
Items: {[f"{i.quantity}x {i.name}" for i in invoice.items]}
Validation passed: {validation.is_valid}
Validation issues: {validation.issues}
Requires extra scrutiny (over ${settings.approval_threshold}): {requires_review}

Should this invoice be approved?
"""

    import json
    response = chat(prompt=prompt, system=SYSTEM_PROMPT)

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        log.warning("LLM returned invalid JSON, defaulting to rejected")
        return ApprovalResult(
            approved=False,
            reasoning="Could not parse approval response",
            requires_review=True,
        )

    return ApprovalResult(
        approved=data.get("approved", False),
        reasoning=data.get("reasoning", ""),
        requires_review=data.get("requires_review", requires_review),
    )
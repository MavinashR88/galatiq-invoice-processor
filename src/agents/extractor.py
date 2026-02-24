from src.tools.pdf_reader import read_file
from src.tools.llm_client import extract_with_tools
from src.models.invoice import Invoice, LineItem
from src.utils.logger import get_logger
from src.utils.exceptions import ExtractionError

log = get_logger(__name__)


def extract(file_path: str) -> Invoice:
    log.info(f"Extracting invoice from: {file_path}")

    raw_text = read_file(file_path)

    log.info(f"Calling LLM tool: extract_invoice")
    data = extract_with_tools(raw_text)

    items = [
        LineItem(
            name=i.get("name", "unknown"),
            quantity=i.get("quantity", 0),
            unit_price=i.get("unit_price", 0.0),
        )
        for i in data.get("items", [])
    ]

    return Invoice(
        invoice_id=data.get("invoice_id") or "unknown",
        vendor=data.get("vendor") or "unknown",
        amount=data.get("amount") or 0.0,
        due_date=data.get("due_date"),
        items=items,
        raw_text=raw_text,
    )
import json
from src.tools.pdf_reader import read_file
from src.tools.llm_client import chat
from src.models.invoice import Invoice, LineItem
from src.utils.logger import get_logger
from src.utils.exceptions import ExtractionError

log = get_logger(__name__)

SYSTEM_PROMPT = """
You are an invoice extraction assistant.
Extract structured data from the invoice text provided.
Always respond with valid JSON only. No extra text.
Use this exact structure:
{
    "invoice_id": "string",
    "vendor": "string",
    "amount": float,
    "due_date": "YYYY-MM-DD or null",
    "items": [
        {"name": "string", "quantity": int, "unit_price": float}
    ]
}
If a field is missing or unclear, use null for strings and 0 for numbers.
"""


def extract(file_path: str) -> Invoice:
    log.info(f"Extracting invoice from: {file_path}")

    raw_text = read_file(file_path)
    response = chat(prompt=raw_text, system=SYSTEM_PROMPT)

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        raise ExtractionError(f"LLM returned invalid JSON: {response}")

    items = [
        LineItem(
            name=i.get("name", "unknown"),
            quantity=i.get("quantity", 0),
            unit_price=i.get("unit_price", 0.0),
        )
        for i in data.get("items", [])
    ]

    return Invoice(
        invoice_id=data.get("invoice_id", "unknown"),
        vendor=data.get("vendor", "unknown"),
        amount=data.get("amount", 0.0),
        due_date=data.get("due_date"),
        items=items,
        raw_text=raw_text,
    )
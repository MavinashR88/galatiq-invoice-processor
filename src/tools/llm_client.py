from openai import OpenAI
from src.config.settings import settings
from src.utils.logger import get_logger
from src.utils.exceptions import ExtractionError

log = get_logger(__name__)

client = OpenAI(
    api_key=settings.groq_api_key,
    base_url="https://api.x.ai/v1",
)

INVOICE_TOOL = {
    "type": "function",
    "function": {
        "name": "extract_invoice",
        "description": "Extract structured invoice data from raw text",
        "parameters": {
            "type": "object",
            "properties": {
                "invoice_id": {"type": "string", "description": "Invoice ID or number"},
                "vendor": {"type": "string", "description": "Vendor or supplier name"},
                "amount": {"type": "number", "description": "Total invoice amount"},
                "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format or null"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "quantity": {"type": "integer"},
                            "unit_price": {"type": "number"}
                        },
                        "required": ["name", "quantity", "unit_price"]
                    }
                }
            },
            "required": ["invoice_id", "vendor", "amount", "items"]
        }
    }
}


def extract_with_tools(prompt: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="grok-3",
            messages=[
                {"role": "system", "content": "You are an invoice extraction assistant. Use the extract_invoice tool to extract data from the invoice."},
                {"role": "user", "content": prompt},
            ],
            tools=[INVOICE_TOOL],
            tool_choice={"type": "function", "function": {"name": "extract_invoice"}},
        )
        tool_call = response.choices[0].message.tool_calls[0]
        import json
        return json.loads(tool_call.function.arguments)
    except Exception as e:
        raise ExtractionError(f"Tool call failed: {e}")


def chat(prompt: str, system: str = "You are a helpful assistant.") -> str:
    try:
        response = client.chat.completions.create(
            model="grok-3",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        raise ExtractionError(f"LLM call failed: {e}")
import pytest
from unittest.mock import patch
from src.agents.extractor import extract


MOCK_TOOL_RESPONSE = {
    "invoice_id": "INV-001",
    "vendor": "Test Vendor",
    "amount": 500.0,
    "due_date": "2024-03-01",
    "items": [
        {"name": "WidgetA", "quantity": 5, "unit_price": 100.0}
    ]
}

MOCK_EMPTY_RESPONSE = {
    "invoice_id": None,
    "vendor": None,
    "amount": 0,
    "due_date": None,
    "items": []
}


def test_extract_valid_invoice():
    with patch("src.agents.extractor.read_file", return_value="raw invoice text"):
        with patch("src.agents.extractor.extract_with_tools", return_value=MOCK_TOOL_RESPONSE):
            invoice = extract("fake/path.txt")

    assert invoice.invoice_id == "INV-001"
    assert invoice.vendor == "Test Vendor"
    assert invoice.amount == 500.0
    assert len(invoice.items) == 1
    assert invoice.items[0].name == "WidgetA"


def test_extract_missing_fields():
    with patch("src.agents.extractor.read_file", return_value="bad invoice text"):
        with patch("src.agents.extractor.extract_with_tools", return_value=MOCK_EMPTY_RESPONSE):
            invoice = extract("fake/path.txt")

    assert invoice.invoice_id == "unknown"
    assert invoice.amount == 0


def test_extract_invalid_json():
    with patch("src.agents.extractor.read_file", return_value="raw text"):
        with patch("src.agents.extractor.extract_with_tools", side_effect=Exception("Tool call failed")):
            with pytest.raises(Exception):
                extract("fake/path.txt")

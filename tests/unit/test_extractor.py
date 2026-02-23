import pytest
from unittest.mock import patch
from src.agents.extractor import extract


def test_extract_valid_invoice():
    mock_response = '''
    {
        "invoice_id": "INV-001",
        "vendor": "Test Vendor",
        "amount": 500.0,
        "due_date": "2024-03-01",
        "items": [
            {"name": "WidgetA", "quantity": 5, "unit_price": 100.0}
        ]
    }
    '''
    with patch("src.agents.extractor.read_file", return_value="raw invoice text"):
        with patch("src.agents.extractor.chat", return_value=mock_response):
            invoice = extract("fake/path.txt")

    assert invoice.invoice_id == "INV-001"
    assert invoice.vendor == "Test Vendor"
    assert invoice.amount == 500.0
    assert len(invoice.items) == 1
    assert invoice.items[0].name == "WidgetA"


def test_extract_missing_fields():
    mock_response = '''
    {
        "invoice_id": null,
        "vendor": null,
        "amount": 0,
        "due_date": null,
        "items": []
    }
    '''
    with patch("src.agents.extractor.read_file", return_value="bad invoice text"):
        with patch("src.agents.extractor.chat", return_value=mock_response):
            invoice = extract("fake/path.txt")

    assert invoice.invoice_id == "unknown"
    assert invoice.amount == 0


def test_extract_invalid_json():
    with patch("src.agents.extractor.read_file", return_value="raw text"):
        with patch("src.agents.extractor.chat", return_value="not json at all"):
            with pytest.raises(Exception):
                extract("fake/path.txt")    
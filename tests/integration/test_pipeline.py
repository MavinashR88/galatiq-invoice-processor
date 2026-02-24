import pytest
from unittest.mock import patch
from src.pipeline.invoice_pipeline import run


MOCK_TOOL_RESPONSE = {
    "invoice_id": "INV-TEST",
    "vendor": "Test Vendor",
    "amount": 500.0,
    "due_date": "2024-03-01",
    "items": [
        {"name": "WidgetA", "quantity": 5, "unit_price": 100.0}
    ]
}

MOCK_LLM_APPROVE = '''
{
    "approved": true,
    "reasoning": "Invoice is valid and under threshold.",
    "requires_review": false
}
'''

MOCK_LLM_REJECT = '''
{
    "approved": false,
    "reasoning": "Insufficient stock.",
    "requires_review": false
}
'''


def test_full_pipeline_approved():
    with patch("src.agents.extractor.read_file", return_value="raw text"):
        with patch("src.agents.extractor.extract_with_tools", return_value=MOCK_TOOL_RESPONSE):
            with patch("src.agents.approver.chat", return_value=MOCK_LLM_APPROVE):
                with patch("src.tools.db_client.get_item", return_value={"item": "WidgetA", "stock": 15}):
                    with patch("src.tools.db_client.has_sufficient_stock", return_value=True):
                        result = run("fake/path.txt")

    assert result["invoice_id"] == "INV-TEST"
    assert result["validation"]["passed"] is True
    assert result["approval"]["approved"] is True
    assert result["payment"]["success"] is True


def test_full_pipeline_rejected():
    with patch("src.agents.extractor.read_file", return_value="raw text"):
        with patch("src.agents.extractor.extract_with_tools", return_value=MOCK_TOOL_RESPONSE):
            with patch("src.agents.approver.chat", return_value=MOCK_LLM_REJECT):
                with patch("src.tools.db_client.get_item", return_value={"item": "WidgetA", "stock": 2}):
                    with patch("src.tools.db_client.has_sufficient_stock", return_value=False):
                        result = run("fake/path.txt")

    assert result["validation"]["passed"] is False
    assert result["approval"]["approved"] is False
    assert result["payment"]["success"] is False

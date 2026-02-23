import pytest
from unittest.mock import patch
from src.agents.validator import validate
from src.models.invoice import Invoice, LineItem


def make_invoice(items):
    return Invoice(
        invoice_id="TEST-001",
        vendor="Test Vendor",
        amount=500.0,
        items=items,
    )


def test_valid_invoice():
    invoice = make_invoice([LineItem(name="WidgetA", quantity=5, unit_price=10.0)])
    with patch("src.agents.validator.get_item", return_value={"item": "WidgetA", "stock": 15}):
        with patch("src.agents.validator.has_sufficient_stock", return_value=True):
            result = validate(invoice)
    assert result.is_valid is True
    assert result.issues == []


def test_insufficient_stock():
    invoice = make_invoice([LineItem(name="GadgetX", quantity=20, unit_price=10.0)])
    with patch("src.agents.validator.get_item", return_value={"item": "GadgetX", "stock": 5}):
        with patch("src.agents.validator.has_sufficient_stock", return_value=False):
            result = validate(invoice)
    assert result.is_valid is False
    assert any("GadgetX" in issue for issue in result.issues)


def test_unknown_item():
    invoice = make_invoice([LineItem(name="SuperGizmo", quantity=1, unit_price=10.0)])
    with patch("src.agents.validator.get_item", return_value=None):
        with patch("src.agents.validator.has_sufficient_stock", return_value=False):
            result = validate(invoice)
    assert result.is_valid is False
    assert any("SuperGizmo" in issue for issue in result.issues)


def test_negative_quantity():
    invoice = make_invoice([LineItem(name="WidgetA", quantity=-1, unit_price=10.0)])
    result = validate(invoice)
    assert result.is_valid is False


def test_invalid_amount():
    invoice = Invoice(
        invoice_id="TEST-002",
        vendor="Test Vendor",
        amount=-100.0,
        items=[],
    )
    result = validate(invoice)
    assert result.is_valid is False
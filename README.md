# Galatiq Invoice Processor

An AI-powered invoice processing pipeline that automates end-to-end invoice handling — from raw document ingestion to payment execution.

Built for Acme Corp to eliminate $2M/year in manual processing costs.

## What It Does

Invoices arrive as PDFs, CSVs, JSONs, or text files. The system:

1. **Extracts** structured data from any format using an LLM
2. **Validates** line items against a live inventory database
3. **Approves or rejects** with AI reasoning (flags invoices over $10K)
4. **Processes payment** or logs rejection with full reasoning

## Tech Stack

- Python 3.13
- xAI Grok (LLM reasoning)
- SQLite (inventory database)
- Pydantic (data validation)
- pdfplumber (PDF extraction)
- pytest (testing)

## Project Structure
```
src/
├── agents/       # extraction, validation, approval, payment
├── pipeline/     # orchestrates all agents
├── tools/        # pdf reader, db client, llm client
├── models/       # Invoice, LineItem, result types
├── config/       # settings from .env
└── utils/        # logger, exceptions
```

## Setup
```bash
git clone https://github.com/mavinashr88/galatiq-invoice-processor
cd galatiq-invoice-processor
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your API key
PYTHONPATH=. python scripts/setup_db.py
```

## Run
```bash
PYTHONPATH=. python main.py --invoice_path=data/invoices/invoice_1001.txt
```

## Test
```bash
PYTHONPATH=. python -m pytest tests/ -v
```

## Sample Output
```json
{
  "invoice_id": "INV-1001",
  "vendor": "Widgets Inc.",
  "amount": 5000.0,
  "validation": { "passed": true, "issues": [] },
  "approval": { "approved": true, "reasoning": "..." },
  "payment": { "success": true, "transaction_id": "..." }
}
```

## Test Cases Covered

| Invoice | Scenario | Result |
|---------|----------|--------|
| INV-1001 | Clean order, within stock | ✅ Approved |
| INV-1002 | Quantity exceeds stock | ❌ Rejected |
| INV-1003 | Fraudulent vendor, zero stock | ❌ Rejected |
| INV-1004 | JSON format, clean order | ✅ Approved |
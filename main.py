import argparse
import json
from pathlib import Path
from src.pipeline.invoice_pipeline import run
from src.utils.logger import get_logger

log = get_logger(__name__)

SUPPORTED_FORMATS = {".txt", ".pdf", ".json", ".csv", ".xml"}


def print_result(result: dict):
    print("\n" + "=" * 60)
    print("  INVOICE PROCESSING REPORT")
    print("=" * 60)
    print(f"  Invoice ID : {result['invoice_id']}")
    print(f"  Vendor     : {result['vendor']}")
    print(f"  Amount     : ${result['amount']}")
    print("-" * 60)
    print(f"  VALIDATION : {'✅ PASSED' if result['validation']['passed'] else '❌ FAILED'}")
    if result['validation']['issues']:
        for issue in result['validation']['issues']:
            print(f"    → {issue}")
    print("-" * 60)
    print(f"  APPROVAL   : {'✅ APPROVED' if result['approval']['approved'] else '❌ REJECTED'}")
    print(f"    → {result['approval']['reasoning']}")
    print("-" * 60)
    print(f"  PAYMENT    : {'✅ SUCCESS' if result['payment']['success'] else '⏭️  SKIPPED'}")
    print(f"    → {result['payment']['message']}")
    if result['payment']['transaction_id']:
        print(f"    → Transaction ID: {result['payment']['transaction_id']}")
    print("=" * 60 + "\n")


def process_single(invoice_path: str):
    result = run(invoice_path)
    print_result(result)


def process_batch(invoice_dir: str):
    folder = Path(invoice_dir)
    files = [f for f in folder.iterdir() if f.suffix in SUPPORTED_FORMATS]

    if not files:
        print(f"No supported invoices found in {invoice_dir}")
        return

    print(f"\nProcessing {len(files)} invoices...\n")

    results = {"approved": [], "rejected": [], "errors": []}

    for file in sorted(files):
        try:
            result = run(str(file))
            print_result(result)
            if result["payment"]["success"]:
                results["approved"].append(result["invoice_id"])
            else:
                results["rejected"].append(result["invoice_id"])
        except Exception as e:
            log.error(f"Failed to process {file.name}: {e}")
            results["errors"].append(file.name)

    print("=" * 60)
    print("  BATCH SUMMARY")
    print("=" * 60)
    print(f"  ✅ Approved : {len(results['approved'])} invoices")
    print(f"  ❌ Rejected : {len(results['rejected'])} invoices")
    print(f"  ⚠️  Errors   : {len(results['errors'])} invoices")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Invoice Processing System")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--invoice_path", help="Path to a single invoice file")
    group.add_argument("--invoice_dir", help="Path to a folder of invoices")
    args = parser.parse_args()

    if args.invoice_path:
        process_single(args.invoice_path)
    else:
        process_batch(args.invoice_dir)


if __name__ == "__main__":
    main()
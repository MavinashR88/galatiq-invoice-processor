import argparse
import json
from src.pipeline.invoice_pipeline import run


def main():
    parser = argparse.ArgumentParser(description="Invoice Processing System")
    parser.add_argument("--invoice_path", required=True, help="Path to invoice file")
    args = parser.parse_args()

    result = run(args.invoice_path)

    print("\n" + "=" * 50)
    print("PIPELINE RESULT")
    print("=" * 50)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
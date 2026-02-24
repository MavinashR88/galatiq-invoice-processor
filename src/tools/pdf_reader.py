import pdfplumber
import csv
from pathlib import Path
from src.utils.logger import get_logger
from src.utils.exceptions import ExtractionError

log = get_logger(__name__)


def read_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise ExtractionError(f"File not found: {file_path}")

    if path.suffix == ".pdf":
        return _read_pdf(path)

    if path.suffix == ".csv":
        return _read_csv(path)

    return path.read_text(encoding="utf-8")


def _read_pdf(path: Path) -> str:
    try:
        with pdfplumber.open(path) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
            return "\n".join(pages)
    except Exception as e:
        raise ExtractionError(f"Failed to read PDF: {e}")


def _read_csv(path: Path) -> str:
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [str(row) for row in reader]
            return "\n".join(rows)
    except Exception as e:
        raise ExtractionError(f"Failed to read CSV: {e}")
import sqlite3
from src.config.settings import settings
from src.utils.logger import get_logger
from src.utils.exceptions import ValidationError

log = get_logger(__name__)


def get_item(item_name: str) -> dict | None:
    try:
        conn = sqlite3.connect(settings.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT item, stock FROM inventory WHERE item = ?", (item_name,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return {"item": row[0], "stock": row[1]}

    except Exception as e:
        raise ValidationError(f"Database error: {e}")


def item_exists(item_name: str) -> bool:
    return get_item(item_name) is not None


def has_sufficient_stock(item_name: str, quantity: int) -> bool:
    item = get_item(item_name)
    if item is None:
        return False
    return item["stock"] >= quantity
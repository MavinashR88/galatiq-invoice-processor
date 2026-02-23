import sqlite3
import os
from src.config.settings import settings


def setup():
    os.makedirs(os.path.dirname(settings.db_path), exist_ok=True)

    conn = sqlite3.connect(settings.db_path)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS inventory")
    cursor.execute("CREATE TABLE inventory (item TEXT PRIMARY KEY, stock INTEGER)")

    cursor.executemany("INSERT INTO inventory VALUES (?, ?)", [
        ("WidgetA", 15),
        ("WidgetB", 10),
        ("GadgetX", 5),
        ("FakeItem", 0),
    ])

    conn.commit()
    conn.close()

    print(f"Database created at: {settings.db_path}")


if __name__ == "__main__":
    setup()
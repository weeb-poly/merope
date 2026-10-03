import json
import sqlite3
from pathlib import Path


def main():
    db = sqlite3.connect("users.db")
    with db:
        cur = db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                discord INTEGER,
                matrix TEXT
            )
        """)
        cur.close()

    data_file = Path("users.json")

    if data_file.is_file():
        with data_file.open() as f:
            data = json.load(f)

        with db:
            cur = db.executemany(
                "INSERT OR IGNORE INTO users(discord, matrix) VALUES(?, ?)",
                ((user["discord"], user["matrix"],) for user in data)
            )
            cur.close()

    db.close()

if __name__ == "__main__":
    main()

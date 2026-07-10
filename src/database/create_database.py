from pathlib import Path

from src.database.connection import get_connection


def create_database():

    conn = get_connection()

    cursor = conn.cursor()

    schema = Path("db/schema.sql").read_text(encoding="utf-8")

    cursor.executescript(schema)

    conn.commit()

    conn.close()

    print("Database created successfully.")


if __name__ == "__main__":
    create_database()
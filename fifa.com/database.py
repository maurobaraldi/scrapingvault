import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path: str):
        Path(db_path).touch(exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()

    def create_table(self, table_name: str, columns: dict):
        cols = ", ".join(f"{k} {v}" for k, v in columns.items())
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})"
        )

    # def insert_or_ignore(self, table_name: str, record: dict):
    #     cols = ", ".join(record.keys())
    #     placeholders = ", ".join("?" for _ in record)
    #     self.cursor.execute(
    #         f"INSERT OR IGNORE INTO {table_name} ({cols}) VALUES ({placeholders})",
    #         tuple(record.values()),
    #     )

    def insert_or_ignore(self, table_name: str, records):
        """
        Insert one or many records using INSERT OR IGNORE.

        Args:
            table_name: Name of the table.
            records: A dict or a list of dicts.

        Examples:
            db.insert_or_ignore("users", {
                "id": 1,
                "name": "Alice",
                "email": "alice@example.com",
            })

            db.insert_or_ignore("users", [
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
                {"id": 3, "name": "Carol", "email": "carol@example.com"},
            ])
        """
        if isinstance(records, dict):
            records = [records]

        records = list(records)
        if not records:
            return

        columns = list(records[0].keys())

        # Ensure every record has the same keys
        for record in records:
            if list(record.keys()) != columns:
                raise ValueError("All records must have the same columns and order.")

        placeholders = ", ".join("?" for _ in columns)
        sql = (
            f"INSERT OR IGNORE INTO {table_name} "
            f"({', '.join(columns)}) VALUES ({placeholders})"
        )

        values = [tuple(record[col] for col in columns) for record in records]

        self.cursor.executemany(sql, values)

    def execute(self, sql, params=()):
        return self.cursor.execute(sql, params)
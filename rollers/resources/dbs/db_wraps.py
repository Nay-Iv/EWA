import sqlite3
from enum import Enum
from datetime import date, datetime


class SQLTypes(Enum):
    INTEGER = "INTEGER"
    TEXT = "TEXT"
    REAL = "REAL"
    NUMERIC = "NUMERIC"
    BLOB = "BLOB"
    DATETIME = "DATETIME"
    BOOLEAN = "BOOLEAN"
    PRIMARY_KEY = "INTEGER PRIMARY KEY"
    FOREIGN_KEY = "INTEGER REFERENCES {}"
    ID = "integer primary key autoincrement"


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table_from_data(self, table_name, data):
        columns = self._generate_schema(data[0])
        self.create_table(table_name, columns)
        for row in data:
            self.insert(table_name, row)

    def create_table(self, table_name, columns):
        columns_str = ", ".join([f"{col_name} {col_type.value}" for col_name, col_type in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.cursor.execute(query)
        self.conn.commit()

    def insert(self, table_name, data):
        columns = ", ".join(data.keys())
        values = ", ".join(["?" for _ in data.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.cursor.execute(query, tuple(self._format_values(data)))
        self.conn.commit()

    def select(self, table_name, columns="*", condition=None, join_type=None, join_table=None, join_condition=None):
        columns_str = ", ".join(columns) if isinstance(columns, (list, tuple)) else columns
        condition_str = f"WHERE {condition}" if condition else ""
        join_str = self._generate_join_clause(join_type, join_table, join_condition)
        query = f"SELECT {columns_str} FROM {table_name} {join_str} {condition_str}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, table_name, data, condition):
        set_str = ", ".join([f"{col_name}=?" for col_name in data.keys()])
        values = tuple(data.values())
        condition_str = f"WHERE {condition}"
        query = f"UPDATE {table_name} SET {set_str} {condition_str}"
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete(self, table_name, condition):
        condition_str = f"WHERE {condition}"
        query = f"DELETE FROM {table_name} {condition_str}"
        self.cursor.execute(query)
        self.conn.commit()

    def _generate_join_clause(self, join_type, join_table, join_condition):
        join_types = {
            "inner": "INNER JOIN",
            "left": "LEFT JOIN",
            "right": "RIGHT JOIN",
            "full": "FULL OUTER JOIN",
            "cross": "CROSS JOIN"
        }
        join_str = f"{join_types.get(join_type, '')} {join_table}" if join_table else ""
        condition_str = f"ON {join_condition}" if join_condition else ""
        return f"{join_str} {condition_str}"

    def _generate_schema(self, row):
        columns = {}
        for key, value in row.items():
            column_type = self._infer_type(value)
            columns[key] = column_type
        return columns

    def _infer_type(self, value):
        if isinstance(value, int):
            return SQLTypes.INTEGER
        elif isinstance(value, float):
            return SQLTypes.REAL
        elif isinstance(value, bool):
            return SQLTypes.BOOLEAN
        elif isinstance(value, str):
            return SQLTypes.TEXT
        elif isinstance(value, date):
            return SQLTypes.DATE
        elif isinstance(value, datetime):
            return SQLTypes.DATETIME
        else:
            return SQLTypes.BLOB

    def _format_values(self, data):
        values = []
        for value in data.values():
            if isinstance(value, date):
                values.append(value.isoformat())
            elif isinstance(value, datetime):
                values.append(value.isoformat())
            else:
                values.append(value)
        return values

    def __del__(self):
        self.conn.close()
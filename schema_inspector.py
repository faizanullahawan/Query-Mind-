
from sqlalchemy import inspect
from connection import engine


def get_database_schema():
    try:
        inspector = inspect(engine)

        schema = {}

        table_names = inspector.get_table_names()

        for table_name in table_names:
            columns = inspector.get_columns(table_name)

            schema[table_name] = []

            for column in columns:
                column_info = {
                    "column_name": column["name"],
                    "data_type": str(column["type"]),
                    "nullable": column["nullable"],
                    "primary_key": column.get("primary_key", False)
                }

                schema[table_name].append(column_info)

        return schema

    except Exception as error:
        print(f"Schema inspection failed: {error}")
        return {}


def display_schema():
    schema = get_database_schema()

    if not schema:
        print("No tables found in the database.")
        return

    print("\n========== DATABASE SCHEMA ==========\n")

    for table_name, columns in schema.items():
        print(f"TABLE: {table_name}")
        print("-" * 40)

        for column in columns:
            print(
                f"Column: {column['column_name']} | "
                f"Type: {column['data_type']} | "
                f"Nullable: {column['nullable']} | "
                f"Primary Key: {column['primary_key']}"
            )

        print()


if __name__ == "__main__":
    display_schema()

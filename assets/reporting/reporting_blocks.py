"""Small building blocks for SQL, Python and reporting workflows.

Names and file locations are supplied by the caller. Examples require pandas;
SQL functions also require SQLAlchemy and a caller-supplied connection.
"""
import pandas as pd


def read_sql_table(connection, query, parameters):
    from sqlalchemy import text
    return pd.read_sql_query(text(query), connection, params=parameters)


def clean_columns(table, date_columns, text_columns):
    table = table.copy()
    for column in date_columns:
        table[column] = pd.to_datetime(table[column])
    for column in text_columns:
        table[column] = table[column].str.strip()
    return table


def combine_and_match(records, batches, key, join_type):
    combined = pd.concat(batches, ignore_index=True)
    return records.merge(combined, on=key, how=join_type)


def select_rows(table, condition):
    return table.loc[condition].copy()


def summarise(table, group_columns, calculations):
    return table.groupby(group_columns).agg(calculations).reset_index()


def api_rows_to_table(rows, column_names):
    return pd.DataFrame.from_records(rows, columns=column_names)


def save_outputs(table, engine, table_name, csv_file):
    table.to_sql(table_name, con=engine, index=False, if_exists='replace')
    table.to_csv(csv_file, index=False)

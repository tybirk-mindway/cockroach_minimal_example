from db import engine
from cockroachdb.sqlalchemy import run_transaction
from sqlalchemy.orm import sessionmaker
import db_models
import pandas as pd


def insert_dataframe_to_database(df, table_name):
    table_name_to_model_name = {
        "transaction_data": "Transactions",
    }
    db_table = getattr(db_models, table_name_to_model_name[table_name])

    def add_data(session, data_bulk, db_table):
        # Alternative insertion method
        data = []
        for row in data_bulk:  # data_bulk is a list of dicts
            data.append(db_table(**row))
        session.bulk_save_objects(data)

    chunksize = 500
    data_bulks = [
        df.iloc[i : i + chunksize - 1].to_dict(orient="records")
        for i in range(0, len(df), chunksize)
    ]

    for bulk in data_bulks:
        run_transaction(
            sessionmaker(bind=engine),
            # lambda session: add_data(session, bulk, db_table),
            lambda session: session.bulk_insert_mappings(db_table, bulk),
        )


if __name__ == "__main__":
    db_models.Base.metadata.create_all(bind=engine)
    transaction_data = pd.read_csv("transactions.csv", parse_dates=["time"])
    print("First 30 entries in data")
    print(transaction_data.iloc[:30])
    insert_dataframe_to_database(transaction_data, "transaction_data")
    print("Inserted data")

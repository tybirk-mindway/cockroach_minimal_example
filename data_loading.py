import uuid
import pandas as pd
import numpy as np


columns_rename_dict: dict = {"start_time": "time"}

PLAYER_ID_TO_UUID = {**{str(i): uuid.uuid4() for i in range(101)}}


def load_transaction_data(filename="transactions.csv"):
    transaction_data = pd.read_csv(filename, parse_dates=["time"]).rename(
        columns_rename_dict, axis=1
    )
    transaction_data = add_net_amounts(transaction_data)
    return sort_and_index_data(transaction_data)


def add_net_amounts(trans):
    """Add column with net amount to transaction data. deposits negative,
    withdrawals positive, cancelled withdrawals negative"""
    net_amounts = np.zeros(len(trans))
    deposits = trans["transaction_type"] == 0
    withdrawals = trans["transaction_type"] == 1
    cancelled_withdrawals = trans["transaction_type"] == 3

    net_amounts[deposits] = -trans.loc[deposits, "amount"]
    net_amounts[withdrawals] = trans.loc[withdrawals, "amount"]
    net_amounts[cancelled_withdrawals] = -trans.loc[cancelled_withdrawals, "amount"]

    trans["net_amount"] = net_amounts
    return trans


def sort_and_index_data(df):
    if df is not None:
        df["player_id"] = df["player_id"].astype(str)
        df["player_id"].replace(PLAYER_ID_TO_UUID, inplace=True)
        df = df.sort_values(by=["player_id", "time"]).set_index("player_id").iloc[:1000]

        return df
    else:
        return None


if __name__ == "__main__":
    data = load_transaction_data("transactions.csv")
    data.to_csv("new_transactions.csv")

import pandas as pd
import unittest
from pandas.testing import assert_frame_equal
from src.coding import extract, transform, load

def test_extract():
    df_users = extract('data/users.csv')
    assert isinstance(df_users, pd.DataFrame)
    assert len(df_users) == 3

def test_transform():
    users_df = extract('data/users.csv')
    transactions_df = extract('data/transactions.csv')
    transformed_df = transform(users_df, transactions_df)
    assert_frame_equal(transformed_df,(pd.DataFrame({'user_id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Charlie'], 'email': ['alice@example.com', 'Bob@example.com', 'charlie@example.com'], 'amount': [70, 40, 40]})))

def test_load():
    df = extract('data/users.csv')
    load('data/test_output.csv', df)
    loaded_df = pd.read_csv('data/test_output.csv')
    assert loaded_df.equals(df)

if __name__ == '__main__':
    test_extract()
    test_transform()
    test_load()
    print("All tests passed!")
import pandas as pd
import unittest
from pandas.testing import assert_frame_equal
from src.coding import extract, transform, load

class TestCoding(unittest.TestCase):

    def test_extract(self):
        df_users = extract('data/users.csv')
        self.assertIsInstance(df_users, pd.DataFrame)
        self.assertEqual(len(df_users), 3)

    def test_transform(self):
        users_df = extract('data/users.csv')
        transactions_df = extract('data/transactions.csv')
        transformed_df = transform(users_df, transactions_df)
        expected_df = pd.DataFrame({'user_id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Charlie'], 'email': ['alice@example.com', 'Bob@example.com', 'charlie@example.com'], 'amount': [70, 40, 40]})
        assert_frame_equal(transformed_df, expected_df)

    def test_load(self):
        df = extract('data/users.csv')
        load('data/test_output.csv', df)
        loaded_df = pd.read_csv('data/test_output.csv')
        self.assertTrue(loaded_df.equals(df))

if __name__ == '__main__':
    unittest.main()
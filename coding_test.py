import pandas as pd

def extract(file_path):
    return pd.read_csv(file_path)

def transform(users_df, transactions_df):
    merged_df = pd.merge(users_df, transactions_df.groupby('user_id')['amount'].sum(), on='user_id', how='left')
    return merged_df.fillna(0)

def load(output_path, transformed_df):
    transformed_df.to_csv(output_path, index=False)

if __name__ == '__main__':
    users_df = extract('users.csv')
    transactions_df = extract('transactions.csv')
    transformed_df = transform(users_df, transactions_df)
    load('user_transaction_summary.csv', transformed_df)
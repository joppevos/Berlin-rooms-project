import sqlite3
import pandas as pd

db = sqlite3.connect('ebay-rooms.db')

def run_query(query):
    return pd.read_sql_query(query, db)

query = "SELECT * FROM rooms;"
print(run_query(query))
